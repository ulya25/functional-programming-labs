from typing import Any

from core import add_match_stat
from model import MatchStat, Player, make_profile

N = 2000


def test_mutable_baseline() -> None:
    player: dict[str, Any] = {"id": 1, "rating": 7.5, "stats": []}
    for i in range(N):
        player["stats"].append({"match_id": i, "goals": 1})
    assert len(player["stats"]) == N


def test_immutable_updates() -> None:
    player = Player(
        id=1,
        name="Ivan",
        rating=7.5,
        roles=frozenset({"forward"}),
        stats=(),
        profile=make_profile(team="Lions"),
    )
    for i in range(N):
        player = add_match_stat(player, MatchStat(i, 1, 0, 90))
    assert len(player.stats) == N
