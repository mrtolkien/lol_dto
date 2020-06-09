from typing import TypedDict, Dict, List, Optional

from lol_dto.classes.game.lol_game_event import LolGameKill
from lol_dto.classes.game.lol_game_team import LolGameTeam


class LolGame(TypedDict, total=False):
    """A dictionary representing a single League of Legends game.

    A TypedDict does not enforce any constraints and is here to raise linter warnings and enable auto-completion.
    """

    # The ['sources'] dictionary should have all information required to identify this game from a given source
    # A Riot API 'sources' dict looks like: {'riotLolApi': {'gameId': int, 'platformId': str}}
    sources: Dict[str, dict]

    # Time-related fields should be expressed in seconds, using floats for ms precision
    duration: int  # Expressed in seconds

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
    kills: List[LolGameKill]

    # Optional esports information
    tournament: Optional[str]  # Name of the tournament this game is a part of
    gameInSeries: Optional[int]  # Game index in the series including this game
    vod: Optional[str]  # VOD url

    # TODO Add a clean picks and bans representation for esports games with full information
    picks_bans: List
