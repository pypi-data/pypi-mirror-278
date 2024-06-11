from asyncwowapi.api_client import ApiClient


class CharacterPvPAPI:
    def __init__(self, client: ApiClient):
        self.client = client

    async def character_pvp_bracket_statistics(self, realm_slug: str, character_name: str, pvp_bracket: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/pvp-bracket/{pvp_bracket}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])

    async def character_pvp_summary(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/pvp-summary"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])
