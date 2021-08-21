from dataclasses import dataclass, field
from typing import List

from lol_dto.classes.game.lol_game_event import LolGameKill
from lol_dto.classes.game.lol_game_team import LolGameTeam
from lol_dto.classes.sources.empty_dataclass import EmptyDataclass

from lol_dto.names_helper.name_classes import ChampionNameClass


@dataclass
class LolPickBan(ChampionNameClass):
    """
    A single pick or ban in a LoL game

    'team' fields is used to account for possibly changing picks and bans formats but not crucial
    """

    championId: int
    isBan: bool  # True if this represents a ban, False if this represents a pick
    team: str  # 'BLUE' or 'RED'


@dataclass
class LolGameTeams:
    BLUE: LolGameTeam = field(default_factory=LolGameTeam)
    RED: LolGameTeam = field(default_factory=LolGameTeam)

    def __iter__(self):
        for t in self.BLUE, self.RED:
            yield t


@dataclass
class LolGamePause:
    # ISO datetime
    realTimestamp: str
    type: str


@dataclass
class LolGame:
    """
    A class representing a single League of Legends game
    """

    # The sources attribute should have all information necessary to identify the game for a given data source
    # Riot API example: game.sources.riotLolApi.gameId, and game.sources.riotLolApi.platformId
    # Each parser transforming data to the LolGame format should implement its own source dataclass to allow for
    #   merging different sources
    # Esports data about the tournament or league name should be linked to a source as it is hard to define a single
    #   source of truth for it
    sources: dataclass = field(default_factory=EmptyDataclass)

    # Time-related fields should be expressed in seconds, optionally using floats for ms precision
    duration: float = None  # Expressed in seconds

    # As JSON does not define a date format, we rely on ISO formatting
    #   Expressed as ISO 8601 date and time with a seconds precision, for example "2020-05-27T02:23:02+00:00"
    start: str = None

    # match-v5 makes a difference between game creation and game start, so we have a secondary field
    creation: str = None

    # Those metadata fields are there to represent data from match-v5 objects
    type: str = None
    queue_id: int = None

    # We allow information duplication here because many data sources only have patch information
    patch: str = None  # Patch should follow a simple XX.YY nomenclature and is the recommended field to use
    gameVersion: str = None  # The full game version expressed as XX.YY.ZZ.αα, allowing to distinguish micro patches

    # This is the only place where the game’s winner appears
    winner: str = None  # BLUE or RED

    # Team are a dictionary with keys equal to the team side ('BLUE' or 'RED')
    teams: LolGameTeams = field(default_factory=LolGameTeams)

    # Kills involve multiple players from different teams and are therefore defined here
    kills: List[LolGameKill] = field(default_factory=list)

    # Game lobby name, appearing amongst other in match-v5
    lobbyName: str = None

    # Optional esports information
    gameInSeries: int = None  # Game index in the series including this game
    vod: str = None  # VOD url

    # Ordered list of picks and bans
    picksBans: List[LolPickBan] = field(default_factory=list)

    # List of pause events that happened in the game
    pauses: List[LolGamePause] = field(default_factory=list)

    def __post_init__(self):
        """
        Post init function to define a backref in children needing access to the patch to find object names
        """
        for team in self.teams:
            setattr(team, "game", self)

        for pb in self.picksBans:
            setattr(pb, "game", self)
