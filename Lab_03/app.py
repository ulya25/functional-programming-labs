from core import add_match_stat, add_role, total_goals, update_rating
from model import MatchStat, Player, make_profile


def build_player() -> Player:
    return Player(
        id=1,
        name="Ivan",
        rating=7.5,
        roles=frozenset({"forward"}),
        stats=(MatchStat(1, 2, 1, 90),),
        profile=make_profile(team="Lions", country="UA"),
    )


def render(title: str, player: Player) -> None:
    print(
        f"{title}: rating={player.rating}, roles={sorted(player.roles)}, "
        f"matches={len(player.stats)}, goals={total_goals(player)}"
    )


def main() -> None:
    p1 = build_player()
    p2 = add_match_stat(p1, MatchStat(2, 3, 0, 80))
    p3 = add_role(p2, "captain")
    p4 = update_rating(p3, 8.4)
    render("p1", p1)
    render("p2", p2)
    render("p3", p3)
    render("p4", p4)
    print("p1 is p4:", p1 is p4, "| hashable:", len({p1, p2, p3, p4}) == 4)


if __name__ == "__main__":
    main()
