from dataclasses import dataclass
from typing import List, Optional
from src.parsers.factory.parser_factory import ParserFactory
from src.fetchers.fetcher import Fetcher


UNABLE_TO_PARSE_URL_CONTENTS = "Unable to parse URL contents"
UNABLE_TO_FETCH_URL_CONTENTS = "Unable to fetch URL contents"


@dataclass
class PropertyAttributes:
    url: str
    attributes: Optional[List[dict]] = None
    error: Optional[str] = None


class Scraper:

    def __init__(self, fetcher: Fetcher):
        self.fetcher = fetcher
        self.parser_factory = ParserFactory()

    def get_property_attributes(self, urls):
        result = []

        for url in urls:
            parser = self.parser_factory.get_parser(url)

            if not parser:
                self._add_parsing_error_to_result(result, url)
                continue

            data = self.fetcher.get_data(url)

            if not data:
                self._add_fetching_error_to_result(result, url)
                continue

            result.append(
                PropertyAttributes(
                    attributes=parser.get_property_attributes(data),
                    url=url,
                )
            )

        return result

    def _add_parsing_error_to_result(self, result, url):
        result.append(
            PropertyAttributes(
                attributes=None,
                url=url,
                error=UNABLE_TO_PARSE_URL_CONTENTS,
            )
        )

    def _add_fetching_error_to_result(self, result, url):
        result.append(
            PropertyAttributes(
                attributes=None,
                url=url,
                error=UNABLE_TO_FETCH_URL_CONTENTS,
            )
        )
