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
```
game: dict
├── teams: dict
├── players: list
│   ├── snapshots: list
│   ├── runes: dict
│   └── items: list
└── event: list
```

# Data access examples

## Game
```python console
game['riotID']
>>> 1353193

game['riotServer']
>>> ESPORTSTMNT03

game['duration']
>>> 1776

game['startTimestamp']
>>> 1587810654658

game['winner']
>>> blue
```

## Team
```python console
teams = game['teams']

teams.keys()
>>> ['blue', 'red']

blue_team = teams['blue']

blue_team['firstBlood']
>>> True

blue_team['baronKills']
>>> 2
```

## Player
```python console
players = game['players']

blue_mid = next(p for p in players if p['team'] == 'blue' and p['role'] == 'mid')

blue_mid['playerID']
>>> 3

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

snapshot = snapshots[15]

snapshot['timestamp']
>>> 900000

snapshot['totalGold']
>>> 6417
```
### Runes
```python console
runes = blue_mid['runes']

runes['keystoneName']
>>> 8005

runes['keystoneName']
>>> Press the Attack

runes['primaryTree'][0]['rune_id']
>>> 9111
```
### Items
```python console
items = blue_mid['items']

items[0]['item_id']
>>> 3031

items[0]['item_slot']
>>> 1
```

## Event
```python console
events = game['events']

event = events[500]

event['type']
>>> 'CHAMPION_KILL'

event['timestamp']
>>> 919689

# The playerID of an event is the one of the player performing the event
event['playerID']
>>> 3
```
