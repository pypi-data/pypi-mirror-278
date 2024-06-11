from asyncwowapi.api_client import ApiClient


class ItemAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def item_classes_index(self):
        endpoint = "/data/wow/item-class/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def item_class(self, itemClassId: int):
        endpoint = f"/data/wow/item-class/{itemClassId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def item_sets_index(self):
        endpoint = "/data/wow/item-set/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def item_set(self, itemSetId: int):
        endpoint = f"/data/wow/item-set/{itemSetId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def item_subclass(self, itemClassId: int, itemSubclassId: int):
        endpoint = f"/data/wow/item-class/{itemClassId}/item-subclass/{itemSubclassId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def item(self, itemId: int):
        endpoint = f"/data/wow/item/{itemId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def item_media(self, itemId: int):
        endpoint = f"/data/wow/media/item/{itemId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def item_search(self, query: str):
        endpoint = f"/data/wow/search/item?name={query}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
