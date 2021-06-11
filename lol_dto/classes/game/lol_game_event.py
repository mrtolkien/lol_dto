from abc import ABC
from dataclasses import dataclass, field
from typing import List, Optional

from lol_dto.classes.game.position import Position


@dataclass
class LolEvent(ABC):
    """
    A single event that took place during a LoL game
    """

    timestamp: float  # Timestamp of the event expressed in seconds from the game start, with possible ms precision

    # In the Riot API only champion kills and monster kills have a position associated to them
    # Cannot make it default to None as it creates issues with inheritance that are not worth the hassle
    position: Optional[Position]  # Position where the event took place


@dataclass
class LolGameKill(LolEvent):
    """
    A single kill in a LoL game
    """

    victimId: int  # Player getting killed
    assistsIds: List[int]  # Players getting an assist in the kill

    # All the id here refer to the id field in players objects
    # Player getting the last hit on the kill. None for executions
    killerId: int = None


@dataclass
class LolGameTeamEpicMonsterKill(LolEvent):
    """
    An epic monster kill for a team
    """

    killerId: int  # Refers to 'id' in players, represents the player landing the last hit
    # Players getting an assist in the monster kill, as shown in client (can be opponents)
    assistsIds: List[int]

    type: str  # 'DRAGON', 'BARON', 'RIFT_HERALD' as of 2021
    subType: str = None  # 'CLOUD', 'INFERNAL', 'MOUNTAIN', 'OCEAN', 'ELDER'


@dataclass
class LolGameTeamBuildingKill(LolEvent):
    """
    A building kill for a team
    """

    type: str  # 'TURRET', 'TURRET_PLATE', 'INHIBITOR'
    lane: str  # 'TOP', 'MID', 'BOT'
    side: str  # 'BLUE', 'RED' (the side it got killed in, technically redundant with team side)

    # Refers to 'id' in players, represents the player landing the last hit
    killerId: int = None
    assistsIds: List[int] = field(default_factory=list)

    towerLocation: str = (
        None  # 'OUTER', 'INNER', 'INHIBITOR', 'NEXUS', None for inhibitors
    )


@dataclass
class LolGamePlayerItemEvent(LolEvent):
    """
    An item-related event for a player

    Represents buying, selling, destroying, and undoing items
    """

    type: str  # 'PURCHASED', 'SOLD', 'UNDO', 'DESTROYED', 'USED', 'PICKED_UP'
    id: int  # Referring to Riot API item ID. Resulting item in case of an UNDO
    name: str  # Optional convenience field for human readability
    undoId: int = None  # Referring to the item that was undone in an UNDO event


@dataclass
class LolGamePlayerWardEvent(LolEvent):
    """
    A ward-related event for a player
    Represents placing and killing wards
    """

    type: str  # 'PLACED', 'KILLED'
    wardType: str  # Values in: YELLOW_TRINKET', 'CONTROL_WARD', 'SIGHT_WARD', 'YELLOW_TRINKET_UPGRADE', 'BLUE_TRINKET',
    #                                  'TEEMO_MUSHROOM', 'VISION_WARD', 'UNDEFINED'


@dataclass
class LolGamePlayerSkillLevelUpEvent(LolEvent):
    """
    A skill level up by a player
    """

    type: str  # 'NORMAL' or 'EVOLVE'
    slot: int  # The skill slot, from 1 to 4


@dataclass
class LolGamePlayerLargeMonsterKill(LolEvent):
    """
    A large monster kill by a player
    """

    killerId: int  # Refers to 'id' in players
    type: str  # 'BLUE_BUFF', 'RED_BUFF', 'RAPTOR', 'WOLF', 'KRUG', 'GROMP', 'SCUTTLE' as of 2021
