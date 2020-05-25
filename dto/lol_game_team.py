from typing import TypedDict, List

from lol.dto.lol_game_team_player import LolGameTeamPlayer


class LolGameTeamBan(TypedDict):
    championId: int
    championName: str  # Optional
    # TODO See if we add "pickTurn" or just rely on list index


class LolGameTeam(TypedDict):
    # All fields here refer to end of dto statistics
    riftHeraldKills: int
    dragonKills: int
    baronKills: int

    towerKills: int
    inhibitorKills: int

    # This is technically redundant with events, but many games have this info without events
    firstBlood: bool
    firstTower: bool
    firstRiftHerald: bool
    firstDragon: bool
    firstBaron: bool

    players: List[LolGameTeamPlayer]
    bans: List[LolGameTeamBan]
