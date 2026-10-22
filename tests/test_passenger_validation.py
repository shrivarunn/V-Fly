import pytest
from tests.helpers import complete_to_passenger
from pages.passenger_page import PassengerPage

@pytest.mark.smoke
def test_tc05_missing_surname_displays_error_and_does_not_advance(browser, base_url):
    _, page = complete_to_passenger(browser, base_url)
    page.fill_passenger("Anju", "", "anju.demo@example.test", "9000000001")
    page.submit()
    assert page.has_surname_error(), "Missing surname should display a field-level validation error"
    assert "Surname is required" in page.surname_error()
    assert "/passenger" in page.current_url(), "Invalid passenger form must not advance"

@pytest.mark.regression
def test_invalid_email_is_rejected(browser, base_url):
    _, page = complete_to_passenger(browser, base_url)
    page.fill_passenger("Anju", "Sharma", "not-an-email", "9000000001")
    page.submit()
    assert "/passenger" in page.current_url()
    assert browser.find_elements("css selector", ".field-error"), "Invalid email should show validation feedback"
