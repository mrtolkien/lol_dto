from typing import TypedDict, Dict, List, Optional

from lol_dto.classes.game.lol_game_event import LolGameKill
from lol_dto.classes.game.lol_game_team import LolGameTeam


class LolPickBan(TypedDict):
    """A single pick or ban in a LoL game.

    'ban' and 'team' fields are required to account for possibly changing picks and bans formats.
    """

    championId: int
    championName: Optional[str]

    isBan: bool  # True if this represented a ban, False if this represented a pick
    team: str  # 'BLUE' or 'RED'


class LolGame(TypedDict, total=False):
    """
    A dictionary representing a single League of Legends game.

    As a TypedDict, it does not enforce any constraints but raises linter warnings and enables auto-completion.
    """

    # The ['sources'] dictionary should have all information necessary to identify the game for a given data source
    # Riot API example: {'riotLolApi': {'gameId': int, 'platformId': str}}
    sources: Dict[str, dict]

    # Time-related fields should be expressed in seconds, optionally using floats for ms precision
    duration: float  # Expressed in seconds

    # As JSON does not define a date format, we rely on ISO formatting
    start: str  # Expressed as ISO 8601 date and time with a seconds precision, for example "2020-05-27T02:23:02+00:00"

    # We allow information duplication here because many data sources only have patch information
    patch: str  # Patch should follow a simple XX.YY nomenclature and is the recommended field to use
    gameVersion: str  # The full game version expressed as XX.YY.ZZ.αα, allowing to distinguish micro patches

    # This is the only place where the game’s winner appears.
    # To know if a given player won, use player['team'] == game['winner']
    winner: str  # Equal to the winning team’s side

    # Team are a dictionary with keys equal to the team side ('BLUE' or 'RED')
    teams: Dict[str, LolGameTeam]

    # Kills involve multiple players from different teams and are therefore defined here
    kills: Optional[List[LolGameKill]]

    # Optional esports information
    tournament: Optional[str]  # Name of the tournament this game is a part of
    gameInSeries: Optional[int]  # Game index in the series including this game
    vod: Optional[str]  # VOD url
    picksBans: Optional[
        List[LolPickBan]
    ]  # Ordered list of picks and bans that happened in the game

    def __init__(self):
        super().__init__()
        ...
