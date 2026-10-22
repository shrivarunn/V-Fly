import pytest
from tests.helpers import search_route

@pytest.mark.smoke
def test_tc08_sold_out_itinerary_is_not_selectable(browser, base_url):
    _, results = search_route(browser, base_url)
    card = browser.find_element("css selector", "[data-itinerary-id='HYD-BLR-103']")
    status = card.find_element("css selector", "[data-testid='itinerary-availability']").text
    button = card.find_element("css selector", "[data-testid='select-itinerary-button']")
    assert status == "Sold out", f"Expected explicit sold-out status, got {status!r}"
    assert not button.is_enabled(), "Sold-out itinerary must have a disabled selection control"
    assert "/results" in browser.current_url(), "Sold-out itinerary must not navigate"
