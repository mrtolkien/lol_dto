from dataclasses import dataclass


@dataclass
class RiotGameSource:
    """
    Example source class for the Riot API
    Use it with:
        setattr(game.sources, 'riotLolApi', RiotGameSource(gameId=..., platformId=...))
    """

    gameId: int = None
    platformId: str = None

    # Esports games field
    gameHash: str = None


@dataclass
class RiotPlayerSource:
    puuid: str = None
    accountId: str = None
    summonerId: str = None
    platformId: str = None

    participantId: int = None  # Will usually be player.id, but it is still a key unique to this data source
