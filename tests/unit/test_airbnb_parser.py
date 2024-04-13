import pytest

from src.parsers.parser import NOT_FOUND
from src.parsers.airbnb_parser import AirBnBParser


@pytest.fixture
def parser():
    return AirBnBParser()


@pytest.fixture
def empty_html_content():
    return """
    <html>
    <head></head>
        <body></body>
    </html>
    """


@pytest.fixture
def full_html_content():
    return """
    <html>
        <head></head>
        <script id="data-injector-instances" type="application/json">
            {
                "listingTitle": "Example Property Name",
                "propertyType": "Tiny home",
                "ogTitle": "Tiny home in Mickleton · ★4.90 · 4 bedrooms · 1 bed · 3 bathrooms",
                "seeAllAmenitiesGroups": [
                    {
                        "title": "Category A",
                        "amenities": [
                            {
                                "title": "First aid kit"
                            },
                            {
                                "title": "Fridge"
                            }
                        ]
                    },
                    {
                        "title": "Category B",
                        "amenities": [
                            {
                                "title": "Oven"
                            }
                        ]
                    }
                ]
            }
        </script>
    </html>
    """


@pytest.fixture
def html_with_unavailable_amenities():
    return """
    <html>
        <head></head>
        <script id="data-injector-instances" type="application/json">
            {
                "seeAllAmenitiesGroups": [
                    {
                        "title": "Not included",
                        "amenities": [
                            {
                                "title": "First aid kit"
                            },
                            {
                                "title": "Fridge"
                            }
                        ]
                    },
                    {
                        "title": "Category B",
                        "amenities": [
                            {
                                "title": "Oven"
                            }
                        ]
                    }
                ]
            }
        </script>
    </html>
    """


def test_empty_string_raises_exception(parser):
    with pytest.raises(Exception):
        parser.get_property_attributes("")


def test_content_of_none_raises_exception(parser):
    with pytest.raises(Exception):
        parser.get_property_attributes(None)


def test_all_attributes_return_value_of_not_found_if_not_present_in_html(
    parser, empty_html_content
):
    assert parser.get_property_attributes(empty_html_content) == {
        "name": NOT_FOUND,
        "type": NOT_FOUND,
        "num_bedrooms": NOT_FOUND,
        "num_bathrooms": NOT_FOUND,
        "amenities": NOT_FOUND,
    }


def test_expected_dict_returned_when_content_contains_all_required_info(
    parser, full_html_content
):
    assert parser.get_property_attributes(full_html_content) == {
        "name": "Example Property Name",
        "type": "Tiny home",
        "num_bedrooms": 4,
        "num_bathrooms": 3,
        "amenities": ["First aid kit", "Fridge", "Oven"],
    }


def test_amenities_marked_as_not_included_are_not_returned(
    parser, html_with_unavailable_amenities
):
    assert parser.get_property_attributes(html_with_unavailable_amenities) == {
        "name": NOT_FOUND,
        "type": NOT_FOUND,
        "num_bedrooms": NOT_FOUND,
        "num_bathrooms": NOT_FOUND,
        "amenities": ["Oven"],
    }
