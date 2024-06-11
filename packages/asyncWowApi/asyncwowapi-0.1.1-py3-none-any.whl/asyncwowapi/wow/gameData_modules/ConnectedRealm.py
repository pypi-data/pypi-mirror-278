from asyncwowapi.api_client import ApiClient


class ConnectedRealmAPI:

    def __init__(self, client: ApiClient):
        self.client = client


    async def connected_realms_index(self):
        """
        :return: Returns an index of connected realms.
        """
        endpoint = "/data/wow/connected-realm/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])

    async def connected_realm(self, connectedRealmId: int):
        """
        :param connectedRealmId: The ID of the connected realm.
        :return: Returns a connected realm by ID.
        """
        endpoint = f"/data/wow/connected-realm/{connectedRealmId}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])

    async def connected_realms_search(self, query_params: dict):
        """
        Performs a search of connected realms. The fields below are provided for example.
        For more detail see the Search Guide.
        https://develop.battle.net/documentation/world-of-warcraft/guides/search
        Args:
            query_params (dict): A dictionary of query parameters to filter the search results.
            The following fields are examples of the parameters that can be used:
                - region (str): REQUIRED. The region of the data to retrieve (e.g., 'us').
                - namespace (str): REQUIRED. The namespace to use to locate this document (e.g., 'dynamic-us').
                - status.type (str): The status of the connected realm, 'UP' or 'DOWN'.
                - realms.timezone (str): The timezone of the realm (e.g., 'America/New_York').
                - orderby (str): The field to sort the result set by (e.g., 'id').
                - _page (int): The result page number (e.g., 1).
        :return:
        """
        endpoint = "/data/wow/search/connected-realm"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'], params=query_params)
