# wahlergebnisse

JSON Wahlergebnisse von Wahlen in Deutschland

Die Daten sind nur vollständig für die 43 Wahlen, zu denen es Ausgaben des Wahl-o-Mat gibt. 

# Quelle

Der Datensatz mit den Wahlergebnissen liegt in der Datei `wahlergebnisse.extended.json`.

Die Daten wurden mit dem Skript `get_data.sh` aus dem Wahlarchiv der Taggesschau bezogen und mit dem Skript `convert_to_json.py` aus HTML in JSON übertragen. Mit dem Skript `convert_to_json.py` wurden fehlende Datensätze ergänzt. Siehe hierzu auch Issue #2. 

Die Datei `governments.json` enthält Informationen über Mandata und gewählte Regierungen, die mit den Wahlergebnissen kombiniert werden können.

# Hinweis zur Lizensierung

Die Prognose zum Ergebnis der Landtagswahl 2018 in Bayern stammt von [dawum.de](https://dawum.de/Bayern/). Diese 
Daten sind lizensiert unter [CC-BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.de).
