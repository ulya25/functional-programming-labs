from dataclasses import FrozenInstanceError

import pytest

from core import add_match_stat, add_role, total_goals, update_rating
from model import MatchStat, Player, make_profile


@pytest.fixture
def player() -> Player:
    return Player(
        id=1,
        name="Ivan",
        rating=7.5,
        roles=frozenset({"forward"}),
        stats=(MatchStat(1, 2, 1, 90),),
        profile=make_profile(team="Lions", country="UA"),
    )


def test_add_match_stat_no_mutation(player: Player) -> None:
    original_stats = player.stats
    new_player = add_match_stat(player, MatchStat(2, 1, 0, 80))
    assert player.stats == original_stats
    assert len(player.stats) == 1
    assert len(new_player.stats) == 2
    assert new_player is not player


def test_add_role_no_mutation(player: Player) -> None:
    new_player = add_role(player, "captain")
    assert player.roles == frozenset({"forward"})
    assert new_player.roles == frozenset({"forward", "captain"})
    assert new_player is not player


def test_update_rating_no_mutation(player: Player) -> None:
    new_player = update_rating(player, 9.0)
    assert player.rating == 7.5
    assert new_player.rating == 9.0
    assert new_player is not player


def test_total_goals(player: Player) -> None:
    new_player = add_match_stat(player, MatchStat(2, 3, 0, 70))
    assert total_goals(player) == 2
    assert total_goals(new_player) == 5


def test_frozen_fields(player: Player) -> None:
    with pytest.raises((FrozenInstanceError, AttributeError)):
        player.rating = 9.0  # type: ignore[misc]


def test_profile_read_only(player: Player) -> None:
    with pytest.raises(TypeError):
        player.profile["team"] = "Tigers"  # type: ignore[index]


def test_profile_is_copied_from_source() -> None:
    source = {"team": "Lions"}
    profile = make_profile(**source)
    source["team"] = "Tigers"
    assert profile["team"] == "Lions"


def test_hashable_after_updates(player: Player) -> None:
    updated = {
        player,
        add_role(player, "captain"),
        update_rating(player, 8.0),
        add_match_stat(player, MatchStat(2, 1, 0, 80)),
    }
    assert len(updated) == 4


def test_equal_players_have_equal_hash(player: Player) -> None:
    same = update_rating(player, player.rating)
    assert same is not player
    assert same == player
    assert hash(same) == hash(player)
