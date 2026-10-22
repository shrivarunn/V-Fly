import pytest
from tests.helpers import search_route
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utilities.data_reader import search_cases, passenger_cases
from pages.passenger_page import PassengerPage
from tests.helpers import select_available

@pytest.mark.regression
@pytest.mark.parametrize("case", search_cases(), ids=lambda case: case["case_id"])
def test_search_cases_from_csv(browser, base_url, case):
    _, results = search_route(browser, base_url, case["origin"], case["destination"], case["passengers"])
    if case["expected_result"] == "results":
        assert results.cards(), f"{case['case_id']}: expected seeded results"
    else:
        assert results.is_empty(), f"{case['case_id']}: expected no results"

@pytest.mark.regression
@pytest.mark.parametrize("case", passenger_cases(), ids=lambda case: case["case_id"])
def test_passenger_cases_from_csv(browser, base_url, case):
    _, results = search_route(browser, base_url)
    select_available(results)
    page = PassengerPage(browser); page.wait_visible(page.SUBMIT)
    page.fill_passenger(case["first_name"], case["surname"], case["email"], case["phone"])
    page.submit()
    if case["expected_valid"]:
        assert "/seats" in page.current_url(), f"{case['case_id']}: valid passenger should advance"
    else:
        assert "/passenger" in page.current_url(), f"{case['case_id']}: invalid passenger should remain on form"
