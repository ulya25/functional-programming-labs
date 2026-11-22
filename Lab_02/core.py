from collections.abc import Callable, Iterable, Iterator
from functools import reduce
from itertools import islice
from typing import Any, TypedDict


class Record(TypedDict, total=False):
    id: int
    title: str
    category: str
    enrollments: list[float]
    total: float


def with_total() -> Callable[[Iterable[Record]], Iterator[Record]]:
    return lambda recs: (
        {**r, "total": float(sum(r.get("enrollments", []) or []))} for r in recs
    )


def boost_category(
    category: str, factor: float
) -> Callable[[Iterable[Record]], Iterator[Record]]:
    def _f(recs: Iterable[Record]) -> Iterator[Record]:
        for r in recs:
            t = float(r.get("total", 0.0))
            yield {**r, "total": (t * factor) if r.get("category") == category else t}

    return _f


def popular_only(min_total: float) -> Callable[[Iterable[Record]], Iterator[Record]]:
    return lambda recs: (r for r in recs if float(r.get("total", 0)) >= min_total)


def sort_by_total_desc() -> Callable[[Iterable[Record]], list[Record]]:
    return lambda recs: sorted(
        recs, key=lambda r: (-float(r.get("total", 0.0)), r.get("id", 0))
    )


def take(n: int) -> Callable[[Iterable[Record]], list[Record]]:
    return lambda recs: list(islice(recs, n))


def pipe(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def _p(x: Any) -> Any:
        for f in funcs:
            x = f(x)
        return x

    return _p


def reduce_stats(recs: Iterable[Record]) -> dict[str, float]:
    def step(acc: dict[str, float], r: Record) -> dict[str, float]:
        return {
            "count": acc["count"] + 1,
            "enrollments": acc["enrollments"] + float(r.get("total", 0.0)),
        }

    acc = reduce(step, recs, {"count": 0.0, "enrollments": 0.0})
    avg = acc["enrollments"] / acc["count"] if acc["count"] else 0.0
    return {
        "count": acc["count"],
        "enrollments": acc["enrollments"],
        "avg_enrollments": avg,
    }


def build_pipeline(
    top_n: int = 3,
    category: str = "Python",
    factor: float = 1.1,
    min_total: float = 100.0,
) -> Callable[[Any], Any]:
    return pipe(
        with_total(),
        boost_category(category, factor),
        popular_only(min_total),
        sort_by_total_desc(),
        take(top_n),
    )
