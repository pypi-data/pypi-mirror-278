from asyncwowapi.api_client import ApiClient


class QuestAPI:

    def __init__(self, client: ApiClient):
        self.client = client


    async def quests_index(self):
        endpoint = "/data/wow/quest/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def quest(self, questId: int):
        endpoint = f"/data/wow/quest/{questId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def quest_categories_index(self):
        endpoint = "/data/wow/quest/category/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def quest_category(self, questCategoryId: int):
        endpoint = f"/data/wow/quest/category/{questCategoryId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def quest_areas_index(self):
        endpoint = "/data/wow/quest/area/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def quest_area(self, questAreaId: int):
        endpoint = f"/data/wow/quest/area/{questAreaId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def quest_types_index(self):
        endpoint = "/data/wow/quest/type/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def quest_type(self, questTypeId: int):
        endpoint = f"/data/wow/quest/type/{questTypeId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
