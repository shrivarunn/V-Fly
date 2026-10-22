from datetime import datetime
import pytest
from tests.helpers import search_route

@pytest.mark.regression
def test_tc03_departure_sort_is_fully_ascending(browser, base_url):
    _, results = search_route(browser, base_url)
    results.sort_by("earliest")
    values = [datetime.strptime(value, "%H:%M").time() for value in results.departure_times()]
    assert values == sorted(values), f"Departure times are not fully ascending: {values}"

def test_sort_by_price_low_to_high(browser, base_url):
    _, results = search_route(browser, base_url)
    results.sort_by("low")
    fares = results.fares()
    assert fares == sorted(fares), f"Prices are not ascending: {fares}"

def test_sort_by_price_high_to_low(browser, base_url):
    _, results = search_route(browser, base_url)
    results.sort_by("high")
    fares = results.fares()
    assert fares == sorted(fares, reverse=True), f"Prices are not descending: {fares}"

def test_latest_departure_sort(browser, base_url):
    _, results = search_route(browser, base_url)
    results.sort_by("latest")
    values = [datetime.strptime(value, "%H:%M").time() for value in results.departure_times()]
    assert values == sorted(values, reverse=True)
