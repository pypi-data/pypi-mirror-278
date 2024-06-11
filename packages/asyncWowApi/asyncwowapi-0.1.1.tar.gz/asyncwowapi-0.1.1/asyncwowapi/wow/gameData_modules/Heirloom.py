from asyncwowapi.api_client import ApiClient


class HeirloomAPI:

    def __init__(self, client: ApiClient):
        self.client = client


    async def heirloom_index(self):
        endpoint = "/data/wow/heirloom/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def heirloom(self, heirloomId: int):
        endpoint = f"/data/wow/heirloom/{heirloomId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
