from typing import Optional, List

from espn_api_orm.generic.api import ESPNBaseAPI
from espn_api_orm.consts import ESPNSportTypes, ESPNSportSeasonTypes
from espn_api_orm.league.api import ESPNLeagueAPI
from espn_api_orm.scoreboard.api import ESPNScoreboardAPI
from espn_api_orm.scoreboard.schema import Scoreboard, Event


class ESPNEventAPI(ESPNScoreboardAPI):
    """
    ESPN Event API for retrieving sports events information.

    Attributes:
        SCHEMA (dict): Dictionary defining the data schema for events.

    Methods:
        get_event(): Retrieve event data for a specific sport.
        get_summary(): Retrieve game summary data.
        get_plays(): Retrieve play-by-play data.
        get_play_probabilities(): Retrieve play probabilities data.
        get_linescores(team_id): Retrieve linescores data.
        get_scoring_and_splits(team_id): Retrieve scoring and splits data.
        get_roster(team_id): Retrieve roster data (starters).
        get_game_officials(): Retrieve game officials/judges data.
        get_power_index(team_id): Retrieve expected margin of victory and predicted win percentage data.

    """

    def __init__(self, sport: ESPNSportTypes, league: str, event_id: int):
        """
        Initialize ESPNScoreboardAPI.
        """
        super().__init__(sport, league)
        self.event_id = event_id

    def get_event(self):
        url = f"{self._base_url}/{self.sport.value}/{self.league}/scoreboard/{self.event_id}"
        return Event(**self.api_request(url))

    def get_summary(self):
        url = f"{self._base_url}/{self.sport.value}/{self.league}/summary?event={self.event_id}"
        return self.api_request(url)

    def get_prediction(self, limit:int=1000) :
        url = f"{self._core_url}/{self.sport.value}/leagues/{self.league}/events/{self.event_id}/competitions/{self.event_id}/predictor?limit={limit}"
        return self.api_request(url)

    def get_odds(self, provider_id: int,limit:int=1000) :
        url = f"{self._core_url}/{self.sport.value}/leagues/{self.league}/events/{self.event_id}/competitions/{self.event_id}/odds/{provider_id}?limit={limit}"
        return self.api_request(url)

    def get_plays(self, limit:int=1000):
        url = f"{self._core_url}/{self.sport.value}/leagues/{self.league}/events/{self.event_id}/competitions/{self.event_id}/plays?limit={limit}"
        return self.api_request(url)

    def get_play_probabilities(self, limit:int=1000):
        url = f"{self._core_url}/{self.sport.value}/leagues/{self.league}/events/{self.event_id}/competitions/{self.event_id}/probabilities?limit={limit}"
        return self.api_request(url)

    def get_linescores(self, team_id):
        url = f"{self._core_url}/{self.sport.value}/leagues/{self.league}/events/{self.event_id}/competitions/{self.event_id}/competitors/{team_id}/linescores"
        return self.api_request(url)

    def get_team_statistics(self, team_id):
        url = f"{self._core_url}/{self.sport.value}/leagues/{self.league}/events/{self.event_id}/competitions/{self.event_id}/competitors/{team_id}/statistics"
        return self.api_request(url)

    def get_roster(self, team_id):
        url = f"{self._core_url}/{self.sport.value}/leagues/{self.league}/events/{self.event_id}/competitions/{self.event_id}/competitors/{team_id}/roster"
        return self.api_request(url)

    def get_game_officials(self):
        url = f"{self._core_url}/{self.sport.value}/leagues/{self.league}/events/{self.event_id}/competitions/{self.event_id}/officials"
        return self.api_request(url)

    def get_power_index(self, team_id):
        url = f"{self._core_url}/{self.sport.value}/leagues/{self.league}/events/{self.event_id}/competitions/{self.event_id}/powerindex/{team_id}"
        return self.api_request(url)

