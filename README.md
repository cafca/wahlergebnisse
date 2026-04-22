# wahlergebnisse

JSON Wahlergebnisse aller Bundestags-, Landtags- und Europawahlen in Deutschland seit 1946.

Die Daten wurden aus dem Wahlarchiv der Tagesschau extrahiert. Dieses Repository ist Teil von [metawahl.de](https://metawahl.de).

## Catch-up crawler

Kleiner Python-Crawler (`crawler/`) um nach jeder neuen Wahl die fehlenden Einträge aus dem Tagesschau-Wahlarchiv nachzutragen. Setup mit [`uv`](https://docs.astral.sh/uv/):

```bash
uv sync
uv run pytest                                     # Parser-Tests gegen Fixtures
uv run python -m crawler list-missing             # offene Slugs anzeigen
uv run python -m crawler fetch 2025-02-23-BT-DE --dry-run
uv run python -m crawler catch-up                 # alle fehlenden Wahlen anhängen
```

Neue Wahlen werden in [`crawler/chronologie.py`](crawler/chronologie.py) (`KNOWN_SLUGS`) eingetragen. Slug-Format: `YYYY-MM-DD-TT-DE[-XX]` (TT ∈ {BT, LT, EP}, XX = Bundesland-Kürzel). Layout-Änderungen bei der Tagesschau lassen die Fixture-Tests rot werden — dann Parser anpassen und neue Fixtures committen.

Das ursprüngliche [Jupyter-Notebook](Wahlergebnis-Crawler.ipynb) bleibt als historische Referenz im Repo.
