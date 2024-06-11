from asyncwowapi.api_client import ApiClient


class RealmAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def realms_index(self):
        endpoint = "/data/wow/realm/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])

    async def realm(self, realmSlug: str):
        endpoint = f"/data/wow/realm/{realmSlug}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])

    async def realm_search(self, query: str):
        endpoint = f"/data/wow/search/realm?name={query}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])
