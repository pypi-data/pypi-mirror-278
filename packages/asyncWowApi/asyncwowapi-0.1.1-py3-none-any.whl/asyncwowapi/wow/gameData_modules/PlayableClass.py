from asyncwowapi.api_client import ApiClient


class PlayableClassAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def playable_classes_index(self):
        endpoint = "/data/wow/playable-class/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def playable_class(self, classId: int):
        endpoint = f"/data/wow/playable-class/{classId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def playable_class_media(self, playableClassId: int):
        endpoint = f"/data/wow/media/playable-class/{playableClassId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def pvp_talent_slots(self, classId: int):
        endpoint = f"/data/wow/playable-class/{classId}/pvp-talent-slots"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
