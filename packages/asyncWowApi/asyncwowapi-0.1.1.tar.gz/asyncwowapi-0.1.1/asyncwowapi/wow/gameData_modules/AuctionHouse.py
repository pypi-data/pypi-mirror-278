from asyncwowapi.api_client import ApiClient


class AuctionHouseAPI:

    def __init__(self, client: ApiClient):
        self.client = client


    async def auctions(self, connectedRealmId: int):
        """
        See the Connected Realm API for information about retrieving a list of connected realm IDs.
        Auction house data updates at a set interval. The value was initially set at 1 hour; however,
        it might change over time without notice.
        Depending on the number of active auctions on the specified connected realm,
        the response from this endpoint may be rather large, sometimes exceeding 10 MB.

        :param connectedRealmId: The ID of the connected realm.
        :return: Returns all active auctions for a connected realm.
        """

        endpoint = f"/data/wow/connected-realm/{connectedRealmId}/auctions"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])

    async def commodities(self):
        """
        Auction house data updates at a set interval. The value was initially set at 1 hour; however,
        it might change over time without notice.
        Depending on the number of active auctions on the specified connected realm, the response from this endpoint may be rather large,
        sometimes exceeding 10 MB.
        :return: Returns all active auctions for commodity items for the entire game region.
        """

        endpoint = f"/data/wow/auctions/commodities"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['dynamic'])
