from asyncwowapi.api_client import ApiClient


class GuildCrestAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    def _get_namespace(self) -> str:
        return f"static-{self.client.region}"

    async def guild_crest_components_index(self):
        endpoint = "/data/wow/guild-crest/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def guild_crest_border_media(self, borderId: int):
        endpoint = f"/data/wow/media/guild-crest/border/{borderId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def guild_crest_emblem_media(self, emblemId: int):
        endpoint = f"/data/wow/media/guild-crest/emblem/{emblemId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
