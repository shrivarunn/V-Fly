from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class TermsPage(BasePage):
    ACCEPT = (By.ID, "terms-accept-checkbox")
    CONTINUE = (By.ID, "terms-continue-button")
    OPEN_MODAL = (By.XPATH, "//button[contains(., 'Read terms and conditions')]")
    DIALOG = (By.ID, "terms-dialog")
    IFRAME = (By.CSS_SELECTOR, "[data-testid='terms-iframe']")

    def wait_loaded(self):
        self.wait_visible(self.ACCEPT)
        return self

    def accept_terms(self):
        checkbox = self.find(self.ACCEPT)
        if not checkbox.is_selected():
            checkbox.click()

    def continue_enabled(self):
        return self.find(self.CONTINUE).is_enabled()

    def continue_to_review(self):
        self.click(self.CONTINUE)

    def open_modal(self):
        self.click(self.OPEN_MODAL)
        self.wait_visible(self.DIALOG)

    def close_modal(self):
        self.click((By.CSS_SELECTOR, ".terms-modal .button"))

    def read_iframe_terms(self):
        self.click((By.XPATH, "//button[contains(., 'Show iframe terms example')]"))
        self.switch_to_frame(self.IFRAME)
        text = self.driver.find_element(By.TAG_NAME, "body").text
        self.leave_frame()
        return text
