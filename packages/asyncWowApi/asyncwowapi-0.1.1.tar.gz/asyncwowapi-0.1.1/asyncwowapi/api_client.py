import aiohttp
from typing import Optional
from pydantic import ValidationError
from asyncwowapi.battle_net.auth import AuthManager
from asyncwowapi.validators import RequestParams


class ApiClient:
    """
    An API client for accessing Blizzard's APIs.

    Args:
        client_id (str, optional): The client ID for authentication.
        client_secret (str, optional): The client secret for authentication.
        token (str, optional): An authentication token.
        region (str, optional): The region for accessing the API. Defaults to 'eu'.
        locale (str, optional): The locale for data localization. Defaults to 'en_US'.

    Raises:
        ValueError: If neither client_id and client_secret nor token is provided.
                    Both client_id and client_secret or token must be provided.

    Note:
        Either a token or both client_id and client_secret must be provided for authentication.
        If both client_id and client_secret are provided, an authentication token will be generated
        using the provided credentials via AuthManager.
    """

    def __init__(self, client_id=None, client_secret=None, token=None, region: str = 'eu', locale: str = 'en_US'):
        self.token = None
        if (client_id is None or client_secret is None) and token is None:
            raise ValueError("Either provide both client_id and client_secret or token, not neither.")

        if client_id is not None and client_secret is not None:
            self.auth_manager = AuthManager(client_id, client_secret, region)
        elif token is not None:
            self.token = token
        else:
            raise ValueError("Either both client_id and client_secret or token must be provided.")

        self.region = region
        self.BASE_URL = f"https://{self.region}.api.blizzard.com"
        self.locale = locale
        self._session = None
        self.namespace = {
            "static": "static-" + self.region,
            "dynamic": "dynamic-" + self.region,
            "profile": "profile-" + self.region
        }

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        if self._session:
            await self._session.close()
            self._session = None

    async def get(self, url: str, namespace: str, params: Optional[dict] = None) -> dict:
        if self._session is None:
            self._session = aiohttp.ClientSession()

        try:
            req_params = RequestParams(namespace=namespace, locale=self.locale)
        except ValidationError as e:
            raise ValueError(f"Invalid request parameters: {e}")

        headers = {
            "namespace": namespace
        }

        if hasattr(self, 'auth_manager'):
            token = await self.auth_manager.get_token()
            headers["Authorization"] = "Bearer " + token
            self.token = token
        elif self.token is not None:
            headers["Authorization"] = "Bearer " + self.token

        if params is None:
            params = {}
        params['namespace'] = namespace
        params['locale'] = req_params.locale
        try:
            async with self._session.get(url, headers=headers, params=params) as resp:
                if resp.status == 401 and hasattr(self, 'auth_manager'):
                    await self.auth_manager.rotate_token()
                    return await self.get(url, namespace, params)
                resp.raise_for_status()
                return await resp.json()
        finally:
            await self.close()

    async def get_by_endpoint(self, endpoint: str, namespace: str, params: Optional[dict] = None) -> dict:
        url = self.BASE_URL + endpoint
        return await self.get(url, namespace, params)
