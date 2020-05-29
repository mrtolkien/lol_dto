from typing import TypedDict, Optional


class Position(TypedDict):
    """A position on the LoL map.
    """

    # min: {x: -120, y: -120}
    # max: {x: 14870, y: 14980}
    x: int  # Horizontal distance from bottom left of the map
    y: int  # Vertical distance from bottom left of the map


class Building(TypedDict):
    """A building on Summoner’s Rift
    """

    # Last update: June 2020
    # TODO Check that 'UNDEFINED_TURRET' are Azir turrets, and check 'FOUNTAIN_TURRET' events (very rare, old games).
    buildingType: str  # 'TURRET', 'INHIBITOR'
    lane: str  # 'TOP', 'MID', 'BOT', None
    towerLocation: Optional[str]  # 'OUTER', 'INNER', 'INHIBITOR', 'NEXUS', None
    side: str  # 'blue', 'red'


class Monster(TypedDict, total=False):
    """A monster on Summoner’s Rift
    """

    type: str  # 'DRAGON', 'NASHOR', or 'RIFT_HERALD' as of June 2020
    subType: Optional[str]  # 'CLOUD', 'INFERNAL', 'MOUNTAIN', 'OCEAN', 'ELDER'
