from asyncwowapi.api_client import ApiClient


class SpellAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def spell(self, spellId: int):
        endpoint = f"/data/wow/spell/{spellId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def spell_media(self, spellId: int):
        endpoint = f"/data/wow/media/spell/{spellId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def spell_search(self, query: str):
        endpoint = f"/data/wow/search/spell?name={query}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
