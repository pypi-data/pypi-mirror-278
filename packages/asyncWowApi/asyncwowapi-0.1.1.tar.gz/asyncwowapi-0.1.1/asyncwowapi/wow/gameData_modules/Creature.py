from asyncwowapi.api_client import ApiClient


class CreatureAPI:

    def __init__(self, client: ApiClient):
        self.client = client


    async def creature_families_index(self):
        endpoint = "/data/wow/creature-family/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def creature_family(self, creatureFamilyId: int):
        endpoint = f"/data/wow/creature-family/{creatureFamilyId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def creature_types_index(self):
        endpoint = "/data/wow/creature-type/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def creature_type(self, creatureTypeId: int):
        endpoint = f"/data/wow/creature-type/{creatureTypeId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def creature(self, creatureId: int):
        endpoint = f"/data/wow/creature/{creatureId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def creature_search(self, query: str):
        endpoint = f"/data/wow/search/creature?name={query}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def creature_display_media(self, creatureDisplayId: int):
        endpoint = f"/data/wow/media/creature-display/{creatureDisplayId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def creature_family_media(self, creatureFamilyId: int):
        endpoint = f"/data/wow/media/creature-family/{creatureFamilyId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
