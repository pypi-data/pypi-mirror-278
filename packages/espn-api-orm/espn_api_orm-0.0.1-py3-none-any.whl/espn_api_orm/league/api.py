import datetime

from espn_api_orm.consts import ESPNSportTypes, FIRST_SEASON
from espn_api_orm.generic.schema import BaseType
from espn_api_orm.league.schema import League
from espn_api_orm.sport.api import ESPNSportAPI


class ESPNLeagueAPI(ESPNSportAPI):
    """
    ESPN League API for retrieving sport information about a specific league.

    Attributes:

    Methods:
    """

    def __init__(self, sport: ESPNSportTypes, league: str):
        """
        Initialize ESPNSportAPI.
        """
        super().__init__(sport)
        self.league = league

    def get_league(self):
        return League(**self.api_request(f"{self._core_url}/{self.sport.value}/leagues/{self.league}"))

    def get_seasons(self, return_values=True):
        res = BaseType(**self.api_request(f"{self._core_url}/{self.sport.value}/leagues/{self.league}/seasons?limit=200"))
        if not return_values:
            return res
        return [int(i) for i in self._get_values(f"{self._core_url}/{self.sport.value}/leagues/{self.league}/seasons", res.items) if int(i) > FIRST_SEASON]

    def get_first_season(self, return_values):
        return min(self.get_seasons(return_values=return_values))

    def get_current_season(self, return_values):
        return max(self.get_seasons(return_values=return_values))

    def is_active(self):
        try:
            season = self.get_current_season(return_values=True)
            reg_res = self.api_request(f"{self._core_url}/{self.sport.value}/leagues/{self.league}/seasons/{season}")
            start_date = datetime.datetime.strptime(reg_res['startDate'], '%Y-%m-%dT%H:%MZ')
            end_date = datetime.datetime.strptime(reg_res['endDate'], '%Y-%m-%dT%H:%MZ')
            return start_date <= datetime.datetime.now() <= end_date
        except Exception as e:
            print(e)
            return False

    def get_franchises(self, return_values=True):
        res = BaseType(**self.api_request(f"{self._core_url}/{self.sport.value}/leagues/{self.league}/franchises?limit=1000"))
        if not return_values:
            return res
        return [int(i) for i in self._get_values(f"{self._core_url}/{self.sport.value}/leagues/{self.league}/franchises", res.items)]

    def get_odds_providers(self, return_values=True):
        res = BaseType(**self.api_request(f"{self._core_url}/{self.sport.value}/leagues/{self.league}/providers?limit=1000"))
        if not return_values:
            return res
        return [int(i) for i in self._get_values(f"{self._core_url}/{self.sport.value}/leagues/{self.league}/providers", res.items)]


