from asyncwowapi.api_client import ApiClient


class ModifiedCraftingAPI:

    def __init__(self, client: ApiClient):
        self.client = client


    async def modified_crafting_index(self):
        endpoint = "/data/wow/modified-crafting/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def modified_crafting_category_index(self):
        endpoint = "/data/wow/modified-crafting/category/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def modified_crafting_category(self, categoryId: int):
        endpoint = f"/data/wow/modified-crafting/category/{categoryId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def modified_crafting_reagent_slot_type_index(self):
        endpoint = "/data/wow/modified-crafting/reagent-slot-type/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def modified_crafting_reagent_slot_type(self, slotTypeId: int):
        endpoint = f"/data/wow/modified-crafting/reagent-slot-type/{slotTypeId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
