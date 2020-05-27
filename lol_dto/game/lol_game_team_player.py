from typing import TypedDict, List, Dict, Optional

from lol_dto.game.lol_game_event import Position


class LolGamePlayerSnapshot(TypedDict):
    """Information about a player at a specific point in the game.
    """

    timestamp: float  # Timestamp of the event expressed in seconds from the game start, with possible ms precision

    currentGold: int  # Current gold (at the time of the snapshot)
    totalGold: int  # Total gold earned
    totalGoldDiff: Optional[int]  # Total gold difference with the opponent in the same role

    cs: int  # Total number of minions and monsters killed
    csDiff: int  # Total CS difference with the opponent in the same role
    monstersKilled: int  # Total monsters (neutral minions) killed

    position: Position  # Player position


class LolGamePlayerRune(TypedDict):
    """A single rune used by one of the players.
    """

    slot: int  # Goes from 0 to 9 as of 2020
    id: int  # Referring to Riot API rune ID
    name: Optional[str]  # Optional rune name for convenience

    rank: int  # Used by stats perks to represent the number of points put in it

    stats: List[int]  # Riot-provided end-of-game statistics for the rune


class LolGamePlayerRunes(TypedDict):
    """All runes used by player.
    """

    primaryTreeId: int  # Refers to Riot rune tree ID
    secondaryTreeId: int  # Refers to Riot rune tree ID

    runes_list: List[LolGamePlayerRune]


class LolGamePlayerItem(TypedDict):
    """A single item that a player possessed at the end of the game.
    """

    slot: int  # Goes from 0 to 6 as of 2020
    id: int  # Referring to Riot API item ID
    name: str  # Optional item name for convenience


class LolGamePlayerSummonerSpell(TypedDict):
    """A single summoner spell chosen by a player.
    """

    slot: int  # 0 or 1
    id: int  # Referring to Riot API summoner spell ID
    name: str  # Optional summoner spell name for convenience


class LolGamePlayer(TypedDict):
    """A player in a LoL game.

    All player-specific information should be present here.
    """

    inGameName: str  # The in-game name is not linked to a particular data source and should be unique

    # TODO Most contentious part of the spec, will likely need a rework
    id: int  # Usually equal to participantId in Riot’s API. Meant to identify the player in events.

    # /!\ This field should be curated if it is present /!\
    role: Optional[str]  # Standard roles are top, jungle, mid, bot, support as of 2020.

    championId: int  # Referring to Riot API champion ID
    championName: int  # Optional champion name for convenience

    # Foreign keys are the ways to identify this player in the data sources used to gather the data
    # Any key that is present in game['sources'] should also be present here
    # A Riot API 'foreignKeys' dict looks like: {'riot': {'accountId': str, 'platformId': str}}
    foreignKeys: Dict[str, dict]

    profileIcon: int  # Refers to Riot API icon ID

    # Snapshots represent player-specific information at a given timestamp.
    # Timestamp could be used as keys, but JSON does not allow for integer keys.
    # This is therefore simply a list, and you should not expect it to be indexed or sorted in any particular way.
    snapshots: List[LolGamePlayerSnapshot]

    # Runes are a dictionary and not directly a list to allow for primaryTree and secondaryTree information
    runes: LolGamePlayerRunes

    # Items are simply a list with the 'slot' field defining which item slot they occupied.
    # The list cannot be simply indexed on this 'slot' as many players have empty slots at the end of games.
    items: List[LolGamePlayerItem]

    # Summoner spells is a simple 2-items list
    summonerSpells: List[LolGamePlayerSummonerSpell]

    # As first blood is player-specific, this does not appear in Team objects.
    firstBlood: bool  # True if the player performed the first blood
    firstBloodAssist: bool  # True if the player assisted the first blood kill
    firstTower: bool  # True if the player dealt the last hit to the first tower kill
    firstTowerAssist: bool  # True if the player assisted the first tower kill
    firstInhibitor: bool  # True if the player dealt the last hit to the first inhibitor kill
    firstInhibitorAssist: bool  # True if the player assisted in the first inhibitor kill

    # TODO Add a small description for every field

    # All statistics here refer to end of game stats, so we do not preface them by anything.
    kills: int
    deaths: int
    assists: int
    gold: int
    cs: int
    level: int

    # Warding-related statistics
    wardsPlaced: int
    wardsKilled: int
    visionWardsBought: int
    visionScore: int

    # Kills-related statistics
    killingSprees: int  # Number of a time a player has initiated a killing spree (2 or more consecutive kills)
    largestKillingSpree: int  # Largest consecutive kills, above 0 only if it reached at least 2

    doubleKills: int
    tripleKills: int
    quadraKills: int
    pentaKills: int

    towerKills: int
    inhibitorKills: int

    # Using modern Riot nomenclature of monsters for "neutral minions"
    monsterKills: int
    monsterKillsInAlliedJungle: int
    monsterKillsInEnemyJungle: int

    # Damage-related statistics
    # Total true damage dealt can be calculated by subtracting physical and magical damage to the total
    totalDamageDealt: int  # Includes damage to minions and monsters
    physicalDamageDealt: int
    magicalDamageDealt: int

    # Total true damage dealt  to champions can be calculated by subtracting physical and magical damage to the total
    totalDamageDealtToChampions: int
    physicalDamageDealtToChampions: int
    magicalDamageDealtToChampions: int

    # Total true damage taken can be calculated by subtracting physical and magical damage to the total
    totalDamageTaken: int
    physicalDamageTaken: int
    magicalDamageTaken: int

    # Really random statistics
    longestTimeSpentLiving: int  # Expressed in seconds
    largestCriticalStrike: int  # Full raw damage of the largest critical strike
    goldSpent: int  # Can be useful to try and identify AFK players?

    # The following fields need to have their behaviour properly explained as part of the specification
    totalHeal: int  # TODO Document this field
    totalUnitsHealed: int  # TODO Document this field
    damageSelfMitigated: int  # TODO Document this field

    totalTimeCrowdControlDealt: int  # TODO Document this field
    timeCCingOthers: int  # TODO Document this field
