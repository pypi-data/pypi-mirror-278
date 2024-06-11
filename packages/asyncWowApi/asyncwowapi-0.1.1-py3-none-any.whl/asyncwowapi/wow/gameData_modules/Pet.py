from asyncwowapi.api_client import ApiClient


class PetAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def pets_index(self):
        endpoint = "/data/wow/pet/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def pet(self, petId: int):
        endpoint = f"/data/wow/pet/{petId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def pet_media(self, petId: int):
        endpoint = f"/data/wow/media/pet/{petId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def pet_abilities_index(self):
        endpoint = "/data/wow/pet-ability/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def pet_ability(self, petAbilityId: int):
        endpoint = f"/data/wow/pet-ability/{petAbilityId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def pet_ability_media(self, petAbilityId: int):
        endpoint = f"/data/wow/media/pet-ability/{petAbilityId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
