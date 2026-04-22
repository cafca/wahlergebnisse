"""HTML parsing for the Tagesschau Wahlarchiv."""

from __future__ import annotations

import re
from datetime import date

from bs4 import BeautifulSoup

STATE_CODES: dict[str, str] = {
    "BW": "Baden-Württemberg",
    "BY": "Bayern",
    "BE": "Berlin",
    "BB": "Brandenburg",
    "HB": "Bremen",
    "HH": "Hamburg",
    "HE": "Hessen",
    "MV": "Mecklenburg-Vorpommern",
    "NI": "Niedersachsen",
    "NW": "Nordrhein-Westfalen",
    "RP": "Rheinland-Pfalz",
    "SL": "Saarland",
    "SN": "Sachsen",
    "ST": "Sachsen-Anhalt",
    "SH": "Schleswig-Holstein",
    "TH": "Thüringen",
}

SLUG_RE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})-(?P<kind>[A-Z]{2})-DE(?:-(?P<state>[A-Z]{2}))?$"
)


def _to_float(s: str) -> float:
    return float(s.strip().replace(".", "").replace(",", "."))


def _to_int(s: str) -> int:
    return int(s.strip().replace(".", "").replace(",", ""))


def parse_results(html: str) -> dict[str, dict]:
    """Parse per-party results from an absolutestimmen_embed.shtml page.

    Returns a dict keyed by party short name, each value containing
    ``pct`` (float), ``votes`` (int), and ``color`` (hex string if available).
    """
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table", class_="fivepercentX")
    if not tables:
        raise ValueError("No fivepercentX tables found on absolutestimmen page")

    results: dict[str, dict] = {}
    for table in tables:
        for row in table.find_all("tr", class_="row"):
            label = row.find("td", class_="labelshort")
            perc = row.find("td", class_="perc")
            votes = row.find("td", class_="votes")
            if not (label and perc and votes):
                continue
            name = label.get_text(strip=True)
            if not name:
                continue
            entry: dict = {
                "pct": _to_float(perc.get_text()),
                "votes": _to_int(votes.get_text()),
            }
            color = _extract_color(row)
            if color:
                entry["color"] = color
            results[name] = entry
    return results


def _extract_color(row) -> str | None:
    """Best-effort hex color for a party row.

    Priority: ``border-color`` on the label's span (newer BTW layout) then the
    bar chart ``background-color`` (older Landtagswahl layout). The grey
    placeholder ``#707173`` is ignored so it doesn't mask missing data.
    """
    span = row.select_one("td.labelshort span[style]")
    if span is not None:
        m = re.search(r"border-color:\s*(#[0-9a-fA-F]{6})", span.get("style", ""))
        if m:
            color = m.group(1)
            if color.lower() != "#707173":
                return color

    bar = row.select_one("td.barholder div[style]")
    if bar is not None:
        m = re.search(r"background-color:\s*(#[0-9a-fA-F]{6})", bar.get("style", ""))
        if m:
            color = m.group(1)
            if color.lower() != "#707173":
                return color
    return None


def parse_overview(html: str) -> dict:
    """Parse turnout and government (coalition) from the main election page."""
    soup = BeautifulSoup(html, "html.parser")

    turnout: float | None = None
    for number in soup.find_all("span", class_="wahlbeteiligung--number"):
        text = number.get_text(strip=True)
        if text.endswith("%"):
            try:
                turnout = _to_float(text[:-1])
            except ValueError:
                continue
            break

    government: list[str] | None = None
    wrapper = soup.find("div", class_="wahlbeteiligung--regierung-wrapper")
    if wrapper:
        labels = wrapper.find_all("span", class_="wahlbeteiligung--parteilabel")
        government = [lbl.get_text(strip=True) for lbl in labels]
        if not government:
            government = None

    return {"turnout": turnout, "government": government}


def metadata_from_slug(slug: str) -> dict:
    """Derive title, ISO date, kind, and territory from a Tagesschau slug.

    Slug format: ``YYYY-MM-DD-TT-DE[-XX]`` where TT is BT/LT/EP and XX
    the two-letter state code for Landtags-level elections.
    """
    m = SLUG_RE.match(slug)
    if not m:
        raise ValueError(f"Unrecognized slug format: {slug!r}")

    iso = f"{m['date']}T00:00:00"
    year = int(m["date"][:4])
    # Validate date components
    date.fromisoformat(m["date"])

    kind_code = m["kind"]
    state_code = m["state"]

    if kind_code == "BT":
        return {
            "title": f"Bundestagswahl {year}",
            "date": iso,
            "kind": "Bundestagswahl",
            "territory": "Deutschland",
        }
    if kind_code == "EP":
        return {
            "title": f"Europawahl in Deutschland {year}",
            "date": iso,
            "kind": "Europawahl",
            "territory": "Europawahl",
        }
    if kind_code == "LT":
        if state_code is None:
            raise ValueError(f"LT slug missing state code: {slug!r}")
        if state_code not in STATE_CODES:
            raise ValueError(f"Unknown state code {state_code!r} in slug {slug!r}")
        territory = STATE_CODES[state_code]
        if state_code in ("HB", "HH"):
            kind = "Bürgerschaftswahl"
        elif state_code == "BE":
            kind = "Abgeordnetenhauswahl"
        else:
            kind = "Landtagswahl"
        return {
            "title": f"{kind} {territory} {year}",
            "date": iso,
            "kind": kind,
            "territory": territory,
        }

    raise ValueError(f"Unknown election kind code {kind_code!r} in slug {slug!r}")
