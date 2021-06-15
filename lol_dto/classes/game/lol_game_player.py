from dataclasses import dataclass, field
from typing import List

from lol_dto.classes.game.position import Position
from lol_dto.classes.game.lol_game_event import (
    LolGamePlayerItemEvent,
    LolGamePlayerWardEvent,
    LolGamePlayerSkillLevelUpEvent,
    LolGamePlayerLargeMonsterKill,
)


@dataclass
class LolGamePlayerSnapshot:
    """
    Information about a player at a specific point in the game

    Riot's API gives this information with a 1 minute granularity in its MatchTimeline object
    """

    timestamp: float  # Timestamp of the event expressed in seconds from the game start, with possible ms precision

    # Player position, None for the last "snapshot" in Riot's API
    position: Position = None

    currentGold: int = None  # Current gold (at the time of the snapshot)
    totalGold: int = None  # Total gold earned

    xp: int = None  # Current experience

    level: int = None  # Current champion level

    cs: int = None  # Total number of minions and monsters killed
    monstersKilled: int = None  # Total monsters (neutral minions) killed

    # Whether or not the player is alive at the time of the snapshot
    isAlive: bool = None

    # TODO Add summoner spell and ultimate availability info

    # Those four last fields are redundant but can be added for convenience
    # TODO Should they be dropped?
    # Experience difference with the opponent in the same role
    xpDiff: int = None
    # Total gold difference with the opponent in the same role
    totalGoldDiff: int = None
    # Total CS difference with the opponent in the same role
    csDiff: int = None
    # Total monsters killed difference with the opponent in the same role
    monstersKilledDiff: int = None


@dataclass
class LolGamePlayerRune:
    """
    A single rune used by one of the players
    """

    slot: int  # Primary tree, secondary tree, then stats perks
    id: int  # Referring to Riot API rune ID

    name: str = None  # Optional rune name for convenience

    # Riot-provided end-of-game statistics for the rune
    stats: List[int] = field(default_factory=list)


@dataclass
class LolGamePlayerItem:
    """
    A single item that a player possessed at the end of the game
    """

    id: int  # Referring to Riot API item ID
    slot: int = None  # Goes from 0 to 6 as of 2020

    name: str = None  # Optional item name for convenience


@dataclass
class LolGamePlayerSummonerSpell:
    """A single summoner spell chosen by a player"""

    id: int  # Referring to Riot API summoner spell ID
    slot: int = None  # 0 or 1
    name: str = None  # Optional summoner spell name for convenience


@dataclass
class LolGamePlayerEndOfGameStats:
    """End of game stats for a player in a game"""

    # As first blood is player-specific, this does not appear in Team objects.
    firstBlood: bool = None  # True if the player performed the first blood
    firstBloodAssist: bool = None  # True if the player assisted the first blood kill
    # True if the player dealt the last hit to the first tower kill
    firstTower: bool = None
    firstTowerAssist: bool = None  # True if the player assisted the first tower kill
    # True if the player dealt the last hit to the first inhibitor kill
    firstInhibitor: bool = None
    #  True if the player assisted in the first inhibitor kill
    firstInhibitorAssist: bool = None

    # TODO Add a small description for every field

    # All statistics here refer to end of game stats, so we do not preface them by anything.
    kills: int = None
    deaths: int = None
    assists: int = None
    gold: int = None
    cs: int = None
    level: int = None

    # Warding-related statistics
    wardsPlaced: int = None
    wardsKilled: int = None
    visionWardsBought: int = None
    visionScore: int = None

    # Kills-related statistics
    killingSprees: int = None  # Number of a time a player has initiated a killing spree (2 or more consecutive kills)
    # Largest consecutive kills, above 0 only if it reached at least 2
    largestKillingSpree: int = None

    doubleKills: int = None
    tripleKills: int = None
    quadraKills: int = None
    pentaKills: int = None

    towerKills: int = None
    inhibitorKills: int = None

    # Using modern Riot nomenclature of monsters for "neutral minions"
    monsterKills: int = None
    monsterKillsInAlliedJungle: int = None
    monsterKillsInEnemyJungle: int = None

    # Damage-related statistics
    # Total true damage dealt can be calculated by subtracting physical and magic damage to the total
    totalDamageDealt: int = None  # Includes damage to minions and monsters
    physicalDamageDealt: int = None
    magicDamageDealt: int = None

    # Total true damage dealt  to champions can be calculated by subtracting physical and magic damage to the total
    totalDamageDealtToChampions: int = None
    physicalDamageDealtToChampions: int = None
    magicDamageDealtToChampions: int = None

    # Total true damage taken can be calculated by subtracting physical and magic damage to the total
    totalDamageTaken: int = None
    physicalDamageTaken: int = None
    magicDamageTaken: int = None

    # Other damage statistics
    damageDealtToObjectives: int = None
    damageDealtToBuildings: int = None
    damageDealtToTurrets: int = None

    # Really random statistics
    longestTimeSpentLiving: int = None  # Expressed in seconds
    largestCriticalStrike: int = None  # Full raw damage of the largest critical strike
    goldSpent: int = None  # Can be useful to try and identify AFK players?

    # The following fields need to have their behaviour properly explained as part of the specification
    totalHeal: int = None  # TODO Document this field
    totalDamageShieldedOnTeammates: int = None  # TODO Document this field
    totalUnitsHealed: int = None  # TODO Document this field
    damageSelfMitigated: int = None  # TODO Document this field

    totalTimeCCDealt: int = None  # TODO Document this field
    timeCCingOthers: int = None  # TODO Document this field

    # Items are simply a list with the 'slot' field defining which item slot they occupied.
    # The list cannot be simply indexed on this 'slot' as many players have empty slots at the end of games.

    # List of end of game items
    items: List[LolGamePlayerItem] = field(default_factory=list)


@dataclass
class LolGamePlayer:
    """
    A player in a LoL game

    All player-specific information should be present here
    """

    id: int = None  # Usually equal to participantId in Riot’s API. Meant to identify the player in kills
    # TODO review use case and process for non-Riot data (Leaguepedia, Bayes, ...)

    inGameName: str = None  # The in-game name is not linked to a particular data source and should be unique
    profileIconId: int = None  # Refers to Riot API icon ID

    # /!\ This field should be curated if it is present /!\
    role: str = None  # Role values are TOP, JGL, MID, BOT, SUP as of 2020.

    championId: int = None  # Referring to Riot API champion ID
    championName: str = None  # Optional champion name for convenience

    # Unique identifiers are the ways to identify this player in the data sources used to gather the data
    # Any attribute that is present in game.sources should also be present here
    # A Riot API uniqueIdentifiers class looks like:
    #                                       player.sources.accountId and player.uniqueIdentifiers.platformId
    # Each parser transforming data to the LolGame format should implement its own source dataclass to allow for
    #   merging different sources
    sources: dataclass = None

    # Rune information is stored directly in the player object as they are beginning-of-game information
    primaryRuneTreeId: int = None  # Refers to Riot rune tree ID
    primaryRuneTreeName: str = None  # Optional name for human readability

    secondaryRuneTreeId: int = None  # Refers to Riot rune tree ID
    secondaryRuneTreeName: str = None  # Optional name for human readability

    runes: List[LolGamePlayerRune] = field(default_factory=list)

    # Summoner spells is a simple 2-items list
    summonerSpells: List[LolGamePlayerSummonerSpell] = field(default_factory=list)

    # End of game stats are statistics like total kills, damage, vision score, ...
    endOfGameStats: LolGamePlayerEndOfGameStats = None

    # Snapshots represent player-specific information at a given timestamp
    # Timestamp could be used as keys but JSON does not allow for integer keys
    # This is therefore simply a list, which you should not expect it to be indexed or sorted in any particular way
    snapshots: List[LolGamePlayerSnapshot] = field(default_factory=list)

    # Item events is a list of item buys, sell, and undo
    itemsEvents: List[LolGamePlayerItemEvent] = field(default_factory=list)

    # Ward events are a list of wards placed and destroyed
    wardsEvents: List[LolGamePlayerWardEvent] = field(default_factory=list)

    # Skill level up events are every time the player used a skill or evolution point
    skillsLevelUpEvents: List[LolGamePlayerSkillLevelUpEvent] = field(
        default_factory=list
    )

    # The next fields are usually not available in Riot's API

    # Kills of large monsters, accessible in some data sources
    largeMonstersKills: List[LolGamePlayerLargeMonsterKill] = field(
        default_factory=list
    )

    # Direct level up events exist in some data sources
    # It is a simple list of level up timestamps, in seconds
    levelUpEvents: List[int] = field(default_factory=list)

    # Cooldown information can be parsed from spectator mode
    #   It includes ultimate usage, summoner spells usage, and items usage (only items with CDs)
    cooldownEvents: List[LolGamePlayerCooldownEvent] = field(default_factory=list)
