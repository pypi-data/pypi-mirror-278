from asyncwowapi.api_client import ApiClient


class CharacterSpecializationsAPI:
    def __init__(self, client: ApiClient):
        self.client = client

    async def character_specializations_summary(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/specializations"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])
