from typing import TypedDict, List, Optional
from lol_dto.game.lol_game_team_player import LolGamePlayer


class LolGameTeamBan(TypedDict):
    """A single ban made by one of the teams.

    We have chosen to eschew the pickTurn field from the Riot API and simply rely on the list’s ordering.
    """

    championId: int  # Based on Riot API champion ID
    championName: Optional[str]  # Optional champion name for convenience


class LolGameTeam(TypedDict):
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

    # Bans should be ordered if the order has any meaning (it does not in solo queue as of 2020)
    # If players do a single champion ban, it should be a part of the player object.
    bans: Optional[List[LolGameTeamBan]]
