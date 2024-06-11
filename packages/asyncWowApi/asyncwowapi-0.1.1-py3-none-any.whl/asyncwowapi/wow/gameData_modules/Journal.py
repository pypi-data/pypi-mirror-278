from asyncwowapi.api_client import ApiClient


class JournalAPI:

    def __init__(self, client: ApiClient):
        self.client = client


    async def journal_expansions_index(self):
        endpoint = "/data/wow/journal-expansion/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def journal_expansion(self, journalExpansionId: int):
        endpoint = f"/data/wow/journal-expansion/{journalExpansionId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def journal_encounters_index(self):
        endpoint = "/data/wow/journal-encounter/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def journal_encounter(self, journalEncounterId: int):
        endpoint = f"/data/wow/journal-encounter/{journalEncounterId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def journal_encounter_search(self, query: str):
        endpoint = f"/data/wow/search/journal-encounter?name={query}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def journal_instances_index(self):
        endpoint = "/data/wow/journal-instance/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def journal_instance(self, journalInstanceId: int):
        endpoint = f"/data/wow/journal-instance/{journalInstanceId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def journal_instance_media(self, journalInstanceId: int):
        endpoint = f"/data/wow/media/journal-instance/{journalInstanceId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
