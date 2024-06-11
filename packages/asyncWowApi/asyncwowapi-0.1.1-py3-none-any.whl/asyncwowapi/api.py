from asyncwowapi.api_client import ApiClient
from asyncwowapi.wow import WoWGameData
from asyncwowapi.wow import WoWProfile


class Api:
    """
    World of Warcraft provides APIs to access data for such things as player profiles, realms, achievements and other game information.
    """
    def __init__(self, client: ApiClient):
        self.wow = self.WoW(client)

    class WoW:
        def __init__(self, client):
            self.game_data = WoWGameData(client)
            self.profile = WoWProfile(client)
