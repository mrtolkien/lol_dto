from typing import TypedDict, Optional, List

from lol_dto.classes.game.position import Position


class LolEvent(TypedDict, total=False):
    """A single event that took place during a LoL game.

    Should not be used as-is and is intended to be a building block for other event classes.
    """

    timestamp: float  # Timestamp of the event expressed in seconds from the game start, with possible ms precision

    # In the Riot API only champion kills and monster kills have a position associated to them
    position: Optional[Position]  # Position where the event took place


class LolGameKill(LolEvent):
    """A single kill in a LoL game
    """

    # All the id here refer to the id field in players objects
    killerId: Optional[int]  # Player getting the last hit on the kill. None for executions.
    assistsIds: List[int]  # Players getting an assist in the kill
    victimId: int  # Player getting killed


class LolGameTeamMonsterKill(LolEvent, total=False):
    """A monster kill for a team.
    """

    killerId: int  # Refers to 'id' in players, represents the player landing the last hit
    type: str  # 'DRAGON', 'NASHOR', 'RIFT_HERALD'
    subType: Optional[str]  # 'CLOUD', 'INFERNAL', 'MOUNTAIN', 'OCEAN', 'ELDER'


class LolGameTeamBuildingKill(LolEvent, total=False):
    """A building kill for a team.
    """

    type: str  # 'TURRET', 'INHIBITOR'
    lane: str  # 'TOP', 'MID', 'BOT'
    side: str  # 'BLUE', 'RED'
    towerLocation: Optional[str]  # 'OUTER', 'INNER', 'INHIBITOR', 'NEXUS'


class LolGamePlayerItemEvent(LolEvent, total=False):
    """An item-related event for a player.

    Represents buying, selling, destroying, and undoing items.
    """

    type: str  # 'PURCHASED', 'SOLD', 'UNDO', 'DESTROYED'
    id: int  # Referring to Riot API item ID. Resulting item in case of an UNDO
    name: str  # Optional convenience field for human readability
    undoId: Optional[int]  # Referring to the item that was undone in an UNDO event


class LolGamePlayerWardEvent(LolEvent):
    """A ward-related event for a player.

    Represents placing and killing wards.
    """

    type: str  # 'PLACED', 'KILLED'
    wardType: str  # Values in: YELLOW_TRINKET', 'CONTROL_WARD', 'SIGHT_WARD', 'YELLOW_TRINKET_UPGRADE', 'BLUE_TRINKET',
    #                                  'TEEMO_MUSHROOM', 'VISION_WARD', 'UNDEFINED'


class LolGamePlayerSkillLevelUpEvent(LolEvent):
    """A skill level up by a player.
    """

    type: str  # 'NORMAL' or 'EVOLVE'
    slot: int  # The skill slot, from 1 to 4
