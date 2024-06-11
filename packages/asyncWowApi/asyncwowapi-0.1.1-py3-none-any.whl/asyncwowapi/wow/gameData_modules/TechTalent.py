from asyncwowapi.api_client import ApiClient


class TechTalentAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def tech_talent_tree_index(self):
        endpoint = "/data/wow/tech-talent-tree/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def tech_talent_tree(self, techTalentTreeId: int):
        endpoint = f"/data/wow/tech-talent-tree/{techTalentTreeId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def tech_talent_index(self):
        endpoint = "/data/wow/tech-talent/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def tech_talent(self, techTalentId: int):
        endpoint = f"/data/wow/tech-talent/{techTalentId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def tech_talent_media(self, techTalentId: int):
        endpoint = f"/data/wow/media/tech-talent/{techTalentId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
