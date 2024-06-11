from asyncwowapi.api_client import ApiClient


class TitleAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def titles_index(self):
        endpoint = "/data/wow/title/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def title(self, titleId: int):
        endpoint = f"/data/wow/title/{titleId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
