import json
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://wahl.tagesschau.de/wahlen/"
DATE_FORMAT = "%d.%m.%Y"


def read_data():
    with open("data.html") as f:
        data = f.read()

    return BeautifulSoup(data, 'html.parser')


def save_result(data):
    rv = {
        "meta": {
            "source": "https://github.com/ciex/wahlergebnisse",
        },
        "data": data
    }
    with open("wahlergebnisse.json", "w") as f:
        json.dump(data, f, indent=2)


def extract(entry):
    rv = {}

    title_elem = entry.find(class_="spantitel")

    # .spantitel a.href
    href = title_elem.a['href']
    start_pos = href.rfind('/', 0, -len('/index.shtml')) + 1
    rv['url'] = BASE_URL + href[start_pos:]

    # .spantitel a span.content
    title = title_elem.a.span.text
    rv['title'] = title

    kind_endpos = title.find(' ')
    rv['kind'] = title[:kind_endpos]

    year_startpos = title.rfind(' ')
    if year_startpos == kind_endpos:
        rv['territory'] = "Deutschland" if rv['kind'] == "Bundestagswahl" \
            else "Europa"
    else:
        rv['territory'] = title[kind_endpos + 1:year_startpos]

    # .spandatum.contents
    date_text = entry.find(class_="spandatum").text[len('am\xa0'):]
    rv['date'] = datetime.strptime(date_text, DATE_FORMAT).isoformat()

    # ul.subdirectlinks li
    parties = entry.find_all('li')
    rv['results'] = dict()
    for party in parties:
        party_infos = party.find_all('span')
        name = party_infos[0].text
        votes = int(party_infos[1].text[1:-2].replace('.', ''))
        pct = float(party_infos[2].text[:-2].replace(',', '.'))

        rv['results'][name] = {
            'votes': votes,
            'pct': pct
        }

    return rv


def main():
    data = read_data()
    results = data.find_all('ul', class_='directLinks')[0]
    print("{} Wahlen gefunden".format(len(list(results))))

    rv = []
    for entry in results:
        rv.append(extract(entry))

    save_result(sorted(rv, key=lambda x: x['title']))

if __name__ == '__main__':
    main()
