from typing import TypedDict, Optional, List

from lol_dto.game.extra_classes import Position, Building, Monster


class LolGameEvent(TypedDict, total=False):
    """A single event that took place during a LoL game.

    'timestamp', 'type', 'playerId', and 'position' should be present for almost all events.

    Other fields can be added as needed depending on the event type. By default, follow the Riot API nomenclature.
    """

    # Timestamps cannot be a primary key as multiple events can have the same timestamp
    timestamp: float  # Timestamp of the event expressed in seconds from the game start, with possible ms precision

    # Event types are mostly copied from Riot’s API but not constrained to an Enum to allow for new types of events
    # Usual values are CHAMPION_KILL, WARD_PLACED, WARD_KILL, BUILDING_KILL, ELITE_MONSTER_KILL, ITEM_PURCHASED,
    #       ITEM_SOLD, ITEM_DESTROYED, ITEM_UNDO, SKILL_LEVEL_UP
    type: str  # Event type

    # TODO This is the most contentious field, currently heavily based on Riot’s structure
    # PlayerId can be null for executions and buildings dying to minions in particular
    playerId: Optional[int]  # Refers to the 'id' field in a player object. Refers to the player performing the event.

    # Currently, only champion kills and monster kills have a position associated to them
    position: Optional[Position]  # Position where the event took place

    # Other fields can be created according to what is needed to describe the event
    itemId: Optional[int]  # Refer to Riot API item IDs. A simple int as we don’t need other info here
    itemIdBeforeUndo: Optional[int]  # For items undo
    itemIdAfterUndo: Optional[int]  # For items undo

    victimId: Optional[int]  # Refers to the player’s id field
    assistingParticipantIds: Optional[List[int]]  # Only filled for kills

    skillSlot: Optional[int]  # 1 to 4
    levelUpType: Optional[str]  # Used for Kha Zix and Kai’Sa evolutions. NORMAL most of the time.

    # Objectives have their own DTO for easier parsing
    building: Optional[Building]
    monster: Optional[Monster]
