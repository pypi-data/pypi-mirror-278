from asyncwowapi.api_client import ApiClient


class CharacterCollectionsAPI:
    def __init__(self, client: ApiClient):
        self.client = client

    async def character_collections_index(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/collections"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])

    async def character_mounts_collection_summary(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/collections/mounts"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])

    async def character_pets_collection_summary(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/collections/pets"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])

    async def character_toys_collection_summary(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/collections/toys"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])

    async def character_heirlooms_collection_summary(self, realm_slug: str, character_name: str):
        endpoint = f"/profile/wow/character/{realm_slug}/{character_name}/collections/heirlooms"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])
