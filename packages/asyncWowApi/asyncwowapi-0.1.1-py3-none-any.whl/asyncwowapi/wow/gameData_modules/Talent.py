from asyncwowapi.api_client import ApiClient


class TalentAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def talent_tree_index(self):
        endpoint = "/data/wow/talent-tree/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def talent_tree(self, talentTreeId: int, specId: int):
        endpoint = f"/data/wow/talent-tree/{talentTreeId}/playable-specialization/{specId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def talent_tree_nodes(self, talentTreeId: int):
        endpoint = f"/data/wow/talent-tree/{talentTreeId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def talents_index(self):
        endpoint = "/data/wow/talent/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def talent(self, talentId: int):
        endpoint = f"/data/wow/talent/{talentId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def pvp_talents_index(self):
        endpoint = "/data/wow/pvp-talent/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def pvp_talent(self, pvpTalentId: int):
        endpoint = f"/data/wow/pvp-talent/{pvpTalentId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
