from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ReservationReviewPage(BasePage):
    SUMMARY = (By.ID, "reservation-summary")
    ROUTE = (By.ID, "summary-route")
    PASSENGERS = (By.ID, "summary-passengers")
    SEATS = (By.ID, "summary-seats")
    TOTAL = (By.ID, "summary-total")

    def wait_loaded(self):
        self.wait_visible(self.SUMMARY)
        return self

    def route_text(self):
        return self.text(self.ROUTE)

    def passenger_text(self):
        return self.text(self.PASSENGERS)

    def seats_text(self):
        return self.text(self.SEATS)

    def total_text(self):
        return self.text(self.TOTAL)
