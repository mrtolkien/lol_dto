# LoL Game DTO
A unified Data Transfer Object for League of Legends games

# Goal
League of Legends game information can come in many forms. The most popular is Riot’s API and in particular its 
[MATCH-V4](https://developer.riotgames.com/apis#match-v4/) endpoint, which defines its own MatchDto 
and MatchTimelineDto objects.

While other sources of information could follow those specifications, having multiple objects represent a single game
and being constrained by Riot’s ever-changing data format is not convenient.

The goal of this unique DTO is to simplify interoperability between community tools, requiring data to only be cast
 once to this unique LoL Game DTO.

To be easily usable in multiple programming languages, we have chosen to keep the data format `JSON` compliant. This 
means allowed data types are strings, numbers, booleans, lists, and dictionaries.

# Structure overview
THIS IS A WORK IN PROGRESS AND NEEDS FINALISATION
```
game: dict
├── teams: dict
│   └── players: list
│       ├── snapshots: list
│       ├── runes: list
│       └── items: list
└── events: list
```

# Data access examples
THIS WAS RELATING TO THE VERY FIRST ALPHA AND IS OUT OF DATE

## Game
```python console
game['sources']['riot']['gameId']
>>> 1353193

game['sources']['riot']['platformId']
>>> ESPORTSTMNT03

game['duration']
>>> 1776

game['startDate']
>>> '2020-04-25T10:30:54Z'

game['winner']
>>> BLUE
```

## Team
```python console
teams = game['teams']

teams.keys()
>>> ['blue', 'red']

blue_team = teams['blue']

blue_team['firstBaron']
>>> True

blue_team['baronKills']
>>> 2
```

## Player
```python console
blue_players = game['blue']['players']

blue_mid = next(p for p in blue_players if p['role'] == 'mid')

blue_mid['kills']
>>> 7

blue_mid['championId']
>>> 1

# Object names can be added during processing for easier use
blue_mid['championName']
>>> Annie
```

### Snapshots
```python console
snapshots = blue_mid['snapshots']

len(snapshots)
>>> 29

snapshot = (s for s in snapshots if s['timestamp'] == 15*60)

snapshot['timestamp']
>>> 900.0

snapshot['totalGold']
>>> 6417
```
### Runes
```python console
runes = blue_mid['runes']

runes['primaryTreeId']
>>> 800

runes['runes_list'][0]['id']
>>> 8005

runes['runes_list'][0]['name']
>>> Press the Attack
```

### Items
```python console
items = blue_mid['items']

items[0]['id']
>>> 3031
```

## Event
```python console
events = game['events']

event = events[500]

event['type']
>>> 'CHAMPION_KILL'

event['timestamp']
>>> 919.689

# The playerID of an event is the one of the player performing the event, here the killer
event['playerId']
>>> 3
```

# Code formatting

If you want to contribute to the project the code should be formatted with `Black`, using a maximum line length of 100.
