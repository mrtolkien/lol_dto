# LoL Game DTO

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A unified Data Transfer Object for League of Legends games. Currently developed by Tolki.

## 2.0 note and JSON serialization

Version 2.0 moved the implementation from `TypedDict` to `dataclass`, which means the syntax changed and is not
backwards compatible.

`dataclasses.asdict()` can be used to get the object as a dictionary, and then saved as a JSON.

Fields can be omitted when not supplied to make the object lighter. This is particularly useful for Snapshots objects.

## Motivation

League of Legends game information can come in many forms. The most popular source is Riot’s API and in particular its
[MATCH-V5](https://developer.riotgames.com/apis#match-v5/) endpoint, which defines its own MatchDto
and MatchTimelineDto objects. While other sources of information could follow Riot’s data format, requiring
multiple objects to represent a single game and being constrained by Riot’s data format is inconvenient.

This is why creating a unique, community-driven representation of League of Legends game data will help communication
and teamwork in open source projects. Improving the data structure will also make the data more accessible to new
developers, and will make existing libraries easier to maintain.

### Constraints

- Retain all the information present in the Riot API

- Allow for external information, like role, to be added to the object

- Be compatible across a wide variety of programming languages

### General philosophy

- We try to adhere to the [Google JSON Style Guide](https://google.github.io/styleguide/jsoncstyleguide.xml?showone=Property_Name_Format#Property_Name_Format)
- Information is as close as possible to the objects it refers to
  - Player-specific information is directly under `player` objects
  - Team-wide information is directly under `team` objects
- Information is not duplicated
  - `winner` is only defined once in the `game` object
- Field names are coherent and comply with modern LoL nomenclature
  - Every field that is an identifier ends with `id`
  - Fields like `cs` or `monstersKilled` use current game vocabulary (as of June 2020)
  - All durations from the game start are expressed in seconds

#### `null`

The `null` value should only be used for unknown information. The best practice is to not have unknown fields in
the object to keep it as light as possible.

## `lol_dto`

This repository hosts a `python` reference implementation in the form of a `dataclass`.

A `dataclass` does not enforce type constraints but will raise linter warnings and allows IDEs to autocomplete field names.

Another module focused on transforming `MatchDto` and `MatchTimelineDto` to a `LolGame` can
[be found here](https://github.com/mrtolkien/riot_transmute). Its
[unit tests](https://github.com/mrtolkien/riot_transmute/blob/master/tests/test_riot_transmute.py)
and [JSON examples](https://github.com/mrtolkien/riot_transmute/tree/master/json_examples)
are useful sources to better understand the data structure.

### LolGame DTO overview

```ascii
game: dict
├── sources: dict
├── teams: dict
|   ├── uniqueIdentifiers: dict
│   ├── bans: list
│   ├── monstersKills: list
│   ├── buildingsKills: list
│   └── players: list
│       ├── uniqueIdentifiers: dict
│       ├── endOfGameStats: dict
│       │   └── items: list
│       ├── summonersSpells: list
│       ├── runes: list
│       ├── snapshots: list
│       ├── itemsEvents: list
│       ├── wardsEvents: list
│       └── skillsLevelUpEvents: list
├── kills: list
├── picksBans: list
└── pauses: list
```

### Game

- `sources` represents unique identifiers for this game for a given data source
  - `"riotLolApi": { "gameId": 4409190456, "platformId": "KR" }`
- `teams` has properties equal to `'BLUE'` and `'RED'`
- `kills` are present directly at the root of the `game` object as they refer to multiple players through
  `killerId`, `victimId`, and `assistingParticipantsIds`
  - We have to rely on the arbitrary `participantId` given by the Riot API because:
    - Relying on `championId` makes it incompatible with blind pick
    - Relying on `inGameName` does not work for `MatchTimeline` objects from the Riot API
- `picksBans` represents the full picks and bans and is mostly used for esports games

### Team

- `bans` is a simple list of `id` of champions banned by the team.
- `monsterKills` and `buildingKills` are at the `team` level because they are team-wide
  - They both define their own `BuildingKillEvent` and `MonsterKillEvent` DTOs that are very different from Riot’s API
- `players` are simply in a list because no unique key arises
  - `roles` are not guaranteed to be defined and unique

### Player

- `id` refers to Riot API’s `participantId` and is unfortunately necessary to be able to link different objects coming
  from it
- `uniqueIdentifiers` is similar to `game['sources']` in that it represents a unique identifier for the player in the
  specified data source
  - `"riotLolApi": { "accountId": "3VcaXNMW8jq3adCqG0k0RPBaxoNL08NFXH_h4_2sKI_iEKw", "platformId": "KR" }`
- `endOfGameStats` represents statistics that are only available at the end of the game, including end of game `items`
  as well as `kills`, `totalDamageDealtToChampions`, ...
- `snapshots` is a list of timestamped information about the player, mostly `gold` and `position` at given timestamps
- `itemsEvents` are item-related events from players (buying, selling, undoing, destroying)
- `wardsEvents` are ward-related events from players (placing, destroying)
- `skillsLevelUpEvents` are skills level up events from players

## Contributing

Currently wanted contribution are:

- Feedback about the data structure and field names
- Implementation of the data structure in other programming languages
- C functions to cast Riot API objects to this LolGame DTO as multiple languages can bind to them
