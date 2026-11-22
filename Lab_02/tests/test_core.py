from copy import deepcopy

import pytest

from core import (
    Record,
    boost_category,
    pipe,
    popular_only,
    reduce_stats,
    sort_by_total_desc,
    take,
    with_total,
)


@pytest.fixture
def courses() -> list[Record]:
    return [
        {
            "id": 1,
            "title": "Python Basics",
            "category": "Programming",
            "enrollments": [120, 80, 60],
        },
        {
            "id": 2,
            "title": "Data Science Intro",
            "category": "Data",
            "enrollments": [90, 70],
        },
        {"id": 3, "title": "Web Design", "category": "Design", "enrollments": [40, 30]},
        {
            "id": 4,
            "title": "Algorithms",
            "category": "Programming",
            "enrollments": [100, 90, 50],
        },
        {
            "id": 5,
            "title": "SQL Fundamentals",
            "category": "Data",
            "enrollments": [60, 50, 40],
        },
        {
            "id": 6,
            "title": "UX Research",
            "category": "Design",
            "enrollments": [20, 10],
        },
    ]


def build(top_n: int):
    return pipe(
        with_total(),
        boost_category("Programming", 1.1),
        popular_only(100.0),
        sort_by_total_desc(),
        take(top_n),
    )


def test_top_n(courses: list[Record]) -> None:
    result = build(3)(courses)
    assert [r["title"] for r in result] == [
        "Python Basics",
        "Algorithms",
        "Data Science Intro",
    ]


def test_no_mutation(courses: list[Record]) -> None:
    original = deepcopy(courses)
    build(3)(courses)
    assert courses == original


def test_reduce_stats() -> None:
    recs: list[Record] = [{"id": 1, "total": 10.0}, {"id": 2, "total": 20.0}]
    stats = reduce_stats(recs)
    assert stats["count"] == 2
    assert stats["enrollments"] == pytest.approx(30.0)
    assert stats["avg_enrollments"] == pytest.approx(15.0)


def test_pipe_order() -> None:
    f = pipe(lambda x: x + 1, lambda x: x * 2)
    assert f(3) == 8
