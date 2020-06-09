from typing import TypedDict


# This class is used both in LolEvent and LolGamePlayerSnapshot classes
class Position(TypedDict):
    """A position on the LoL map.
    """

    # min: -120
    # max: 14870
    x: int  # Horizontal distance from bottom left of the map
    y: int  # Vertical distance from bottom left of the map
