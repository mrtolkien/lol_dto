from dataclasses import dataclass, field
from typing import List, Optional, Dict

from lol_dto.classes.game.lol_game_event import (
    LolGameTeamEpicMonsterKill,
    LolGameTeamBuildingKill,
)
from lol_dto.classes.game.lol_game_player import LolGamePlayer
from lol_dto.classes.sources.empty_dataclass import EmptyDataclass


@dataclass
class LolGameTeamEndOfGameStats:
    """
    End of game stats pertaining the whole team
    """

    # Structure kills need to be related to team as they can be killed by minions
    turretKills: int = None  # Total turret kills
    inhibitorKills: int = None  # Total inhibitor kills

    firstTurret: bool = None  # True if the team killed the first turret
    firstInhibitor: bool = None  # True if the team killed the first inhibitor

    # Epic monsters kills are linked to teams as it makes little sense to link them to individual players
    riftHeraldKills: int = None  # Total rift herald kills
    dragonKills: int = None  # Total dragon kills
    baronKills: int = None  # Total baron kills

    firstRiftHerald: bool = None  # True if the team killed the first Rift Herald
    firstDragon: bool = None  # True if the team killed the first Dragon
    firstBaron: bool = None  # True if the team killed the first Nashor


@dataclass
class LolGameTeam:
    """
    One of the two teams taking part in a LoL game

    It's side is defined by the attribute name: teams.BLUE and teams.RED
    """

    # Players are defined as a simple list as no obvious key emerges
    players: List[LolGamePlayer] = field(default_factory=list)

    # Team-related bans are a list of champions that were banned by players on the team
    bans: Optional[List[int]] = field(default_factory=list)  # List of champion IDs
    # List of champion names for human readability
    bansNames: Optional[List[str]] = field(default_factory=list)

    # End of game stats
    endOfGameStats: LolGameTeamEndOfGameStats = None

    # Team monsters kills
    epicMonstersKills: List[LolGameTeamEpicMonsterKill] = field(default_factory=list)

    # Team buildings kills
    buildingsKills: List[LolGameTeamBuildingKill] = field(default_factory=list)

    # Esports-specific identifiers
    sources: dataclass = field(default_factory=EmptyDataclass)
