from asyncwowapi.api_client import ApiClient


class PowerTypeAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def power_types_index(self):
        endpoint = "/data/wow/power-type/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def power_type(self, powerTypeId: int):
        endpoint = f"/data/wow/power-type/{powerTypeId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
