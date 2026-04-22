from pathlib import Path

import pytest

from crawler.fetch import archive_url
from crawler.parse import metadata_from_slug, parse_overview, parse_results
from crawler.schema import build_entry, validate_entry

FIXTURES = Path(__file__).parent / "fixtures"


def read(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def _btw_2025_entry(preliminary: bool = False) -> dict:
    slug = "2025-02-23-BT-DE"
    return build_entry(
        metadata=metadata_from_slug(slug),
        url=archive_url(slug),
        overview=parse_overview(read("btw_2025.html")),
        results=parse_results(read("btw_2025_absolutestimmen.html")),
        preliminary=preliminary,
    )


def test_build_entry_btw_2025_shape():
    entry = _btw_2025_entry()
    assert entry["title"] == "Bundestagswahl 2025"
    assert entry["date"] == "2025-02-23T00:00:00"
    assert entry["territory"] == "Deutschland"
    assert entry["kind"] == "Bundestagswahl"
    assert entry["turnout"] == 82.5
    assert entry["government"] == ["UNION", "SPD"]
    assert entry["url"].startswith("https://www.tagesschau.de/wahl/archiv/")
    assert len(entry["results"]) == 29
    assert "preliminary" not in entry


def test_build_entry_preliminary_flag():
    entry = _btw_2025_entry(preliminary=True)
    assert entry["preliminary"] is True


def test_build_entry_ltw_th_2024_no_government():
    slug = "2024-09-01-LT-DE-TH"
    entry = build_entry(
        metadata=metadata_from_slug(slug),
        url=archive_url(slug),
        overview=parse_overview(read("ltw_th_2024.html")),
        results=parse_results(read("ltw_th_2024_absolutestimmen.html")),
    )
    assert entry["government"] is None
    assert entry["territory"] == "Thüringen"


def test_validate_rejects_unknown_territory():
    entry = _btw_2025_entry()
    entry["territory"] = "Atlantis"
    with pytest.raises(ValueError, match="Unknown territory"):
        validate_entry(entry)


def test_validate_rejects_party_without_pct():
    entry = _btw_2025_entry()
    entry["results"]["FakeParty"] = {"votes": 1}
    with pytest.raises(ValueError, match="missing numeric pct"):
        validate_entry(entry)


def test_validate_rejects_missing_results():
    entry = _btw_2025_entry()
    entry["results"] = {}
    with pytest.raises(ValueError, match="no party results"):
        validate_entry(entry)


def test_validate_rejects_pct_overflow():
    entry = _btw_2025_entry()
    # Poisoned entry: every party reports 50% -> sum > 101
    for party in entry["results"]:
        entry["results"][party] = {"pct": 50.0}
    with pytest.raises(ValueError, match="percentages sum"):
        validate_entry(entry)
