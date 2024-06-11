from asyncwowapi.api_client import ApiClient


class GuildAPI:
    def __init__(self, client: ApiClient):
        self.client = client

    async def guild_summary(self, realm_slug: str, guild_name_slug: str):
        endpoint = f"/data/wow/guild/{realm_slug}/{guild_name_slug}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])

    async def guild_activity(self, realm_slug: str, guild_name_slug: str):
        endpoint = f"/data/wow/guild/{realm_slug}/{guild_name_slug}/activity"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])

    async def guild_achievements(self, realm_slug: str, guild_name_slug: str):
        endpoint = f"/data/wow/guild/{realm_slug}/{guild_name_slug}/achievements"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])

    async def guild_roster(self, realm_slug: str, guild_name_slug: str):
        endpoint = f"/data/wow/guild/{realm_slug}/{guild_name_slug}/roster"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['profile'])
