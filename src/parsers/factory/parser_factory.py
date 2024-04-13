from src.parsers.airbnb_parser import AirBnBParser


class ParserFactory:
    def get_parser(self, url):
        if "airbnb.co.uk" in url:
            return AirBnBParser()
        else:
            print(f"Unable to find parser for URL {url}")
            return None