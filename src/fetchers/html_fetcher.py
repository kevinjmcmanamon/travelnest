import requests
from src.fetchers.fetcher import Fetcher


class HTMLFetcher(Fetcher):

    def get_data(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch {url}: {response.status_code}")
            return None