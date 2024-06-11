from asyncwowapi.api_client import ApiClient


class CharacterProfileAPI:
    def __init__(self, client: ApiClient):
        self.client = client

    async def character_profile_summary(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])

    async def character_profile_status(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/status"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])
