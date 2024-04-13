import pytest

from src.scraper import (
    UNABLE_TO_FETCH_URL_CONTENTS,
    UNABLE_TO_PARSE_URL_CONTENTS,
    Scraper,
)
from src.fetchers.html_fetcher import HTMLFetcher


@pytest.fixture
def html_fetcher():
    return HTMLFetcher()


@pytest.fixture
def scraper(html_fetcher):
    return Scraper(html_fetcher)


@pytest.fixture
def expected_attributes_1():
    return {
        "name": "Little Country Houses - Poppy's Pad with hot tub",
        "type": "Tiny home",
        "num_bedrooms": 1,
        "num_bathrooms": 1,
        "amenities": [
            "Indoor fireplace",
            "Heating",
            "Smoke alarm",
            "Fire extinguisher",
            "First aid kit",
            "Kitchen",
            "Fridge",
            "Cooking basics",
            "Oven",
            "Patio or balcony",
            "BBQ grill",
            "Free parking on premises",
            "Hot tub",
            "Self check-in",
            "Lockbox",
        ],
    }


@pytest.fixture
def expected_attributes_2():
    return {
        "name": "Lovely loft on the beautiful North Norfolk Coast",
        "type": "Entire guest house",
        "num_bedrooms": 1,
        "num_bathrooms": 1,
        "amenities": [
            "Hair dryer",
            "Shampoo",
            "Body soap",
            "Hot water",
            "Shower gel",
            "Essentials",
            "Hangers",
            "Bed linen",
            "Clothes storage: wardrobe",
            "Portable fans",
            "Heating",
            "Smoke alarm",
            "Carbon monoxide alarm",
            "Wifi",
            "Fridge",
            "Microwave",
            "Dishes and cutlery",
            "Mini fridge",
            "Kettle",
            "Wine glasses",
            "Coffee",
            "Private entrance",
            "Garden",
            "Free parking on premises",
        ],
    }


def test_scraper_returns_as_expected_when_unknown_url(scraper):
    urls = ["https://www.unknown.co.uk/rooms/abc"]

    result = scraper.get_property_attributes(urls)

    assert len(result) == 1

    assert result[0].error == UNABLE_TO_PARSE_URL_CONTENTS
    assert result[0].url == urls[0]
    assert result[0].attributes == None


def test_scraper_returns_as_expected_when_url_does_not_return_200(scraper):
    urls = ["https://www.airbnb.co.uk/rooms/33571269"]  # returns 404

    result = scraper.get_property_attributes(urls)

    assert len(result) == 1

    assert result[0].error == UNABLE_TO_FETCH_URL_CONTENTS
    assert result[0].url == urls[0]
    assert result[0].attributes == None


def test_scraper_returns_expected_property_attributes_for_single_property(
    scraper, expected_attributes_1
):
    urls = ["https://www.airbnb.co.uk/rooms/20669368"]

    result = scraper.get_property_attributes(urls)

    assert len(result) == 1

    assert result[0].error == None
    assert result[0].url == urls[0]
    assert result[0].attributes == expected_attributes_1


def test_scraper_returns_expected_property_attributes_for_multiple_properties(
    scraper, expected_attributes_1, expected_attributes_2
):
    urls = [
        "https://www.airbnb.co.uk/rooms/33571269",  # returns 404
        "https://www.airbnb.co.uk/rooms/20669368",
        "https://www.airbnb.co.uk/rooms/50633275",
    ]

    result = scraper.get_property_attributes(urls)

    assert len(result) == 3

    assert result[0].error == UNABLE_TO_FETCH_URL_CONTENTS
    assert result[0].url == urls[0]
    assert result[0].attributes == None

    assert result[1].error == None
    assert result[1].url == urls[1]
    assert result[1].attributes == expected_attributes_1

    assert result[2].error == None
    assert result[2].url == urls[2]
    assert result[2].attributes == expected_attributes_2
