from typing import TypedDict, Optional


class Position(TypedDict):
    """A position on the LoL map.
    """

    # min: {x: -120, y: -120}
    # max: {x: 14870, y: 14980}
    x: int  # Horizontal distance from bottom left of the map
    y: int  # Vertical distance from bottom left of the map
