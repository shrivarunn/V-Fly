import pytest
from tests.helpers import complete_to_seats
from pages.terms_page import TermsPage
from pages.reservation_review_page import ReservationReviewPage
from pages.seat_selection_page import SeatSelectionPage

@pytest.mark.smoke
@pytest.mark.workflow
def test_tc06_selected_seat_appears_in_reservation_review(browser, base_url):
    _, seats = complete_to_seats(browser, base_url)
    chosen = seats.choose_first_available()
    assert seats.continue_enabled(), "Seat continue should enable after required seat count is selected"
    seats.continue_to_terms()
    terms = TermsPage(browser).wait_loaded()
    terms.accept_terms()
    terms.continue_to_review()
    review = ReservationReviewPage(browser).wait_loaded()
    assert chosen in review.seats_text(), f"Selected seat {chosen} should be shown in review"

@pytest.mark.regression
def test_occupied_seat_is_disabled(browser, base_url):
    _, seats = complete_to_seats(browser, base_url)
    occupied = browser.find_element("css selector", "[data-seat-id='A2']")
    assert not occupied.is_enabled(), "Occupied seats must be disabled"

@pytest.mark.regression
def test_cannot_continue_without_required_seats(browser, base_url):
    _, seats = complete_to_seats(browser, base_url, passengers=2)
    assert not seats.continue_enabled(), "Two passengers must select two seats before continuing"

@pytest.mark.regression
def test_multiple_passengers_can_select_distinct_seats(browser, base_url):
    _, seats = complete_to_seats(browser, base_url, passengers=2)
    first = seats.choose_first_available()
    second = seats.choose_first_available()
    assert first != second
    assert len(seats.selected_seats()) == 2
    seats.continue_to_terms()
    assert "/terms" in seats.current_url()
