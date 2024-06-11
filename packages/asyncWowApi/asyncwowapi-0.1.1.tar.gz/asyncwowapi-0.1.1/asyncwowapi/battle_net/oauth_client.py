import aiohttp
from urllib.parse import urlencode


class OAuthClient:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, region: str = 'us'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.region = region
        self.base_url = f"https://{self.region}.api.blizzard.com"
        self.auth_url = f"https://oauth.battle.net/authorize"
        self.token_url = f"https://oauth.battle.net/token"

    def get_authorization_url(self, scope: str, state: str) -> str:
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': scope,
            'state': state
        }
        return f"{self.auth_url}?{urlencode(params)}"

    async def exchange_code_for_token(self, code: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.token_url, data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_uri,
            }, auth=aiohttp.BasicAuth(self.client_id, self.client_secret)) as resp:
                return await resp.json()

    async def get_user_info(self, access_token: str) -> dict:
        url = "https://oauth.battle.net/userinfo"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                return await resp.json()
