from asyncwowapi.api_client import ApiClient


class PvPTierAPI:

    def __init__(self, client: ApiClient):
        self.client = client


    async def pvp_tiers_index(self):
        endpoint = "/data/wow/pvp-tier/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def pvp_tier(self, pvpTierId: int):
        endpoint = f"/data/wow/pvp-tier/{pvpTierId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def pvp_tier_media(self, pvpTierId: int):
        endpoint = f"/data/wow/media/pvp-tier/{pvpTierId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
