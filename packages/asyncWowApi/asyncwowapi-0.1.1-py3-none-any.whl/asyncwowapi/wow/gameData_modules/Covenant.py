from asyncwowapi.api_client import ApiClient


class CovenantAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def covenant_index(self):
        endpoint = "/data/wow/covenant/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def covenant(self, covenantId: int):
        endpoint = f"/data/wow/covenant/{covenantId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def covenant_media(self, covenantId: int):
        endpoint = f"/data/wow/media/covenant/{covenantId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def soulbind_index(self):
        endpoint = "/data/wow/covenant/soulbind/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def soulbind(self, soulbindId: int):
        endpoint = f"/data/wow/covenant/soulbind/{soulbindId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def conduit_index(self):
        endpoint = "/data/wow/covenant/conduit/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def conduit(self, conduitId: int):
        endpoint = f"/data/wow/covenant/conduit/{conduitId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
