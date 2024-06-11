from asyncwowapi.api_client import ApiClient


class CharacterQuestsAPI:
    def __init__(self, client: ApiClient):
        self.client = client

    async def character_quests(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/quests"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])

    async def character_completed_quests(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/quests/completed"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])
