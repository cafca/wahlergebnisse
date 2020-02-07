import requests

URL_OVERVIEW = "https://wahl.tagesschau.de/wahlen/chronologie/chronologie.shtml"

def download_url(url):
    print(f"Downloading {url}...")

def parse_election_urls(raw_overview):
    print("Parsing election urls...")
    return []

def extract_results(raw_election_data):
    print("Extracting results from election data...")
    return {}

def save_result(data):
    print("Saving results to disk...")

def main():
    raw_overview = download_url(URL_OVERVIEW)

    election_urls = parse_election_urls(raw_overview)
    print(len(election_urls), "Wahlen gefunden")

    rv = []
    for election_url in election_urls:
        raw_election = download_url(election_url)
        rv.append(extract_results(raw_election))

    save_result(rv)


if __name__ == "__main__":
    main()
