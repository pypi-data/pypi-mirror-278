from asyncwowapi.api_client import ApiClient


class AchievementAPI:

    def __init__(self, client: ApiClient):
        self.client = client
        self.namespace = 'static'

    async def achievement_categories_index(self):
        """
        :return: Returns an index of achievement categories.
        """

        endpoint = "/data/wow/achievement-category/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def achievement_category(self, achievement_category_id: int):
        """
        Returns an achievement category by ID.
        :param achievement_category_id: The ID of the achievement category.
        :return: Achievement category data.
        """

        endpoint = f"/data/wow/achievement-category/{achievement_category_id}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def achievements_index(self):
        """
        Returns an index of achievements.
        :return: Index of achievements.
        """

        endpoint = "/data/wow/achievement/index"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def achievement(self, achievement_id: int):
        """
        Returns an achievement by ID.
        :param achievement_id: The ID of the achievement.
        :return: Achievement data.
        """

        endpoint = f"/data/wow/achievement/{achievement_id}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])

    async def achievement_media(self, achievement_id: int):
        """
        Returns media for an achievement by ID.
        :param achievement_id: The ID of the achievement.
        :return: Media for the achievement.
        """

        endpoint = f"/data/wow/media/achievement/{achievement_id}"
        return await self.client.get_by_endpoint(endpoint, self.client.namespace['static'])
