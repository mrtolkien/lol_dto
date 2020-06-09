from typing import TypedDict, List, Dict, Optional

from lol_dto.classes.game.position import Position
from lol_dto.classes.game.lol_game_event import (
    LolGamePlayerItemEvent,
    LolGamePlayerWardEvent,
    LolGamePlayerSkillLevelUpEvent,
)


class LolGamePlayerSnapshot(TypedDict, total=False):
    """Information about a player at a specific point in the game.
    """

    timestamp: float  # Timestamp of the event expressed in seconds from the game start, with possible ms precision

    currentGold: int  # Current gold (at the time of the snapshot)
    totalGold: int  # Total gold earned
    totalGoldDiff: Optional[int]  # Total gold difference with the opponent in the same role

    xp: int  # Current experience
    level: int  # Current champion level

    cs: int  # Total number of minions and monsters killed
    csDiff: Optional[int]  # Total CS difference with the opponent in the same role

    monstersKilled: int  # Total monsters (neutral minions) killed

    position: Optional[Position]  # Player position, None for the last "snapshot"


class LolGamePlayerRune(TypedDict, total=False):
    """A single rune used by one of the players.
    """

    slot: int  # Primary tree, secondary tree, then stats perks
    id: int  # Referring to Riot API rune ID

    name: Optional[str]  # Optional rune name for convenience
    rank: Optional[int]  # Used by stats perks to represent the number of points put in it

    stats: List[int]  # Riot-provided end-of-game statistics for the rune


class LolGamePlayerItem(TypedDict, total=False):
    """A single item that a player possessed at the end of the game.
    """

    slot: int  # Goes from 0 to 6 as of 2020
    id: int  # Referring to Riot API item ID
    name: Optional[str]  # Optional item name for convenience


class LolGamePlayerSummonerSpell(TypedDict, total=False):
    """A single summoner spell chosen by a player.
    """

    slot: int  # 0 or 1
    id: int  # Referring to Riot API summoner spell ID
    name: Optional[str]  # Optional summoner spell name for convenience


class LolGamePlayerStats(TypedDict, total=False):
    """End of game stats for a player in a game
    """

    # Items are simply a list with the 'slot' field defining which item slot they occupied.
    # The list cannot be simply indexed on this 'slot' as many players have empty slots at the end of games.
    items: List[LolGamePlayerItem]  # List of end of game items

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
    # Total true damage dealt can be calculated by subtracting physical and magic damage to the total
    totalDamageDealt: int  # Includes damage to minions and monsters
    physicalDamageDealt: int
    magicDamageDealt: int

    # Total true damage dealt  to champions can be calculated by subtracting physical and magic damage to the total
    totalDamageDealtToChampions: int
    physicalDamageDealtToChampions: int
    magicDamageDealtToChampions: int

    # Total true damage taken can be calculated by subtracting physical and magic damage to the total
    totalDamageTaken: int
    physicalDamageTaken: int
    magicDamageTaken: int

    # Other damage statistics
    damageDealtToObjectives: int
    damageDealtToTurrets: int

    # Really random statistics
    longestTimeSpentLiving: int  # Expressed in seconds
    largestCriticalStrike: int  # Full raw damage of the largest critical strike
    goldSpent: int  # Can be useful to try and identify AFK players?

    # The following fields need to have their behaviour properly explained as part of the specification
    totalHeal: int  # TODO Document this field
    totalUnitsHealed: int  # TODO Document this field
    damageSelfMitigated: int  # TODO Document this field

    totalTimeCCDealt: int  # TODO Document this field
    timeCCingOthers: int  # TODO Document this field


class LolGamePlayer(TypedDict, total=False):
    """A player in a LoL game.

    All player-specific information should be present here.
    """

    # TODO Most contentious part of the spec, will likely need a rework
    id: int  # Usually equal to participantId in Riot’s API. Meant to identify the player in events.

    inGameName: str  # The in-game name is not linked to a particular data source and should be unique
    profileIconId: int  # Refers to Riot API icon ID

    # /!\ This field should be curated if it is present /!\
    role: Optional[str]  # Standard roles are top, jungle, mid, bot, support as of 2020.

    championId: int  # Referring to Riot API champion ID
    championName: Optional[str]  # Optional champion name for convenience

    # Unique identifiers are the ways to identify this player in the data sources used to gather the data
    # Any key that is present in game['sources'] should also be present here
    # A Riot API 'uniqueIdentifiers' dict looks like: {'riot': {'accountId': str, 'platformId': str}}
    uniqueIdentifiers: Dict[str, dict]

    # TODO Add esports fields (team, playerName, ...)

    # Rune information is stored directly in the player object as they are beginning-of-game information
    primaryRuneTreeId: int  # Refers to Riot rune tree ID
    secondaryRuneTreeId: int  # Refers to Riot rune tree ID

    runes: List[LolGamePlayerRune]

    # Summoner spells is a simple 2-items list
    summonerSpells: List[LolGamePlayerSummonerSpell]

    # End of game stats are statistics like total kills, damage, vision score, ...
    endOfGameStats: LolGamePlayerStats

    # Snapshots represent player-specific information at a given timestamp.
    # Timestamp could be used as keys but JSON does not allow for integer keys.
    # This is therefore simply a list, and you should not expect it to be indexed or sorted in any particular way.
    snapshots: List[LolGamePlayerSnapshot]

    # Item events is a list of item buys, sell, and undo
    itemsEvents: List[LolGamePlayerItemEvent]

    # Ward events are a list of wards placed and destroyed
    wardsEvents: List[LolGamePlayerWardEvent]

    # Skill level up events are every time the player used a skill or evolution point
    skillsEvents: List[LolGamePlayerSkillLevelUpEvent]
