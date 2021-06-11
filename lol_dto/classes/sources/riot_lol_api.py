from dataclasses import dataclass


@dataclass
class RiotGameSource:
    """
    Example source class for the Riot API
    Use it with:
        setattr(game.sources, 'riotLolApi', RiotGameSource(gameId=..., platformId=...))
    """

    gameId: int
    platformId: str


@dataclass
class RiotPlayerSource:
    puuid: str = None
    accountId: str = None
    summonerId: str = None
    platformId: str = None
