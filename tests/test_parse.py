from pathlib import Path

import pytest

from crawler.parse import (
    metadata_from_slug,
    parse_overview,
    parse_results,
)

FIXTURES = Path(__file__).parent / "fixtures"


def read(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


class TestParseResults:
    def test_btw_2025_party_count(self):
        results = parse_results(read("btw_2025_absolutestimmen.html"))
        assert len(results) == 29

    def test_btw_2025_top_parties(self):
        r = parse_results(read("btw_2025_absolutestimmen.html"))
        assert r["CDU"]["pct"] == 22.55
        assert r["CDU"]["votes"] == 11_196_374
        assert r["CDU"]["color"] == "#121212"
        assert r["AfD"]["pct"] == 20.80
        assert r["AfD"]["votes"] == 10_328_780
        assert r["SPD"]["pct"] == 16.41
        assert r["SPD"]["votes"] == 8_149_124
        assert r["Grüne"]["pct"] == 11.61
        assert r["Linke"]["pct"] == 8.77
        assert r["CSU"]["pct"] == 5.97

    def test_btw_2025_includes_small_parties(self):
        r = parse_results(read("btw_2025_absolutestimmen.html"))
        # WerteUnion is below 5% and must still appear
        assert "WerteUnion" in r
        assert r["WerteUnion"]["pct"] > 0

    def test_btw_2025_all_have_pct(self):
        r = parse_results(read("btw_2025_absolutestimmen.html"))
        for name, party in r.items():
            assert isinstance(party["pct"], float), name
            assert party["pct"] >= 0, name

    def test_btw_2025_sum_under_101(self):
        r = parse_results(read("btw_2025_absolutestimmen.html"))
        total = sum(p["pct"] for p in r.values())
        assert total <= 101.0

    def test_ltw_th_2024_party_count(self):
        r = parse_results(read("ltw_th_2024_absolutestimmen.html"))
        assert len(r) == 15

    def test_ltw_th_2024_top_parties(self):
        r = parse_results(read("ltw_th_2024_absolutestimmen.html"))
        assert r["AfD"]["pct"] > 30
        assert "Linke" in r
        assert "CDU" in r
        assert "BSW" in r

    def test_ltw_by_2023_party_count(self):
        r = parse_results(read("ltw_by_2023_absolutestimmen.html"))
        assert len(r) == 15

    def test_ltw_by_2023_top_parties(self):
        r = parse_results(read("ltw_by_2023_absolutestimmen.html"))
        assert r["CSU"]["pct"] > 30
        assert "FW" in r  # Freie Wähler
        assert "Grüne" in r


class TestParseOverview:
    def test_btw_2025_turnout(self):
        o = parse_overview(read("btw_2025.html"))
        assert o["turnout"] == 82.5

    def test_btw_2025_government(self):
        o = parse_overview(read("btw_2025.html"))
        assert o["government"] == ["UNION", "SPD"]

    def test_ltw_by_2023_turnout(self):
        o = parse_overview(read("ltw_by_2023.html"))
        assert o["turnout"] == 73.3

    def test_ltw_by_2023_government(self):
        o = parse_overview(read("ltw_by_2023.html"))
        assert o["government"] == ["CSU", "FW"]

    def test_ltw_th_2024_turnout(self):
        o = parse_overview(read("ltw_th_2024.html"))
        assert o["turnout"] == 73.6

    def test_ltw_th_2024_no_government_yet(self):
        # Government not formed at archive time — wrapper absent
        o = parse_overview(read("ltw_th_2024.html"))
        assert o["government"] is None


class TestMetadataFromSlug:
    def test_bundestagswahl(self):
        m = metadata_from_slug("2025-02-23-BT-DE")
        assert m == {
            "title": "Bundestagswahl 2025",
            "date": "2025-02-23T00:00:00",
            "kind": "Bundestagswahl",
            "territory": "Deutschland",
        }

    def test_europawahl(self):
        m = metadata_from_slug("2024-06-09-EP-DE")
        assert m == {
            "title": "Europawahl in Deutschland 2024",
            "date": "2024-06-09T00:00:00",
            "kind": "Europawahl",
            "territory": "Europawahl",
        }

    def test_landtagswahl_bayern(self):
        m = metadata_from_slug("2023-10-08-LT-DE-BY")
        assert m == {
            "title": "Landtagswahl Bayern 2023",
            "date": "2023-10-08T00:00:00",
            "kind": "Landtagswahl",
            "territory": "Bayern",
        }

    def test_landtagswahl_thueringen(self):
        m = metadata_from_slug("2024-09-01-LT-DE-TH")
        assert m["territory"] == "Thüringen"
        assert m["title"] == "Landtagswahl Thüringen 2024"

    def test_landtagswahl_baden_wuerttemberg(self):
        m = metadata_from_slug("2026-03-08-LT-DE-BW")
        assert m["territory"] == "Baden-Württemberg"

    def test_buergerschaftswahl_hamburg(self):
        m = metadata_from_slug("2025-03-02-LT-DE-HH")
        assert m["kind"] == "Bürgerschaftswahl"
        assert m["territory"] == "Hamburg"
        assert m["title"] == "Bürgerschaftswahl Hamburg 2025"

    def test_buergerschaftswahl_bremen(self):
        m = metadata_from_slug("2023-05-14-LT-DE-HB")
        assert m["kind"] == "Bürgerschaftswahl"
        assert m["territory"] == "Bremen"

    def test_abgeordnetenhauswahl_berlin(self):
        m = metadata_from_slug("2023-02-12-LT-DE-BE")
        assert m["kind"] == "Abgeordnetenhauswahl"
        assert m["territory"] == "Berlin"
        assert m["title"] == "Abgeordnetenhauswahl Berlin 2023"

    def test_unknown_state_code_raises(self):
        with pytest.raises(ValueError):
            metadata_from_slug("2025-01-01-LT-DE-ZZ")

    def test_unknown_kind_raises(self):
        with pytest.raises(ValueError):
            metadata_from_slug("2025-01-01-XY-DE")
