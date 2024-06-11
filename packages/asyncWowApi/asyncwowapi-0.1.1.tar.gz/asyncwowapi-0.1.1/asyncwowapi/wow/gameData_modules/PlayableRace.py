from asyncwowapi.api_client import ApiClient


class PlayableRaceAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def playable_races_index(self):
        endpoint = "/data/wow/playable-race/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def playable_race(self, playableRaceId: int):
        endpoint = f"/data/wow/playable-race/{playableRaceId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
