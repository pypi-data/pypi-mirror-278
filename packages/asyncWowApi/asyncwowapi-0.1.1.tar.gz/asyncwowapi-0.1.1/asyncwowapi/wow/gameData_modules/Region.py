from asyncwowapi.api_client import ApiClient


class RegionAPI:

    def __init__(self, client: ApiClient):
        self.client = client


    async def regions_index(self):
        endpoint = "/data/wow/region/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])

    async def region(self, regionId: int):
        endpoint = f"/data/wow/region/{regionId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])
