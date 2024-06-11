from asyncwowapi.api_client import ApiClient


class CharacterSoulbindsAPI:
    def __init__(self, client: ApiClient):
        self.client = client

    async def character_soulbinds(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/soulbinds"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])
