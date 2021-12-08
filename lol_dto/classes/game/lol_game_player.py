from dataclasses import dataclass, field
from typing import List

from lol_dto.classes.game.position import Position
from lol_dto.classes.game.lol_game_event import (
    LolGamePlayerItemEvent,
    LolGamePlayerWardEvent,
    LolGamePlayerSkillLevelUpEvent,
    LolGamePlayerLargeMonsterKill,
    LolGamePlayerSpellUseEvent,
    LolGamePlayerSpecialKill,
)
from lol_dto.classes.sources.empty_dataclass import EmptyDataclass
from lol_dto.names_helper.name_classes import (
    ChampionNameClass,
    RuneNameClass,
    ItemNameClass,
    SummonerNameClass,
    RuneTreeNameClass,
)


@dataclass
class LolGamePlayerSnapshotChampionStats:
    """
    Champion stats at a given snapshot for a player
    """

    abilityHaste: int = None
    abilityPower: int = None
    armor: int = None
    armorPen: int = None
    armorPenPercent: int = None
    attackDamage: int = None
    attackSpeed: int = None
    bonusArmorPenPercent: int = None
    bonusMagicPenPercent: int = None
    ccReduction: int = None
    cooldownReduction: int = None
    health: int = None
    healthMax: int = None
    healthRegen: int = None
    lifesteal: int = None
    magicPen: int = None
    magicPenPercent: int = None
    magicResist: int = None
    movementSpeed: int = None
    omnivamp: int = None
    physicalVamp: int = None
    power: int = None
    powerMax: int = None
    powerRegen: int = None
    spellVamp: int = None


@dataclass
class LolGamePlayerSnapshotDamageStats:
    """
    Damage stats at a given snapshot for a player
    """

    magicDamageDone: int = None
    magicDamageDoneToChampions: int = None
    magicDamageTaken: int = None
    physicalDamageDone: int = None
    physicalDamageDoneToChampions: int = None
    physicalDamageTaken: int = None
    totalDamageDone: int = None
    totalDamageDoneToChampions: int = None
    totalDamageTaken: int = None
    trueDamageDone: int = None
    trueDamageDoneToChampions: int = None
    trueDamageTaken: int = None


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

    # Whether or not a summoner spell is available or not
    spell1Available: bool = None
    spell2Available: bool = None

    # Ultimate availability
    ultimateAvailable: bool = None

    # Absolutely no clue what this is supposed to be, match-v5 field
    timeEnemySpentControlled: int = None

    # New snapshot fields from match-v5
    championStats: LolGamePlayerSnapshotChampionStats = field(
        default_factory=LolGamePlayerSnapshotChampionStats
    )
    damageStats: LolGamePlayerSnapshotDamageStats = field(
        default_factory=LolGamePlayerSnapshotDamageStats
    )


@dataclass
class LolGamePlayerRune(RuneNameClass):
    """
    A single rune used by one of the players
    """

    slot: int  # Primary tree, secondary tree, then stats perks
    id: int  # Referring to Riot API rune ID

    # Riot-provided end-of-game statistics for the rune
    stats: List[int] = field(default_factory=list)


@dataclass
class LolGamePlayerItem(ItemNameClass):
    """
    A single item that a player possessed at the end of the game
    """

    id: int  # Referring to Riot API item ID
    slot: int = None  # Goes from 0 to 6 as of 2020


@dataclass
class LolGamePlayerSummonerSpell(SummonerNameClass):
    """A single summoner spell chosen by a player"""

    id: int  # Referring to Riot API summoner spell ID
    slot: int = None  # 0 or 1
    casts: int = None  # New match-v5 field


@dataclass
class LolGamePlayerEndOfGameStats:
    """End of game stats for a player in a game"""

    # As first blood is player-specific, this does not appear in Team objects.
    firstBlood: bool = None  # True if the player performed the first blood
    firstBloodAssist: bool = None  # True if the player assisted the first blood kill
    # True if the player dealt the last hit to the first turret kill
    firstTurret: bool = None
    firstTurretAssist: bool = None  # True if the player assisted the first turret kill
    # True if the player dealt the last hit to the first inhibitor kill
    firstInhibitor: bool = None
    #  True if the player assisted in the first inhibitor kill
    firstInhibitorAssist: bool = None

    # TODO Add a proper description for every field

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

    turretKills: int = None
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

    # Spell uses statistics, accessible in match-v5
    #   I hate the format, but am not sure where to put it otherwise where it would make sense
    spell1Casts: int = None
    spell2Casts: int = None
    spell3Casts: int = None
    spell4Casts: int = None

    # Really random statistics
    longestTimeSpentLiving: int = None  # Expressed in seconds
    largestCriticalStrike: int = None  # Full raw damage of the largest critical strike
    goldSpent: int = None  # Can be useful to try and identify AFK players?

    # The following fields need to have their behaviour properly explained as part of the specification
    totalHeal: int = None
    totalDamageShieldedOnTeammates: int = None
    totalUnitsHealed: int = None
    damageSelfMitigated: int = None

    totalTimeCCDealt: int = None
    timeCCingOthers: int = None

    # New match-v5 end of game stats
    xp: int = None
    bountyLevel: int = None
    baronKills: int = None
    championTransform: int = None
    consumablesPurchased: int = None
    detectorWardsPlaced: int = None
    dragonKills: int = None
    inhibitorTakedowns: int = None
    itemsPurchased: int = None
    nexusKills: int = None
    nexusTakedowns: int = None
    objectivesStolen: int = None
    objectivesStolenAssists: int = None
    sightWardsBoughtInGame: int = None
    totalHealsOnTeammates: int = None
    totalTimeSpentDead: int = None
    turretTakedowns: int = None

    # Items are simply a list with the 'slot' field defining which item slot they occupied.
    # The list cannot be simply indexed on this 'slot' as many players have empty slots at the end of games.

    # List of end of game items
    items: List[LolGamePlayerItem] = field(default_factory=list)


@dataclass
class LolGamePlayer(ChampionNameClass, RuneTreeNameClass):
    """
    A player in a LoL game

    All player-specific information should be present here
    """

    # Usually equal to participantId in Riot’s API. Meant to identify the player in kills
    #   Can be arbitrary, the only thing that matters is to be consistent with game.kills.killerId fields
    id: int = None

    inGameName: str = None  # The in-game name is not linked to a particular data source and should be unique
    profileIconId: int = None  # Refers to Riot API icon ID

    # /!\ This field should be curated if it is present /!\
    role: str = None  # Role values are TOP, JGL, MID, BOT, SUP as of 2020.

    championId: int = None  # Referring to Riot API champion ID

    # Unique identifiers are the ways to identify this player in the data sources used to gather the data
    # Any attribute that is present in game.sources should also be present here
    # A Riot API uniqueIdentifiers class looks like:
    #                                       player.sources.accountId and player.uniqueIdentifiers.platformId
    # Each parser transforming data to the LolGame format should implement its own source dataclass to allow for
    #   merging different sources
    sources: dataclass = field(default_factory=EmptyDataclass)

    # Rune information is stored directly in the player object as they are beginning-of-game information
    primaryRuneTreeId: int = None  # Refers to Riot rune tree ID
    secondaryRuneTreeId: int = None  # Refers to Riot rune tree ID

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
    spellsUses: List[LolGamePlayerSpellUseEvent] = field(default_factory=list)

    # Special kills are linked to players and represent first bloods, multi-kills, and ace
    specialKills: List[LolGamePlayerSpecialKill] = field(default_factory=list)
