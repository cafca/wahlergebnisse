"""Entry assembly and validation for wahlergebnisse.json records."""

from __future__ import annotations

# Territories currently present in wahlergebnisse.json. New crawls must emit
# one of these — unexpected territories likely indicate a parser regression.
CANONICAL_TERRITORIES: frozenset[str] = frozenset(
    {
        "Baden-Württemberg",
        "Bayern",
        "Berlin",
        "Brandenburg",
        "Bremen",
        "Deutschland",
        "Europawahl",
        "Hamburg",
        "Hessen",
        "Mecklenburg-Vorpommern",
        "Niedersachsen",
        "Nordrhein-Westfalen",
        "Rheinland-Pfalz",
        "Saarland",
        "Sachsen",
        "Sachsen-Anhalt",
        "Schleswig-Holstein",
        "Thüringen",
    }
)


def build_entry(
    *,
    metadata: dict,
    url: str,
    overview: dict,
    results: dict[str, dict],
    preliminary: bool = False,
) -> dict:
    """Assemble a single ``wahlergebnisse.json`` entry.

    Raises ``ValueError`` on missing required fields or unknown territories.
    """
    entry = {
        "title": metadata["title"],
        "url": url,
        "date": metadata["date"],
        "territory": metadata["territory"],
        "kind": metadata["kind"],
        "government": overview.get("government"),
        "turnout": overview.get("turnout"),
        "results": results,
    }
    if preliminary:
        entry["preliminary"] = True
    validate_entry(entry)
    return entry


def validate_entry(entry: dict) -> None:
    """Enforce the invariants metawahl's ``bootstrap_db.py`` relies on."""
    required = ("title", "url", "date", "territory", "kind")
    for key in required:
        if not entry.get(key):
            raise ValueError(f"Entry missing required field {key!r}: {entry.get('title')}")

    if "results" not in entry:
        raise ValueError(f"Entry missing required field 'results': {entry.get('title')}")

    if entry["territory"] not in CANONICAL_TERRITORIES:
        raise ValueError(
            f"Unknown territory {entry['territory']!r}; refusing to write to "
            "wahlergebnisse.json. Add it to CANONICAL_TERRITORIES if legitimate."
        )

    if not entry["results"]:
        raise ValueError(f"Entry has no party results: {entry['title']!r}")

    pct_total = 0.0
    for name, party in entry["results"].items():
        pct = party.get("pct")
        if not isinstance(pct, (int, float)):
            raise ValueError(
                f"Party {name!r} in {entry['title']!r} missing numeric pct"
            )
        pct_total += float(pct)

    # Same tolerance as the original crawler; catches missing-parties and
    # duplicate-parties regressions without over-rejecting rounded input.
    if pct_total > 101.0:
        raise ValueError(
            f"Result percentages sum to {pct_total:.2f} for "
            f"{entry['title']!r} (expected <= 101.0)"
        )
