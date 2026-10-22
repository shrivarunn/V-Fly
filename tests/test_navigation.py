import pytest
from tests.helpers import search_route, select_available
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.passenger_page import PassengerPage

@pytest.mark.regression
def test_browser_back_and_forward_preserve_search(browser, base_url):
    _, results = search_route(browser, base_url)
    select_available(results)
    PassengerPage(browser).wait_visible(PassengerPage.SUBMIT)
    browser.back()
    SearchResultsPage(browser).wait_loaded()
    browser.forward()
    PassengerPage(browser).wait_visible(PassengerPage.SUBMIT)
    assert "/passenger" in browser.current_url()

@pytest.mark.regression
def test_direct_navigation_without_workflow_state_returns_home(browser, base_url):
    home = HomePage(browser).open(base_url + "/seats")
    home.wait_visible(home.SEARCH)
    assert browser.current_url().rstrip("/") == base_url.rstrip("/"), "A direct workflow URL without state should safely redirect home"
