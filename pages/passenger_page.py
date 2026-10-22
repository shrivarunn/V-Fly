from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class PassengerPage(BasePage):
    FIRST = (By.ID, "passenger-first-name")
    SURNAME = (By.ID, "passenger-surname")
    EMAIL = (By.ID, "passenger-email")
    PHONE = (By.ID, "passenger-phone")
    SUBMIT = (By.ID, "passenger-form-submit")
    SURNAME_ERROR = (By.ID, "surname-error")

    def fill_passenger(self, first_name="Anju", surname="Sharma", email="anju.demo@example.test", phone="9000000001"):
        self.type(self.FIRST, first_name)
        self.type(self.SURNAME, surname)
        self.type(self.EMAIL, email)
        self.type(self.PHONE, phone)
        return self

    def submit(self):
        self.click(self.SUBMIT)

    def surname_error(self):
        return self.text(self.SURNAME_ERROR)

    def has_surname_error(self):
        return bool(self.driver.find_elements(*self.SURNAME_ERROR))

    def continue_with_passenger(self, first_name="Anju", surname="Sharma", email="anju.demo@example.test", phone="9000000001"):
        self.fill_passenger(first_name, surname, email, phone)
        self.submit()
