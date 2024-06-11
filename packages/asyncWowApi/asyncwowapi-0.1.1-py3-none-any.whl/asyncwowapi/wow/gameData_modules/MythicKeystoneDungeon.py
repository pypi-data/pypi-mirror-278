from asyncwowapi.api_client import ApiClient


class MythicKeystoneDungeonAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def keystone_dungeons_index(self):
        endpoint = "/data/wow/mythic-keystone/dungeon/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])

    async def keystone_dungeon(self, dungeonId: int):
        endpoint = f"/data/wow/mythic-keystone/dungeon/{dungeonId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])

    async def keystone_index(self):
        endpoint = "/data/wow/mythic-keystone/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])

    async def keystone_periods_index(self):
        endpoint = "/data/wow/mythic-keystone/period/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])

    async def keystone_period(self, periodId: int):
        endpoint = f"/data/wow/mythic-keystone/period/{periodId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])

    async def keystone_seasons_index(self):
        endpoint = "/data/wow/mythic-keystone/season/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])

    async def keystone_season(self, seasonId: int):
        endpoint = f"/data/wow/mythic-keystone/season/{seasonId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])
