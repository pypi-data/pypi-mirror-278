from asyncwowapi.api_client import ApiClient


class MythicRaidLeaderboardAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def mythic_raid_leaderboard(self, raid: str, faction: str):
        endpoint = f"/data/wow/leaderboard/hall-of-fame/{raid}/{faction}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])
