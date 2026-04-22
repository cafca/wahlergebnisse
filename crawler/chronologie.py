"""Known election slugs to catch up.

Hardcoded list updated by hand when new elections happen — simpler and more
reliable than scraping the archive landing page (which redesigns periodically).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

# Elections after the 2021-09-26 data cutoff. Extend after each future election.
KNOWN_SLUGS: tuple[str, ...] = (
    "2022-03-27-LT-DE-SL",
    "2022-05-08-LT-DE-SH",
    "2022-05-15-LT-DE-NW",
    "2022-10-09-LT-DE-NI",
    "2023-02-12-LT-DE-BE",
    "2023-05-14-LT-DE-HB",
    "2023-10-08-LT-DE-BY",
    "2023-10-08-LT-DE-HE",
    "2024-06-09-EP-DE",
    "2024-09-01-LT-DE-SN",
    "2024-09-01-LT-DE-TH",
    "2024-09-22-LT-DE-BB",
    "2025-02-23-BT-DE",
    "2025-03-02-LT-DE-HH",
)

_SLUG_URL_RE = re.compile(r"/(\d{4}-\d{2}-\d{2}-[A-Z]{2}-DE(?:-[A-Z]{2})?)/")


def slugs_in_dataset(path: Path | str) -> set[str]:
    """Extract slugs from URLs in wahlergebnisse.json."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    slugs: set[str] = set()
    for entry in data:
        m = _SLUG_URL_RE.search(entry.get("url", ""))
        if m:
            slugs.add(m.group(1))
    return slugs


def missing_slugs(path: Path | str) -> list[str]:
    """Return KNOWN_SLUGS not yet present in wahlergebnisse.json."""
    present = slugs_in_dataset(path)
    return [s for s in KNOWN_SLUGS if s not in present]
