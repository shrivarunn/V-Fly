import pytest
from tests.helpers import search_route

@pytest.mark.regression
def test_tc02_maximum_price_filter(browser, base_url):
    _, results = search_route(browser, base_url)
    results.set_max_price(850)
    results.wait_visible(results.RESULTS)
    fares = results.fares()
    assert fares, "Expected at least one itinerary at or below the selected limit"
    assert all(fare <= 850 for fare in fares), f"Fare filter leaked values over ₹850: {fares}"

def test_price_filter_can_show_empty_state(browser, base_url):
    _, results = search_route(browser, base_url)
    results.set_max_price(500)
    assert results.is_empty(), "A price cap below all route fares should show the empty state"

def test_filter_reset_restores_seeded_results(browser, base_url):
    _, results = search_route(browser, base_url)
    results.set_max_price(500)
    assert results.is_empty()
    results.reset_filters()
    assert len(results.cards()) == 3
