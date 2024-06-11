from asyncwowapi.api_client import ApiClient


class MediaSearchAPI:

    def __init__(self, client: ApiClient):
        self.client = client

    async def media_search(self, query: str):
        endpoint = f"/data/wow/search/media?name={query}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
