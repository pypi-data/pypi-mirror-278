from asyncwowapi.api_client import ApiClient


class CharacterEncountersAPI:
    def __init__(self, client: ApiClient):
        self.client = client

    async def character_encounters_summary(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/encounters"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])

    async def character_dungeons(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/encounters/dungeons"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])

    async def character_raids(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/encounters/raids"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])
