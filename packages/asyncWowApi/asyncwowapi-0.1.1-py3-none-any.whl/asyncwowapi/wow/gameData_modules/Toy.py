from asyncwowapi.api_client import ApiClient


class ToyAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def toy_index(self):
        endpoint = "/data/wow/toy/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def toy(self, toyId: int):
        endpoint = f"/data/wow/toy/{toyId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
