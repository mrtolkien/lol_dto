from typing import TypedDict, List, Optional

from lol_dto.classes.game.lol_game_event import LolGameTeamMonsterKill, LolGameTeamBuildingKill
from lol_dto.classes.game.lol_game_player import LolGamePlayer


class LolGameTeam(TypedDict, total=False):
    """One of the two teams taking part in a LoL game.

    The key referring to this object is what defines its side.
    """

    # End of game statistics
    riftHeraldKills: int  # Total rift herald kills
    dragonKills: int  # Total dragon kills
    baronKills: int  # Total baron kills

    # Because towers can be killed by minions, those fields are not redundant with player['towerKills']
    towerKills: int  # Total tower kills
    inhibitorKills: int  # Total inhibitor kills

    # First blood is associated to players and not teams
    # Structure kills need to be related to team as they can be killed by minions
    firstTower: bool  # True if the team killed the first tower
    firstInhibitor: bool  # True if the team killed the first inhibitor

    # Object kills are linked to teams as it makes little sense to link them to individual players
    firstRiftHerald: bool  # True if the team killed the first Rift Herald
    firstDragon: bool  # True if the team killed the first Dragon
    firstBaron: bool  # True if the team killed the first Nashor

    # Players are defined as a simple list as no obvious key emerges
    players: List[LolGamePlayer]

    # Team-related bans are a list of champions that were banned by players on the team
    bans: Optional[List[int]]  # List of champion IDs
    bansNames: Optional[List[str]]  # List of champion names for human readability

    # Team monsters kills
    monstersKills: List[LolGameTeamMonsterKill]

    # Team buildings kills
    buildingsKills: List[LolGameTeamBuildingKill]

    # TODO Add esports fields (name, trigram, ...)
