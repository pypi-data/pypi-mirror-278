from asyncwowapi.api_client import ApiClient


class AzeriteEssenceAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def azerite_essences_index(self):
        """
        :return: Returns an index of azerite essences.
        """
        endpoint = "/data/wow/azerite-essence/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def azerite_essence(self, azeriteEssenceId: int):
        """
        :param azeriteEssenceId: The ID of the azerite essence.
        :return: Returns an azerite essence by ID.
        """
        endpoint = f"/data/wow/azerite-essence/{azeriteEssenceId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def azerite_essence_search(self):
        """
        Performs a search of azerite essences. The fields below are provided for example.
        For more detail see the Search Guide.
        https://develop.battle.net/documentation/world-of-warcraft/guides/search
        :return:
        """
        endpoint = "/data/wow/search/azerite-essence"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def azerite_essence_media(self, azeriteEssenceId: int):
        """
        :param azeriteEssenceId: The ID of the azerite essence.
        :return: Returns media for an azerite essence by ID.
        """
        endpoint = f"/data/wow/media/azerite-essence/{azeriteEssenceId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
