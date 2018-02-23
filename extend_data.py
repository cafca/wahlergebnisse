#!/usr/bin/env python3

import json

#
# Die Recherche-Fuktion des Tagesschau Wahlarchivs berücksichtigt einige Wahlen
# nicht. Die Daten für diese werden von diesem Skript als JSON file ausgegeben.
# Quelle der Daten sind Zweitstimmen aus der Ergebnis-Tabelle der jeweiligen
# Wikipedia-Seite: https://de.wikipedia.org/wiki/{title}
#


def compile_results(parties, votes, percentages):
    rv = dict()
    for i in range(len(parties)):
        rv[parties[i]] = {
            "votes": votes[i] if i < len(votes) else 0.0,
            "pct": percentages[i] if i < len(percentages) else 0.0
        }
    return rv

missing_occasions = list()


# BTW17

parties = ["CDU", "SPD", "AfD", "FDP", "Linke", "Grüne", "CSU", "FW", "Die Partei", "Tierschutzpartei", "NPD", "Piraten", "ÖDP", "BGE", "V-Partei", "DM", "DiB", "BP", "AD-Demokraten", "Tierschutzallianz", "MLPD", "Gesundheitsforschung", "MENSCHLICHE WELT", "DKP", "Die Grauen", "Volksabstimmung", "BüSo", "Die Humanisten", "MG", "du.", "DIE RECHTE", "SGP", "B*", "PDV"]

votes = [12447656, 9539381, 5878115, 4999449, 4297270, 4158400, 2869688, 463292, 454349, 374179, 176020, 173476, 144809, 97539, 64073, 63203, 60914, 58037, 41251, 32221, 29785, 23404, 11558, 11661, 9631, 10009, 6693, 5991, 5617, 3032, 2054, 1291, 911, 533]

percentages = [26.76, 20.51, 12.64, 10.75, 9.24, 8.94, 6.17, 1.00, 0.98, 0.80, 0.38, 0.37, 0.31, 0.21, 0.14, 0.14, 0.13, 0.12, 0.09, 0.07, 0.06, 0.05, 0.03, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01, 0.00, 0.00, 0.00, 0.00]


missing_occasions.append({
    "url": "https://wahl.tagesschau.de/wahlen/2017-09-24-BT-DE/index.shtml",
    "title": "Bundestagswahl 2017",
    "kind": "Bundestagswahl",
    "territory": "Deutschland",
    "date": "2017-09-24T00:00:00",
    "results": compile_results(parties, votes, percentages)
})


# Landtagswahl im Saarland 2017

parties = ["CDU", "SPD", "Die LINKE", "AfD", "Grüne", "FDP", "Familie", "Piraten", "NPD", "Freie Wähler", "LKR", "Reformer", "DIE EINHEIT", "DBD", "BGE", "FBU"]

votes = [217263, 158057,68566,32971,21392,17419,4435,3979,3744,2146,1179,880,872,543,286,51]

percentages = [40.70, 29.61, 12.85, 6.18, 4.01, 3.26, 0.83, 0.75, 0.70, 0.40, 0.22, 0.17, 0.16, 0.10, 0.05, 0.01]

# TODO: Replace WP-data with data from
# https://wahl.tagesschau.de/wahlen/2017-03-26-LT-DE-SL/index.shtml

missing_occasions.append({
    "url": "https://de.wikipedia.org/wiki/Landtagswahl im Saarland 2017",
    "title": "Landtagswahl im Saarland 2017",
    "kind": "Landtagswahl",
    "territory": "Saarland",
    "date": "2017-03-26T00:00:00",
    "results": compile_results(parties, votes, percentages)
})


# Landtagswahl in Schleswig-Holstein 2017

parties = ["CDU", "SPD", "GRÜNE", "FDP", "PIRATEN", "SSW", "DIE LINKE", "FAMILIE", "FREIE WÄHLER", "AfD", "LKR", "Die PARTEI", "Z.SH"]

votes = [471460, 401806, 190181, 169037, 17091, 48968, 56018, 9262, 8369, 86711, 3053, 8219, 4333]

percentages = [32.0, 27.3, 12.9, 11.5, 1.2, 3.3, 3.8, 0.6, 0.6, 5.9, 0.2, 0.6, 0.3]

# TODO: Replace WP-data with data from
# "https://wahl.tagesschau.de/wahlen/2017-05-07-LT-DE-SH/index.shtml"

missing_occasions.append({
    "url": "https://de.wikipedia.org/wiki/Landtagswahl in Schleswig-Holstein 2017",
    "title": "Landtagswahl in Schleswig-Holstein 2017",
    "kind": "Landtagswahl",
    "territory": "Schleswig-Holstein",
    "date": "2017-05-07T00:00:00",
    "results": compile_results(parties, votes, percentages)
})

# Landtagswahl in Nordrhein-Westfalen 2017

parties = ["CDU", "SPD", "FDP", "AfD", "Grüne", "Die Linke", "Piraten", "Tierschutzliste", "Die PARTEI", "Freie Wähler", "NPD", "BIG", "ÖDP", "AD-Demokraten NRW", "V-Partei³", "Aufbruch C", "Volksabstimmung", "MLPD", "Die Violetten", "JED", "REP", "Gesundheitsforschung", "BGE", "Schöner Leben", "DBD", "Die Rechte", "Zentrum", "DKP", "FBI/FWG", "Parteilose WG „BRD“", "PAN", "Familie", "LD", "LKR", "Einzelbewerber"]

votes = [2796683, 2649205, 1065307, 626756, 539062, 415936, 80780, 59747, 54990, 33083, 28723, 17421, 13288, 12688, 10013, 9636, 8386, 7707, 7171, 7054, 6597, 5964, 5260, 5162, 4742, 3589, 3336, 2899, 2877, 2002, 1349]

percentages =[32.95, 31.21, 12.55, 7.38, 6.35, 4.90, 0.95, 0.70, 0.65, 0.39, 0.34, 0.21, 0.16, 0.15, 0.12, 0.11, 0.10, 0.09, 0.08, 0.08, 0.08, 0.07, 0.06, 0.06, 0.06, 0.04, 0.04, 0.03, 0.03, 0.02, 0.02]

# TODO: Replace WP-data with data from
# http://wahl.tagesschau.de/wahlen/2017-05-14-LT-DE-NW/index.shtml

missing_occasions.append({
    "url": "de.wikipedia.org/wiki/Landtagswahl in Nordrhein-Westfalen 2017",
    "title": "Landtagswahl in Nordrhein-Westfalen 2017",
    "kind": "Landtagswahl",
    "territory": "Nordrhein-Westfalen",
    "date": "2017-05-14T00:00:00",
    "results": compile_results(parties, votes, percentages)
})


# Wahl zum Abgeordnetenhaus von Berlin 2016

parties = ["SPD", "CDU", "DIE LINKE", "GRÜNE", "AfD", "FDP", "Die PARTEI", "Tierschutzpartei", "PIRATEN", "Graue Panther", "NPD", "Gesundheitsforschung", "pro Deutschland", "ALFA", "DKP", "PSG", "BüSo", "DIE VIOLETTEN", "MENSCHLICHE WELT", "B", "ödp"]

votes = [352430, 287997, 255701, 248324, 231492, 109500, 31924, 30620, 28332, 18159, 9459, 7854, 7288, 6658, 3473, 2046, 1286, 856, 839, 636, 295]

percentages = [21.6, 17.6, 15.6, 15.2, 14.2, 6.7, 2.0, 1.9, 1.7, 1.1, 0.6, 0.5, 0.4, 0.4, 0.2, 0.1, 0.1, 0.1, 0.1, 0.0, 0.0]

# TODO: Replace WP-data with data from
# "https://wahl.tagesschau.de/wahlen/2016-09-18-LT-DE-BE/index.shtml"

missing_occasions.append({
    "url": "https://de.wikipedia.org/wiki/Landtagswahl in Berlin 2016",
    "title": "Landtagswahl in Berlin 2016",
    "kind": "Landtagswahl",
    "territory": "Berlin",
    "date": "2016-09-18T00:00:00",
    "results": compile_results(parties, votes, percentages)
})


# Europawahl in Deutschland 2014

parties = ["CDU", "SPD", "GRÜNE", "DIE LINKE", "AfD", "CSU", "FDP", "FREIE WÄHLER", "PIRATEN", "Tierschutzpartei", "NPD", "FAMILIE", "ÖDP", "Die PARTEI", "REP", "Volksabstimmung", "BP", "PBC", "PRO NRW", "AUF", "CM", "DKP", "MLPD", "BüSo", "PSG "]

votes = [8812653, 8003628, 3139274, 2168455, 2070014, 1567448, 986841, 428800, 425044, 366598, 301139, 202803, 185244, 184709, 109757, 88535, 62438, 55336, 52649, 50953, 30136, 25147, 18198, 10369, 8924]

percentages = [30.0, 27.3, 10.7, 7.4, 7.1, 5.3, 3.4, 1.5, 1.4, 1.2, 1.0, 0.7, 0.6, 0.6, 0.4, 0.3, 0.2, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.0, 0.0]

# TODO: Replace WP-data with data from
# "https://wahl.tagesschau.de/wahlen/2014-05-25-EP-DE/index.shtml"

missing_occasions.append({
    "url": "https://de.wikipedia.org/wiki/Europawahl in Deutschland 2014",
    "title": "Europawahl in Deutschland 2014",
    "kind": "Europawahl",
    "territory": "Europa",
    "date": "2014-05-25T00:00:00",
    "results": compile_results(parties, votes, percentages)
})


if __name__ == '__main__':
    with open("wahlergebnisse.json") as f:
        rv = json.load(f)

    print("Adding {} missing occasions...".format(len(missing_occasions)))

    rv += missing_occasions

    with open("wahlergebnisse.extended.json", 'w') as f:
        json.dump(rv, f, indent=2, ensure_ascii=False)
