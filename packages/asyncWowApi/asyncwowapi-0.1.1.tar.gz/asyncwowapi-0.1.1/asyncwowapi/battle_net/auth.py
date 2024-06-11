import aiohttp

class AuthManager:
    def __init__(self, client_id: str, client_secret: str, region: str = 'eu'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.region = region
        self.token_url = "https://oauth.battle.net/token"
        self._token = None
        self._session = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        if self._session:
            await self._session.close()
            self._session = None

    async def _fetch_token(self) -> str:
        if self._session is None:
            self._session = aiohttp.ClientSession()
        try:
            async with self._session.post(self.token_url, data={"grant_type": "client_credentials"},
                                          auth=aiohttp.BasicAuth(self.client_id, self.client_secret)) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"Failed to fetch token: {await resp.text()} (status: {resp.status})")
                response_data = await resp.json()
                self._token = response_data['access_token']
                return self._token
        finally:
            await self.close()

    async def get_token(self) -> str:
        if self._token is None:
            return await self._fetch_token()
        return self._token

    async def rotate_token(self):
        self._token = None
        await self._fetch_token()
