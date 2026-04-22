"""HTTP client with on-disk cache for Tagesschau pages."""

from __future__ import annotations

import hashlib
import time
from pathlib import Path

import requests

ARCHIVE_BASE = "https://www.tagesschau.de/wahl/archiv"
USER_AGENT = "wahlergebnisse-crawler/0.1 (+https://github.com/ciex/wahlergebnisse)"
REQUEST_DELAY_SECONDS = 1.0


class Fetcher:
    """Fetches Tagesschau pages, caching responses on disk.

    Call sites hit ``fetch(url)``; repeat calls return the cached body.
    """

    def __init__(self, cache_dir: Path | str = ".cache", delay: float = REQUEST_DELAY_SECONDS):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.delay = delay
        self._last_request_at: float | None = None
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": USER_AGENT})

    def _cache_path(self, url: str) -> Path:
        key = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
        return self.cache_dir / f"{key}.html"

    def fetch(self, url: str, refresh: bool = False) -> str:
        path = self._cache_path(url)
        if path.exists() and not refresh:
            return path.read_text(encoding="utf-8")

        if self._last_request_at is not None:
            elapsed = time.monotonic() - self._last_request_at
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)

        response = self._session.get(url, timeout=30)
        self._last_request_at = time.monotonic()
        response.raise_for_status()
        path.write_text(response.text, encoding="utf-8")
        return response.text

    def fetch_election(self, slug: str, refresh: bool = False) -> tuple[str, str]:
        """Return (overview_html, results_html) for an election slug."""
        overview = self.fetch(f"{ARCHIVE_BASE}/{slug}/", refresh=refresh)
        results = self.fetch(
            f"{ARCHIVE_BASE}/{slug}/absolutestimmen_embed.shtml", refresh=refresh
        )
        return overview, results


def archive_url(slug: str) -> str:
    """Canonical archive URL for a given slug (stable across runs)."""
    return f"{ARCHIVE_BASE}/{slug}/index.shtml"
