from typing import TypedDict, Dict


class LolGameEvent(TypedDict):
    # TODO Changing event timestamp from ms to s, ask if losing precision matters to anybody
    timestamp: int  # Timestamp of the event, expressed in seconds
    # TODO See if we constrain event type to an enum.
    type: str  # Should likely be defined as an enumeration
    playerId: int  # The id field in a LolGameTeamPlayer. Refers to the player performing the action

    # TODO See how we define the position
    position: Dict[str, int]  # Defined as distance from the bottom left of the map

    # TODO See how we handle all event-specific fields like victimId. Should we even define them here?
