from asyncwowapi.api_client import ApiClient


class ReputationsAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def reputation_factions_index(self):
        endpoint = "/data/wow/reputation-faction/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def reputation_faction(self, reputationFactionId: int):
        endpoint = f"/data/wow/reputation-faction/{reputationFactionId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def reputation_tiers_index(self):
        endpoint = "/data/wow/reputation-tiers/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def reputation_tiers(self, reputationTiersId: int):
        endpoint = f"/data/wow/reputation-tiers/{reputationTiersId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
