from asyncwowapi.api_client import ApiClient
from asyncwowapi.wow.gameData_modules import (
    AchievementAPI, AuctionHouseAPI, AzeriteEssenceAPI, ConnectedRealmAPI,
    CovenantAPI, CreatureAPI, GuildCrestAPI, HeirloomAPI, ItemAPI, JournalAPI,
    MediaSearchAPI, ModifiedCraftingAPI, MountAPI, MythicKeystoneAffixAPI,
    MythicKeystoneDungeonAPI, MythicKeystoneLeaderboardAPI, MythicRaidLeaderboardAPI,
    PetAPI, PlayableClassAPI, PlayableRaceAPI, PlayableSpecializationAPI, PowerTypeAPI,
    ProfessionAPI, PvPSeasonAPI, PvPTierAPI, QuestAPI, RealmAPI, RegionAPI,
    ReputationsAPI, SpellAPI, TalentAPI, TechTalentAPI, TitleAPI, ToyAPI, WoWTokenAPI
)


class WoWGameData(
    AuctionHouseAPI, AchievementAPI, AzeriteEssenceAPI, ConnectedRealmAPI,
    CovenantAPI, CreatureAPI, GuildCrestAPI, HeirloomAPI, ItemAPI, JournalAPI,
    MediaSearchAPI, ModifiedCraftingAPI, MountAPI, MythicKeystoneAffixAPI,
    MythicKeystoneDungeonAPI, MythicKeystoneLeaderboardAPI, MythicRaidLeaderboardAPI,
    PetAPI, PlayableClassAPI, PlayableRaceAPI, PlayableSpecializationAPI, PowerTypeAPI,
    ProfessionAPI, PvPSeasonAPI, PvPTierAPI, QuestAPI, RealmAPI, RegionAPI,
    ReputationsAPI, SpellAPI, TalentAPI, TechTalentAPI, TitleAPI, ToyAPI, WoWTokenAPI
):
    """
    The World of Warcraft game data APIs encompass both static and dynamic game data.
    """

    def __init__(self, client: ApiClient):
        super().__init__(client)
