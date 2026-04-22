"""CLI for the wahlergebnisse catch-up crawler.

Subcommands:
    list-missing        print KNOWN_SLUGS not yet in wahlergebnisse.json
    fetch <slug>        fetch one election; append/update wahlergebnisse.json
    catch-up            fetch every missing slug

Use ``--dry-run`` with ``fetch``/``catch-up`` to print JSON without writing.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from crawler.chronologie import KNOWN_SLUGS, missing_slugs
from crawler.fetch import Fetcher, archive_url
from crawler.parse import metadata_from_slug, parse_overview, parse_results
from crawler.schema import build_entry

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = REPO_ROOT / "wahlergebnisse.json"

_SLUG_URL_RE = re.compile(r"/(\d{4}-\d{2}-\d{2}-[A-Z]{2}-DE(?:-[A-Z]{2})?)/")


def _slug_of(entry: dict) -> str | None:
    m = _SLUG_URL_RE.search(entry.get("url", ""))
    return m.group(1) if m else None


def _load_dataset(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def _existing_slugs(path: Path) -> set[str]:
    return {s for e in _load_dataset(path) if (s := _slug_of(e)) is not None}


def _append_new_entries(path: Path, new_entries: list[dict]) -> None:
    """Append entries to the JSON array without rewriting existing text.

    Re-serializing the whole file with json.dumps normalizes number formatting
    (e.g. ``5.30`` → ``5.3``), which would churn diffs for entries we aren't
    touching. Surgical text append keeps historical entries byte-identical.
    """
    if not new_entries:
        return
    raw = path.read_text(encoding="utf-8")
    close = raw.rfind("]")
    if close == -1:
        raise ValueError(f"No closing ']' in {path}")
    # Find previous non-whitespace char to decide whether array is empty.
    before_close = raw[:close].rstrip()
    trailing_ws = raw[len(before_close) : close]
    array_empty = before_close.endswith("[")
    serialized = [
        "  " + json.dumps(e, ensure_ascii=False, indent=2).replace("\n", "\n  ")
        for e in new_entries
    ]
    new_block = ",\n".join(serialized)
    if array_empty:
        body = before_close + "\n" + new_block + "\n"
    else:
        body = before_close + ",\n" + new_block + trailing_ws
    path.write_text(body + raw[close:], encoding="utf-8")


def _fetch_entry(fetcher: Fetcher, slug: str, preliminary: bool) -> dict:
    overview_html, results_html = fetcher.fetch_election(slug)
    return build_entry(
        metadata=metadata_from_slug(slug),
        url=archive_url(slug),
        overview=parse_overview(overview_html),
        results=parse_results(results_html),
        preliminary=preliminary,
    )


def cmd_list_missing(args: argparse.Namespace) -> int:
    missing = missing_slugs(DATASET_PATH)
    if not missing:
        print(f"All {len(KNOWN_SLUGS)} known slugs present.")
        return 0
    for slug in missing:
        print(slug)
    return 0


def cmd_fetch(args: argparse.Namespace) -> int:
    fetcher = Fetcher(cache_dir=REPO_ROOT / ".cache")
    entry = _fetch_entry(fetcher, args.slug, preliminary=args.preliminary)
    if args.dry_run:
        print(json.dumps(entry, ensure_ascii=False, indent=2))
        return 0
    if args.slug in _existing_slugs(DATASET_PATH):
        print(f"skipped (already present): {args.slug}", file=sys.stderr)
        return 1
    _append_new_entries(DATASET_PATH, [entry])
    print(f"added: {entry['title']} ({args.slug})")
    return 0


def cmd_catch_up(args: argparse.Namespace) -> int:
    missing = missing_slugs(DATASET_PATH)
    if not missing:
        print("Nothing to do.")
        return 0
    fetcher = Fetcher(cache_dir=REPO_ROOT / ".cache")
    new_entries: list[dict] = []
    for slug in missing:
        try:
            entry = _fetch_entry(fetcher, slug, preliminary=False)
        except Exception as exc:
            print(f"FAILED {slug}: {exc}", file=sys.stderr)
            if args.stop_on_error:
                return 1
            continue
        if args.dry_run:
            print(f"would add: {entry['title']} ({slug})")
        else:
            new_entries.append(entry)
            print(f"added: {entry['title']} ({slug})")
    if not args.dry_run:
        _append_new_entries(DATASET_PATH, new_entries)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="crawler")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-missing").set_defaults(func=cmd_list_missing)

    p_fetch = sub.add_parser("fetch")
    p_fetch.add_argument("slug")
    p_fetch.add_argument("--preliminary", action="store_true")
    p_fetch.add_argument("--dry-run", action="store_true")
    p_fetch.set_defaults(func=cmd_fetch)

    p_catch = sub.add_parser("catch-up")
    p_catch.add_argument("--dry-run", action="store_true")
    p_catch.add_argument("--stop-on-error", action="store_true")
    p_catch.set_defaults(func=cmd_catch_up)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
