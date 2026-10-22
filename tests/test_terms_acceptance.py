import pytest
from tests.helpers import complete_to_seats
from pages.terms_page import TermsPage
from pages.reservation_review_page import ReservationReviewPage

@pytest.mark.smoke
@pytest.mark.workflow
def test_tc07_terms_must_be_accepted_before_review(browser, base_url):
    _, seats = complete_to_seats(browser, base_url)
    seats.choose_first_available()
    seats.continue_to_terms()
    terms = TermsPage(browser).wait_loaded()
    assert not terms.continue_enabled(), "Terms continue must start disabled"
    terms.accept_terms()
    assert terms.continue_enabled(), "Accepting terms should enable continue"
    terms.continue_to_review()
    assert ReservationReviewPage(browser).wait_loaded()

@pytest.mark.regression
def test_terms_modal_opens_and_closes(browser, base_url):
    _, seats = complete_to_seats(browser, base_url)
    seats.choose_first_available(); seats.continue_to_terms()
    terms = TermsPage(browser).wait_loaded()
    terms.open_modal()
    assert terms.find(terms.DIALOG).is_displayed()
    terms.close_modal()
    assert not browser.find_elements(*terms.DIALOG)

@pytest.mark.regression
def test_terms_iframe_can_be_entered_and_left(browser, base_url):
    _, seats = complete_to_seats(browser, base_url)
    seats.choose_first_available(); seats.continue_to_terms()
    terms = TermsPage(browser).wait_loaded()
    text = terms.read_iframe_terms()
    assert "fictional demo terms" in text
    assert terms.find(terms.ACCEPT).is_displayed(), "Should return to default document after iframe interaction"
