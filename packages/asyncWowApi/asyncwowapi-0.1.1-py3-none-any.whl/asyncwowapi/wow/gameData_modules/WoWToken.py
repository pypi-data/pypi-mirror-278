from asyncwowapi.api_client import ApiClient


class WoWTokenAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def wow_token_index(self):
        endpoint = "/data/wow/token/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])
