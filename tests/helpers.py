from datetime import date
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.passenger_page import PassengerPage
from pages.seat_selection_page import SeatSelectionPage
from pages.terms_page import TermsPage
from pages.reservation_review_page import ReservationReviewPage

def future_date():
    return date.today().isoformat()

def search_route(browser, base_url, origin="Hyderabad", destination="Bengaluru", passengers=1):
    home = HomePage(browser).open(base_url)
    home.wait_visible(home.SEARCH)
    home.search(origin, destination, future_date(), passengers)
    results = SearchResultsPage(browser).wait_loaded()
    return home, results

def select_available(results):
    ids = results.itinerary_ids()
    for itinerary_id in ids:
        card = results.driver.find_element("css selector", f"[data-itinerary-id='{itinerary_id}']")
        button = card.find_element("css selector", "[data-testid='select-itinerary-button']")
        if button.is_enabled():
            results.select_itinerary(itinerary_id)
            return itinerary_id
    raise AssertionError("Expected at least one selectable itinerary")

def complete_to_passenger(browser, base_url, origin="Hyderabad", destination="Bengaluru", passengers=1):
    _, results = search_route(browser, base_url, origin, destination, passengers)
    itinerary_id = select_available(results)
    passenger = PassengerPage(browser)
    passenger.wait_visible(passenger.SUBMIT)
    return itinerary_id, passenger

def complete_to_seats(browser, base_url, passengers=1):
    itinerary_id, passenger = complete_to_passenger(browser, base_url, passengers=passengers)
    for idx in range(passengers):
        if idx == 0:
            passenger.fill_passenger("Anju", "Sharma", "anju.demo@example.test", "9000000001")
        else:
            # Fill additional passenger fields through the form's stable testid locators.
            from selenium.webdriver.common.by import By
            blocks = browser.find_elements(By.CSS_SELECTOR, ".passenger-card")
            fields = blocks[idx].find_elements(By.CSS_SELECTOR, "input")
            for field, value in zip(fields, [f"Demo{idx+1}", f"Person{idx+1}", f"demo{idx+1}@example.test", f"900000000{idx+1}"]):
                field.send_keys(value)
    passenger.submit()
    seats = SeatSelectionPage(browser).wait_loaded()
    return itinerary_id, seats
