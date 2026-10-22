from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class SeatSelectionPage(BasePage):
    MAP = (By.ID, "seat-map")
    SEAT = (By.CSS_SELECTOR, "[data-testid='seat']")
    SELECTED_LIST = (By.ID, "selected-seat-list")
    CONTINUE = (By.ID, "seat-continue-button")

    def wait_loaded(self):
        self.wait_visible(self.MAP)
        return self

    def choose_seat(self, seat_id):
        self.click((By.CSS_SELECTOR, f"[data-seat-id='{seat_id}']:not(:disabled)"))

    def choose_first_available(self):
        for seat in self.driver.find_elements(*self.SEAT):
            if seat.is_enabled() and seat.get_attribute("aria-pressed") != "true":
                seat.click()
                return seat.get_attribute("data-seat-id")
        raise AssertionError("No available seat was found")

    def selected_seats(self):
        return [e.text for e in self.driver.find_elements(By.CSS_SELECTOR, "#selected-seat-list span")]

    def continue_to_terms(self):
        self.click(self.CONTINUE)

    def continue_enabled(self):
        return self.find(self.CONTINUE).is_enabled()
