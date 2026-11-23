from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType


@dataclass(frozen=True, slots=True)
class MatchStat:
    match_id: int
    goals: int
    assists: int
    minutes: int


@dataclass(frozen=True, slots=True)
class Player:
    id: int
    name: str
    rating: float
    roles: frozenset[str]
    stats: tuple[MatchStat, ...]
    profile: Mapping[str, str] = field(hash=False)


def make_profile(**kwargs: str) -> Mapping[str, str]:
    base = dict(kwargs)
    return MappingProxyType(base)
