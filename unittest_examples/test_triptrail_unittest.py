import unittest
from pages.home_page import HomePage
from utilities.driver_factory import create_driver
from utilities.config_reader import get_settings

class TestTripTrailUnittest(unittest.TestCase):
    """Standalone unittest example. Class-level lifecycle shares one browser across this class;
    pytest's function-scoped fixture instead creates an isolated browser per test by default."""

    @classmethod
    def setUpClass(cls):
        cls.settings = get_settings()
        cls.driver = create_driver(cls.settings["browser"], cls.settings["headless"])
        cls.driver.set_window_size(1280, 900)

    @classmethod
    def tearDownClass(cls):
        if getattr(cls, "driver", None):
            cls.driver.quit()

    def test_homepage_title_and_search_control(self):
        page = HomePage(self.driver).open(self.settings["base_url"])
        page.wait_visible(page.SEARCH)
        self.assertIn("V-Fly", page.title())
        self.assertTrue(page.find(page.SEARCH).is_displayed(), "Search button should be visible")

if __name__ == "__main__":
    unittest.main(verbosity=2)
