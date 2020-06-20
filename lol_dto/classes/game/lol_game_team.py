from typing import TypedDict, List, Optional, Dict

from lol_dto.classes.game.lol_game_event import LolGameTeamMonsterKill, LolGameTeamBuildingKill
from lol_dto.classes.game.lol_game_player import LolGamePlayer


class LolGameTeamEndOfGameStats(TypedDict, total=False):
    """End of game stats pertaining the whole team.
    """
    # Structure kills need to be related to team as they can be killed by minions
    towerKills: int  # Total tower kills
    inhibitorKills: int  # Total inhibitor kills

    firstTower: bool  # True if the team killed the first tower
    firstInhibitor: bool  # True if the team killed the first inhibitor

    # Epic monsters kills are linked to teams as it makes little sense to link them to individual players
    riftHeraldKills: int  # Total rift herald kills
    dragonKills: int  # Total dragon kills
    baronKills: int  # Total baron kills

    firstRiftHerald: bool  # True if the team killed the first Rift Herald
    firstDragon: bool  # True if the team killed the first Dragon
    firstBaron: bool  # True if the team killed the first Nashor


class LolGameTeam(TypedDict, total=False):
    """One of the two teams taking part in a LoL game.

    The key referring to this object is what defines its side.
    """

    # Players are defined as a simple list as no obvious key emerges
    players: List[LolGamePlayer]

    # Team-related bans are a list of champions that were banned by players on the team
    bans: Optional[List[int]]  # List of champion IDs
    bansNames: Optional[List[str]]  # List of champion names for human readability

    # End of game stats
    endOfGameStats: LolGameTeamEndOfGameStats

    # Team monsters kills
    monstersKills: List[LolGameTeamMonsterKill]

    # Team buildings kills
    buildingsKills: List[LolGameTeamBuildingKill]

    # Esports-specific fields
    name: Optional[str]  # The actual name of the team (T1, Fnatic, TSM, ...)
    uniqueIdentifiers: Dict[str, dict]
