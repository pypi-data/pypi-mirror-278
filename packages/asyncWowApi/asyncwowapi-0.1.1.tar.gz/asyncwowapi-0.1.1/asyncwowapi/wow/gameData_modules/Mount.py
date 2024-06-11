from asyncwowapi.api_client import ApiClient


class MountAPI:

    def __init__(self, client: ApiClient):
        self.client = client


    async def mounts_index(self):
        endpoint = "/data/wow/mount/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def mount(self, mountId: int):
        endpoint = f"/data/wow/mount/{mountId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def mount_search(self, query: str):
        endpoint = f"/data/wow/search/mount?name={query}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
