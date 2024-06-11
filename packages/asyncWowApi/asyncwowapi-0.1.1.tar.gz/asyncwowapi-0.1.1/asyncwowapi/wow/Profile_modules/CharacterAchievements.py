from asyncwowapi.api_client import ApiClient


class CharacterAchievementsAPI:
    def __init__(self, client: ApiClient):
        self.client = client

    async def character_achievements_summary(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/achievements"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])

    async def character_achievements_statistics(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/achievements/statistics"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])
