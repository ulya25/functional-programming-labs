from dataclasses import replace

from model import MatchStat, Player


def add_match_stat(player: Player, stat: MatchStat) -> Player:
    return replace(player, stats=player.stats + (stat,))


def add_role(player: Player, role: str) -> Player:
    return replace(player, roles=player.roles | frozenset({role}))


def update_rating(player: Player, new_rating: float) -> Player:
    return replace(player, rating=new_rating)


def total_goals(player: Player) -> int:
    return sum(s.goals for s in player.stats)
