import json

with open('wahlergebnisse.json') as f:
    data = json.load(f)

df = filter(lambda x: int(x['date'][:4]) >= 2002, data)

for entry in df:
    print(entry['title'])
