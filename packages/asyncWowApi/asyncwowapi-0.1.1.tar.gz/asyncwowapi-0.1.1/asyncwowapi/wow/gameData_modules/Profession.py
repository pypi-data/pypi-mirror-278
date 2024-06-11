from asyncwowapi.api_client import ApiClient


class ProfessionAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def professions_index(self):
        endpoint = "/data/wow/profession/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def profession(self, professionId: int):
        endpoint = f"/data/wow/profession/{professionId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def profession_media(self, professionId: int):
        endpoint = f"/data/wow/media/profession/{professionId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def profession_skill_tier(self, professionId: int, skillTierId: int):
        endpoint = f"/data/wow/profession/{professionId}/skill-tier/{skillTierId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def recipe(self, recipeId: int):
        endpoint = f"/data/wow/recipe/{recipeId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def recipe_media(self, recipeId: int):
        endpoint = f"/data/wow/media/recipe/{recipeId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
