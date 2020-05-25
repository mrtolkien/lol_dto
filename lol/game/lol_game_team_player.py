from typing import TypedDict, List, Dict


class LolGameTeamPlayerSnapshot(TypedDict):
    currentGold: int
    totalGold: int
    totalGoldDiff: int

    cs: int
    csDiff: int
    monstersKilled: int  # Moved to "monsters" nomenclature

    position: Dict[str, int]  # Defined as distance from the bottom left of the map


class LolGameTeamPlayerRune(TypedDict):
    slot: int  # Goes from 0 to 9 as of 2020
    id: int
    name: str  # Optional
    rank: int  # Used for perks to represent the number of points put in it
    # TODO Check if rank appears in Riot’s API

    stats: List[int]  # End of game stats per rune


class LolGameTeamPlayerItem(TypedDict):
    slot: int  # Goes from 0 to 6 as of 2020
    id: int
    name: str  # Optional


class LolGameTeamPlayerSummonerSpell(TypedDict):
    slot: int  # 0 or 1
    id: int
    name: str  # Optional


class LolGameTeamPlayer(TypedDict):
    id: int  # Can be equal to participantId in Riot’s API. Meant to identify the player in this game
    kills: int

    championId: int  # Based on Riot’s champions identifiers
    championName: int  # Optional

    inGameName: str  # The in-game name is not linked to a particular data source and is unique
    role: str  # Role as defined by the community. Roles are top, jungle, mid, bot, support as of 2020

    riotRole: str  # Role and lane as defined by Riot’s API, very inaccurate
    riotLane: str

    # Fields specific to a unique data source are prefaced by its name
    riotAccountId: str
    riotSummonerId: str
    riotProfileIcon: int

    # Example of esports information
    leaguepediaLink: str

    # TODO Ask about this design choice, a list is easier to create but harder to use
    # Current idea: keys should a duration expressed as mm:ss to allow for easy querying and sorting
    # To iterate on snapshots in chronological order, simply use: for time in sorted(snapshots): (...)
    snapshots: Dict[str, LolGameTeamPlayerSnapshot]

    # TODO Ask if runes/items should be a list or map. Currently a list because of regular structural
    # TODO See where/how to save primary/secondary rune tree names
    runes: List[LolGameTeamPlayerRune]
    items: List[LolGameTeamPlayerItem]
    summonerSpells: List[LolGameTeamPlayerSummonerSpell]

    # All stats here refer to end of game stats
    firstBlood: bool
    firstTower: bool

    kills: int
    deaths: int
    assists: int
    gold: int
    cs: int
    level: int

    # TODO Lots of fields here are redundant, maybe cutting them is better for a pure DTO
    killingSprees: int
    largestKillingSpree: int
    largestMultiKill: int
    doubleKills: int
    tripleKills: int
    quadraKills: int
    pentaKills: int

    towerKills: int
    inhibitorKills: int

    # Using modern Riot nomenclature of monsters for "neutral minions"
    # TODO See if people prefer neutral minions
    monsterKills: int
    monsterKillsInAlliedJungle: int
    monsterKillsInEnemyJungle: int

    wardsPlaced: int
    wardsKilled: int
    visionWardsBought: int
    visionScore: int

    timeDead: int  # Expressed in seconds

    largestCriticalStrike: int

    totalDamageDealt: int
    physicalDamageDealt: int
    magicalDamageDealt: int

    totalDamageDealtToChampions: int
    physicalDamageDealtToChampions: int
    magicalDamageDealtToChampions: int

    totalDamageTaken: int
    physicalDamageTaken: int
    magicalDamageTaken: int

    totalHeal: int
    # TODO Check this field’s use
    totalUnitsHealed: int  # Possibly irrelevant/wrong
    damageSelfMitigated: int  # same, might be an irrelevant field we should drop

    totalTimeCrowdControlDealt: int  # Misleading field imo
    timeCCingOthers: int  # Misleading field imo
