from asyncwowapi.api_client import ApiClient


class AccountProfileAPI:
    def __init__(self, client: ApiClient):
        self.client = client

    def _get_namespace(self) -> str:
        return f"profile-{self.client.region}"

    async def profile_summary(self):
        endpoint = f"/profile/user/wow"
        return await self.client.get_by_endpoint(endpoint, self._get_namespace())

    async def protected_character_summary(self, realm_id: int, character_id: int):
        endpoint = f"/profile/user/wow/protected-character/{realm_id}-{character_id}"
        return await self.client.get_by_endpoint(endpoint, self._get_namespace())

    async def account_collections_index(self):
        endpoint = f"/profile/user/wow/collections"
        return await self.client.get_by_endpoint(endpoint, self._get_namespace())

    async def mounts_collection_summary(self):
        endpoint = f"/profile/user/wow/collections/mounts"
        return await self.client.get_by_endpoint(endpoint, self._get_namespace())

    async def pets_collection_summary(self):
        endpoint = f"/profile/user/wow/collections/pets"
        return await self.client.get_by_endpoint(endpoint, self._get_namespace())

    async def toys_collection_summary(self):
        endpoint = f"/profile/user/wow/collections/toys"
        return await self.client.get_by_endpoint(endpoint, self._get_namespace())

    async def heirlooms_collection_summary(self):
        endpoint = f"/profile/user/wow/collections/heirlooms"
        return await self.client.get_by_endpoint(endpoint, self._get_namespace())
