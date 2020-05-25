from typing import TypedDict, Dict, List

from lol.dto.lol_game_event import LolGameEvent
from lol.dto.lol_game_team import LolGameTeam


class LolGame(TypedDict):
    # Fields that are related to a specific data source should be prefaced by its name
    riotId: str  # gameId in Riot’s API
    riotServer: str  # platformId in Riot’s API

    # Example of esports information
    leaguepediaId: str
    leaguepediaTournament: str
    gameInSeries: int
    vod_url: str

    # Fields independent of the data source
    duration: int  # expressed in seconds
    startDate: str  # expressed as ISO 8601 date
    gameVersion: str  # Raw dto version or patch? TODO

    winner: str  # equal to the winning team’s side (blue or red as of 2020)

    # TODO Ask about this design against a list of teams/players directly children of LolGame
    # Team are a dictionary with keys equal to the team side
    teams: Dict[str, LolGameTeam]

    # Events are currently a simple list as no obvious key arises (multiple events can have the same timestamp)
    events: List[LolGameEvent]
