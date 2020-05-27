from typing import TypedDict


class Position(TypedDict):
    """A position on the LoL map.
    """

    # min: {x: -120, y: -120}
    # max: {x: 14870, y: 14980}
    x: int  # Horizontal distance from bottom left of the map
    y: int  # Vertical distance from bottom left of the map


class LolGameEvent(TypedDict):
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
    playerId: int  # Refers to the 'id' field in a player object. Refers to the player performing the event.

    # Currently, only champion kills and monster kills have a position associated to them
    position: Position  # Position where the event took place

    # Other fields can be created according to what is needed to describe the event
    # Expected fields can mirror Riot’s MatchEventDto for standard events types
