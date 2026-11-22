import argparse
import json

from core import Record, build_pipeline, reduce_stats


def load_records(path: str) -> list[Record]:
    with open(path, encoding="utf-8") as f:
        data: list[Record] = json.load(f)
    return data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="sample_data.json")
    parser.add_argument("--top", type=int, default=3)
    parser.add_argument("--category", default="Programming")
    parser.add_argument("--factor", type=float, default=1.1)
    parser.add_argument("--min-total", type=float, default=100.0)
    return parser.parse_args()


def render(top: list[Record], stats: dict[str, float]) -> None:
    for r in top:
        print(r["title"], "total:", r["total"])
    print("Count:", stats["count"])
    print("Enrollments:", stats["enrollments"])
    print("Avg enrollments:", stats["avg_enrollments"])


def main() -> None:
    args = parse_args()
    records = load_records(args.data)
    pipeline = build_pipeline(
        top_n=args.top,
        category=args.category,
        factor=args.factor,
        min_total=args.min_total,
    )
    top = pipeline(records)
    stats = reduce_stats(top)
    render(top, stats)


if __name__ == "__main__":
    main()
