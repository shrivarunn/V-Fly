import pytest
from tests.helpers import search_route
from pages.home_page import HomePage

@pytest.mark.smoke
def test_tc01_search_seeded_route(browser, base_url):
    _, results = search_route(browser, base_url)
    assert "HYD-BLR-101" in results.itinerary_ids(), "Expected seeded Hyderabad–Bengaluru itinerary was not displayed"
    assert len(results.cards()) == 3, "Hyderabad–Bengaluru should show three seeded itineraries"

@pytest.mark.regression
def test_same_origin_destination_is_rejected(browser, base_url):
    home = HomePage(browser).open(base_url)
    home.wait_visible(home.SEARCH)
    home.set_route("Hyderabad", "Hyderabad")
    home.click(home.SEARCH)
    assert home.search_error() == "Origin and destination must be different."
    assert "/results" not in home.current_url()

@pytest.mark.regression
def test_missing_route_fields_are_validated(browser, base_url):
    home = HomePage(browser).open(base_url)
    home.wait_visible(home.SEARCH)
    home.select_by_value(home.ORIGIN, "")
    home.click(home.SEARCH)
    assert home.search_error() == "Choose both origin and destination."

@pytest.mark.regression
def test_past_date_is_rejected(browser, base_url):
    from datetime import date, timedelta
    home = HomePage(browser).open(base_url); home.wait_visible(home.SEARCH)
    home.type(home.DATE, (date.today()-timedelta(days=1)).isoformat())
    home.click(home.SEARCH)
    assert home.search_error() == "Choose today or a future departure date."
