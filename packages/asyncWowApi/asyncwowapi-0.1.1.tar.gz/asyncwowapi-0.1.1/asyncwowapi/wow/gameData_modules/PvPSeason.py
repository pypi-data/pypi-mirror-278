from asyncwowapi.api_client import ApiClient


class PvPSeasonAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def pvp_seasons_index(self):
        endpoint = "/data/wow/pvp-season/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])

    async def pvp_season(self, pvpSeasonId: int):
        endpoint = f"/data/wow/pvp-season/{pvpSeasonId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])

    async def pvp_leaderboards_index(self, pvpSeasonId: int):
        endpoint = f"/data/wow/pvp-season/{pvpSeasonId}/pvp-leaderboard/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])

    async def pvp_leaderboard(self, pvpSeasonId: int, pvpBracket: str):
        endpoint = f"/data/wow/pvp-season/{pvpSeasonId}/pvp-leaderboard/{pvpBracket}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])

    async def pvp_rewards_index(self, pvpSeasonId: int):
        endpoint = f"/data/wow/pvp-season/{pvpSeasonId}/pvp-reward/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])
