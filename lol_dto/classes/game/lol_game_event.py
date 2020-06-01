from typing import TypedDict, Optional, List

from lol_dto.classes.game.extra_classes import Position


class LolGameEvent(TypedDict, total=False):
    """A single event that took place during a LoL game.

    Should not be used as-is and is intended to be a building block for other event classes.
    """

    timestamp: float  # Timestamp of the event expressed in seconds from the game start, with possible ms precision

    # In the Riot API only champion kills and monster kills have a position associated to them
    position: Optional[Position]  # Position where the event took place


class LolGameKill(LolGameEvent):
    """A single kill in a LoL game
    """

    # All the id here refer to the id field in players objects
    killerId: int
    assistingParticipantIds: List[int]
    victimId: int


class LolGameTeamMonsterKill(LolGameEvent, total=False):
    """A monster kill for a team.
    """
    killerId: int  # Refers to 'id' in players, represents the player landing the last hit
    type: str  # 'DRAGON', 'NASHOR', 'RIFT_HERALD'
    subType: Optional[str]  # 'CLOUD', 'INFERNAL', 'MOUNTAIN', 'OCEAN', 'ELDER'


class LolGameTeamBuildingKill(LolGameEvent):
    """A building kill for a team.
    """
    # TODO Check that 'UNDEFINED_TURRET' are Azir turrets, and check 'FOUNTAIN_TURRET' events (very rare, old games).
    type: str  # 'TURRET', 'INHIBITOR'
    lane: str  # 'TOP', 'MID', 'BOT', None
    towerLocation: Optional[str]  # 'OUTER', 'INNER', 'INHIBITOR', 'NEXUS', None
    side: str  # 'BLUE', 'RED'


class LolGamePlayerItemEvent(LolGameEvent, total=False):
    """An item-related event for a player.

    Represents buying, selling, destroying, and undoing items.
    """

    # TODO See if "UNDO" needs specific fields
    type: str  # PURCHASED, SOLD, UNDO, DESTROYED
    id: int  # Referring to Riot API item ID. Resulting item in case of an UNDO
    undoId: Optional[int]  # Referring to the item that was undone in an UNDO event


class LolGamePlayerWardEvent(LolGameEvent):
    """A ward-related event for a player.

    Represents placing and killing wards.
    """

    type: str  # PLACED, KILLED
    wardType: str  # TODO Document possible ward types


class LolGamePlayerSkillEvent(LolGameEvent):
    """A skill level up by a player.
    """

    type: str  # NORMAL or ? TODO Search for level up types
    skillSlot: int  # The skill slot, from 1 to 4  TODO Is that the right name?

