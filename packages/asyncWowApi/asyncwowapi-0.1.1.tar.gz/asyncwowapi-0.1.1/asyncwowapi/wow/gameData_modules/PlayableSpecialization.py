from asyncwowapi.api_client import ApiClient


class PlayableSpecializationAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def playable_specializations_index(self):
        endpoint = "/data/wow/playable-specialization/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def playable_specialization(self, specId: int):
        endpoint = f"/data/wow/playable-specialization/{specId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def playable_specialization_media(self, specId: int):
        endpoint = f"/data/wow/media/playable-specialization/{specId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
