import pytest
import requests_mock

from src.fetchers.html_fetcher import HTMLFetcher

@pytest.fixture
def html_fetcher():
    return HTMLFetcher()

def test_fetcher_returns_none_if_200_not_received(html_fetcher):
    url = "https://example.com/nonexistent"

    with requests_mock.Mocker() as m:
        m.get(url, status_code=404)
        html = html_fetcher.get_data(url)

    assert html is None

def test_fetcher_returns_expected_html_if_200_received(html_fetcher):
    url = "https://example.com"
    expected_html = "<html><body><h1>Hello, World!</h1></body></html>"

    with requests_mock.Mocker() as m:
        m.get(url, text=expected_html)
        html = html_fetcher.get_data(url)

    assert html == expected_html