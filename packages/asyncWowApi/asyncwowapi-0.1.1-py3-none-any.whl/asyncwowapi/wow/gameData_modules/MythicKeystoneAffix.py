from asyncwowapi.api_client import ApiClient


class MythicKeystoneAffixAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def keystone_affixes_index(self):
        endpoint = "/data/wow/keystone-affix/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def keystone_affix(self, keystoneAffixId: int):
        endpoint = f"/data/wow/keystone-affix/{keystoneAffixId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def keystone_affix_media(self, keystoneAffixId: int):
        endpoint = f"/data/wow/media/keystone-affix/{keystoneAffixId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
