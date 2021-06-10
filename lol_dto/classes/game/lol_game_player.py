from dataclasses import dataclass, field
from typing import List, Dict, Optional

from lol_dto.classes.game.position import Position
from lol_dto.classes.game.lol_game_event import (
    LolGamePlayerItemEvent,
    LolGamePlayerWardEvent,
    LolGamePlayerSkillLevelUpEvent,
)


@dataclass
class LolGamePlayerSnapshot:
    """
    Information about a player at a specific point in the game
    """

    timestamp: float  # Timestamp of the event expressed in seconds from the game start, with possible ms precision

    currentGold: int  # Current gold (at the time of the snapshot)
    totalGold: int  # Total gold earned

    xp: int  # Current experience
    xpDiff: int  # Experience difference with the opponent in the same role

    level: int  # Current champion level

    cs: int  # Total number of minions and monsters killed

    monstersKilled: int  # Total monsters (neutral minions) killed
    monstersKilledDiff: int  # Total monsters killed difference with the opponent in the same role

    position: Position = None  # Player position, None for the last "snapshot"

    # Those two last fields are redundant but can be added for convenience

    # Total gold difference with the opponent in the same role
    totalGoldDiff: int = None

    csDiff: int = None  # Total CS difference with the opponent in the same role


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

    slot: int  # Goes from 0 to 6 as of 2020
    id: int  # Referring to Riot API item ID
    name: str = None  # Optional item name for convenience


@dataclass
class LolGamePlayerSummonerSpell:
    """A single summoner spell chosen by a player"""

    slot: int  # 0 or 1
    id: int  # Referring to Riot API summoner spell ID
    name: str = None  # Optional summoner spell name for convenience


@dataclass
class LolGamePlayerEndOfGameStats:
    """End of game stats for a player in a game"""

    # No None defaults set as those fields should usually be set from Riot's API
    #   TODO Maybe set defaults because of incomplete scoreboards that you can get from Leaguepedia?

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

    # Items are simply a list with the 'slot' field defining which item slot they occupied.
    # The list cannot be simply indexed on this 'slot' as many players have empty slots at the end of games.

    # List of end of game items
    items: List[LolGamePlayerItem] = field(default_factory=list)


@dataclass
class LolGamePlayer:
    """A player in a LoL game.

    All player-specific information should be present here.
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

    # Snapshots represent player-specific information at a given timestamp.
    # Timestamp could be used as keys but JSON does not allow for integer keys.
    # This is therefore simply a list, and you should not expect it to be indexed or sorted in any particular way.
    snapshots: List[LolGamePlayerSnapshot] = field(default_factory=list)

    # Item events is a list of item buys, sell, and undo
    itemsEvents: List[LolGamePlayerItemEvent] = field(default_factory=list)

    # Ward events are a list of wards placed and destroyed
    wardsEvents: List[LolGamePlayerWardEvent] = field(default_factory=list)

    # Skill level up events are every time the player used a skill or evolution point
    skillsLevelUpEvents: List[LolGamePlayerSkillLevelUpEvent] = field(
        default_factory=list
    )
