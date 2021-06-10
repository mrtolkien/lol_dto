from dataclasses import dataclass


# This class is used both in LolEvent and LolGamePlayerSnapshot classes
@dataclass
class Position:
    """
    A position on the LoL map, defined by Riot's coordinates
    """

    # min: -120
    # max: 14870
    x: int  # Horizontal distance from bottom left of the map
    y: int  # Vertical distance from bottom left of the map
