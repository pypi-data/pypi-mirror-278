from asyncwowapi.api_client import ApiClient


class MythicKeystoneLeaderboardAPI:

    def __init__(self, client: ApiClient):
        self.client = client


    async def keystone_leaderboards_index(self, connectedRealmId: int):
        endpoint = f"/data/wow/connected-realm/{connectedRealmId}/mythic-leaderboard/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])

    async def keystone_leaderboard(self, connectedRealmId: int, dungeonId: int, period: int):
        endpoint = f"/data/wow/connected-realm/{connectedRealmId}/mythic-leaderboard/{dungeonId}/period/{period}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])
