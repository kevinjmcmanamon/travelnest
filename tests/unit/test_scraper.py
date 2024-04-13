import pytest
from unittest.mock import MagicMock
from src.fetchers.fetcher import Fetcher
from src.parsers.parser import Parser
from src.scraper import (
    Scraper,
    PropertyAttributes,
    UNABLE_TO_PARSE_URL_CONTENTS,
    UNABLE_TO_FETCH_URL_CONTENTS,
)


class MockFetcher(Fetcher):
    def get_data(self, url):
        return f"Mocked data for {url}"


class MockParser(Parser):
    def get_property_attributes(url):
        return {
            "name": "Test name",
            "num_bedrooms": 3,
        }


@pytest.fixture
def scraper():
    fetcher = MockFetcher()
    return Scraper(fetcher)


def test_error_received_if_url_content_cannot_be_parsed(scraper):
    urls = ["http://unknown.co.uk/1", "http://unknown.co.uk/2"]

    expected_attributes = [
        PropertyAttributes(
            url=urls[0], attributes=None, error=UNABLE_TO_PARSE_URL_CONTENTS
        ),
        PropertyAttributes(
            url=urls[1], attributes=None, error=UNABLE_TO_PARSE_URL_CONTENTS
        ),
    ]

    attributes = scraper.get_property_attributes(urls)

    assert attributes == expected_attributes


def test_error_received_if_url_content_cannot_be_fetched(scraper):
    urls = ["http://airbnb.co.uk/1", "http://airbnb.co.uk/2"]
    scraper.fetcher.get_data = MagicMock(return_value=None)

    expected_attributes = [
        PropertyAttributes(
            url=urls[0], attributes=None, error=UNABLE_TO_FETCH_URL_CONTENTS
        ),
        PropertyAttributes(
            url=urls[1], attributes=None, error=UNABLE_TO_FETCH_URL_CONTENTS
        ),
    ]

    attributes = scraper.get_property_attributes(urls)

    assert attributes == expected_attributes


def test_get_property_attributes_success(scraper):
    urls = ["http://airbnb.co.uk/1"]

    scraper.parser_factory.get_parser = MagicMock(return_value=MockParser)

    expected_attributes = [
        PropertyAttributes(
            url=urls[0],
            attributes={
                "name": "Test name",
                "num_bedrooms": 3,
            },
        )
    ]

    attributes = scraper.get_property_attributes(urls)

    assert attributes == expected_attributes
