from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.config_reader import get_settings

class HomePage(BasePage):
    ORIGIN = (By.ID, "origin-input")
    DESTINATION = (By.ID, "destination-input")
    DATE = (By.ID, "departure-date-input")
    PASSENGERS = (By.ID, "passenger-count-select")
    SWAP = (By.ID, "swap-route-button")
    SEARCH = (By.ID, "search-submit-button")
    ERROR = (By.CSS_SELECTOR, "[data-testid='search-error']")

    def load(self):
        self.open(get_settings()["base_url"])
        self.wait_visible(self.SEARCH)
        return self

    def search(self, origin="Hyderabad", destination="Bengaluru", date=None, passengers=1):
        from datetime import date as date_type
        date = date or date_type.today().isoformat()
        self.select_by_visible_text(self.ORIGIN, origin)
        self.select_by_visible_text(self.DESTINATION, destination)
        self.type(self.DATE, date)
        self.select_by_value(self.PASSENGERS, str(passengers))
        self.click(self.SEARCH)
        return self

    def swap_route(self):
        self.click(self.SWAP)

    def search_error(self):
        return self.text(self.ERROR)

    def set_route(self, origin, destination):
        self.select_by_visible_text(self.ORIGIN, origin)
        self.select_by_visible_text(self.DESTINATION, destination)
