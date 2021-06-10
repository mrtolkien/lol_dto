from dataclasses import dataclass, field
from typing import Dict, List

from lol_dto.classes.game.lol_game_event import LolGameKill
from lol_dto.classes.game.lol_game_team import LolGameTeam


@dataclass
class LolPickBan:
    """
    A single pick or ban in a LoL game

    'team' fields is used to account for possibly changing picks and bans formats but not crucial
    """

    championId: int
    isBan: bool  # True if this represents a ban, False if this represents a pick
    team: str  # 'BLUE' or 'RED'

    # Optional field for direct human use
    championName: str = None


@dataclass
class LolGameTeams:
    BLUE: LolGameTeam = field(default_factory=LolGameTeam)
    RED: LolGameTeam = field(default_factory=LolGameTeam)


@dataclass
class LolGame:
    """
    A class representing a single League of Legends game
    """

    # The sources attribute should have all information necessary to identify the game for a given data source
    # Riot API example: game.sources.riotLolApi.gameId, and game.sources.riotLolApi.platformId
    # Each parser transforming data to the LolGame format should implement its own source dataclass to allow for
    #   merging different sources
    sources: dataclass = None

    # Time-related fields should be expressed in seconds, optionally using floats for ms precision
    duration: float = None  # Expressed in seconds

    # As JSON does not define a date format, we rely on ISO formatting
    #   Expressed as ISO 8601 date and time with a seconds precision, for example "2020-05-27T02:23:02+00:00"
    start: str = None

    # We allow information duplication here because many data sources only have patch information
    patch: str = None  # Patch should follow a simple XX.YY nomenclature and is the recommended field to use
    gameVersion: str = None  # The full game version expressed as XX.YY.ZZ.αα, allowing to distinguish micro patches

    # This is the only place where the game’s winner appears.
    # To know if a given player won, use player['team'] == game['winner']
    winner: str = None  # Equal to the winning team’s side

    # Team are a dictionary with keys equal to the team side ('BLUE' or 'RED')
    teams: LolGameTeams = field(default_factory=LolGameTeams)

    # Kills involve multiple players from different teams and are therefore defined here
    kills: List[LolGameKill] = field(default_factory=list)

    # Optional game type

    # Optional esports information
    tournament: str = None  # Name of the tournament this game is a part of
    gameInSeries: int = None  # Game index in the series including this game
    vod: str = None  # VOD url

    # Ordered list of picks and bans
    picksBans: List[LolPickBan] = field(default_factory=list)
