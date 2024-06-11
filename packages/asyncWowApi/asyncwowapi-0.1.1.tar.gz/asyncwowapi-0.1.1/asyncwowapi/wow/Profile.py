from asyncwowapi.api_client import ApiClient
from asyncwowapi.wow.Profile_modules import (
    AccountProfileAPI, CharacterAchievementsAPI, CharacterAppearanceAPI, CharacterCollectionsAPI,
    CharacterEncountersAPI, CharacterEquipmentAPI, CharacterHunterPetsAPI, CharacterMediaAPI,
    CharacterMythicKeystoneProfileAPI, CharacterProfessionsAPI, CharacterProfileAPI, CharacterPvPAPI,
    CharacterQuestsAPI, CharacterReputationsAPI, CharacterSoulbindsAPI, CharacterSpecializationsAPI,
    CharacterStatisticsAPI, GuildAPI
)


class WoWProfile(AccountProfileAPI,
                 CharacterAchievementsAPI,
                 CharacterAppearanceAPI,
                 CharacterCollectionsAPI,
                 CharacterEncountersAPI,
                 CharacterEquipmentAPI,
                 CharacterHunterPetsAPI,
                 CharacterMediaAPI,
                 CharacterMythicKeystoneProfileAPI,
                 CharacterProfessionsAPI,
                 CharacterProfileAPI,
                 CharacterPvPAPI,
                 CharacterQuestsAPI,
                 CharacterReputationsAPI,
                 CharacterSoulbindsAPI,
                 CharacterSpecializationsAPI,
                 CharacterStatisticsAPI,
                 GuildAPI):
    """
    The World of Warcraft profile APIs listed below encompass profile game data.
    """

    def __init__(self, client: ApiClient):
        super().__init__(client)
