from asyncwowapi.api_client import ApiClient


class CharacterMythicKeystoneProfileAPI:
    def __init__(self, client: ApiClient):
        self.client = client

    async def character_mythic_keystone_profile_index(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/mythic-keystone-profile"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])

    async def character_mythic_keystone_season_details(self, realm_slug: str, character_name: str, season_id: int):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/mythic-keystone-profile/season/{season_id}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])
