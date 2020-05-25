from typing import TypedDict


class LolGameEvent(TypedDict):
    # TODO Changing event timestamp from ms to s, ask if losing precision matters to anybody
    timestamp: int  # Timestamp of the event, expressed in seconds
    # TODO See if we constrain event type to an enum.
    type: str  # Should likely be defined as an enumeration
    playerId: int  # The id field in a LolGameTeamPlayer
