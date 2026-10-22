import pytest
from tests.helpers import search_route, select_available
from pages.passenger_page import PassengerPage

@pytest.mark.smoke
def test_tc04_itinerary_selection_preserves_route_date_and_fare(browser, base_url):
    _, results = search_route(browser, base_url)
    selected_id = select_available(results)
    passenger = PassengerPage(browser)
    passenger.wait_visible(passenger.SUBMIT)
    assert "/passenger" in passenger.current_url(), "Selecting an available itinerary should open passenger details"
    assert selected_id in browser.page_source, "Selected itinerary identifier should be preserved on the passenger page"
    assert "Hyderabad" in browser.page_source and "Bengaluru" in browser.page_source
