from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class SearchResultsPage(BasePage):
    RESULTS = (By.ID, "results-list")
    CARDS = (By.CSS_SELECTOR, "[data-testid='itinerary-card']")
    PRICE_FILTER = (By.ID, "price-filter")
    SORT = (By.ID, "departure-sort")
    EMPTY = (By.ID, "empty-results")

    def wait_loaded(self):
        self.wait_visible(self.RESULTS)
        return self

    def cards(self):
        self.wait_visible(self.RESULTS)
        return self.driver.find_elements(*self.CARDS)

    def itinerary_ids(self):
        return [c.get_attribute("data-itinerary-id") for c in self.cards()]

    def fares(self):
        return [int(c.find_element(By.CSS_SELECTOR, "[data-testid='itinerary-fare']").get_attribute("data-fare")) for c in self.cards()]

    def departure_times(self):
        return [c.find_element(By.CSS_SELECTOR, "[data-testid='itinerary-departure-time']").text for c in self.cards()]

    def availability_for(self, itinerary_id):
        card = self.driver.find_element(By.CSS_SELECTOR, f"[data-itinerary-id='{itinerary_id}']")
        return card.find_element(By.CSS_SELECTOR, "[data-testid='itinerary-availability']").text

    def select_itinerary(self, itinerary_id=None):
        cards = self.cards()
        if itinerary_id:
            card = self.driver.find_element(By.CSS_SELECTOR, f"[data-itinerary-id='{itinerary_id}']")
        else:
            card = next(c for c in cards if c.find_element(By.CSS_SELECTOR, "[data-testid='select-itinerary-button']").is_enabled())
        button = card.find_element(By.CSS_SELECTOR, "[data-testid='select-itinerary-button']")
        button.click()
        return self

    def set_max_price(self, price):
        self.wait_visible(self.PRICE_FILTER)
        self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input',{bubbles:true})); arguments[0].dispatchEvent(new Event('change',{bubbles:true}));", self.find(self.PRICE_FILTER), str(price))

    def sort_by(self, value):
        self.select_by_value(self.SORT, value)

    def reset_filters(self):
        self.click((By.CSS_SELECTOR, ".reset-button"))

    def is_empty(self):
        return bool(self.driver.find_elements(*self.EMPTY))
