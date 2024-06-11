from asyncwowapi.api_client import ApiClient


class CharacterMediaAPI:
    def __init__(self, client: ApiClient):
        self.client = client

    async def character_media_summary(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/character-media"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])
