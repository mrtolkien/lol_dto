from dataclasses import dataclass
from typing import List

try:
    # TODO Make the optional import have a better syntax and a proper extra
    import lol_id_tools
except ImportError:
    pass

# TODO Currently, this is relying on lol_id_tools and far from perfect
#   Ideally, move it to using cassiopeia and using the right patch information through self.game backrefs


@dataclass
class ChampionNameClass:
    championId: int

    @property
    def championName(self) -> str:
        return lol_id_tools.get_name(self.championId, object_type="champion")


@dataclass
class BanNamesClass:
    bans: List[int]

    @property
    def bansNames(self) -> List[str]:
        return [lol_id_tools.get_name(b, object_type="champion") for b in self.bans]


@dataclass
class RuneNameClass:
    id: int

    @property
    def name(self) -> str:
        return lol_id_tools.get_name(self.id, object_type="rune")


@dataclass
class RuneTreeNameClass:
    primaryRuneTreeId: int
    secondaryRuneTreeId: int

    @property
    def primaryRuneTreeName(self) -> str:
        return lol_id_tools.get_name(self.primaryRuneTreeId, object_type="rune")

    @property
    def secondaryRuneTreeName(self) -> str:
        return lol_id_tools.get_name(self.secondaryRuneTreeId, object_type="rune")


@dataclass
class ItemNameClass:
    id: int

    @property
    def name(self) -> str:
        return lol_id_tools.get_name(self.id, object_type="item")


@dataclass
class SummonerNameClass:
    id: int

    @property
    def name(self) -> str:
        return lol_id_tools.get_name(self.id, object_type="summoner_spell")
