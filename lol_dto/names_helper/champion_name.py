from dataclasses import dataclass


@dataclass
class ChampionNameClass:
    championId: int

    @property
    def championName(self) -> str:
        ...
