from dataclasses import dataclass
from typing import List

try:
    import lol_id_tools
except ImportError:
    pass

# Ideally, move it to using cassiopeia and using the right patch information through self.game backrefs


@dataclass
class ChampionNameClass:
    championId: int

    @property
    def championName(self) -> str:
        return lol_id_tools.get_name(self.championId, object_type="champion", patch=self.game.patch)


@dataclass
class BanNamesClass:
    bans: List[int]

    @property
    def bansNames(self) -> List[str]:
        return [lol_id_tools.get_name(b, object_type="champion", patch=self.game.patch) for b in self.bans]


@dataclass
class RuneNameClass:
    id: int

    @property
    def name(self) -> str:
        return lol_id_tools.get_name(self.id, object_type="rune", patch=self.game.patch)


@dataclass
class RuneTreeNameClass:
    primaryRuneTreeId: int
    secondaryRuneTreeId: int

    @property
    def primaryRuneTreeName(self) -> str:
        return lol_id_tools.get_name(self.primaryRuneTreeId, object_type="rune", patch=self.game.patch)

    @property
    def secondaryRuneTreeName(self) -> str:
        return lol_id_tools.get_name(self.secondaryRuneTreeId, object_type="rune", patch=self.game.patch)


@dataclass
class ItemNameClass:
    id: int

    @property
    def name(self) -> str:
        return lol_id_tools.get_name(self.id, object_type="item", patch=self.game.patch)


@dataclass
class SummonerNameClass:
    id: int

    @property
    def name(self) -> str:
        return lol_id_tools.get_name(self.id, object_type="summoner_spell", patch=self.game.patch)
