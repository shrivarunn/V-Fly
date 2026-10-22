from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from utilities.config_reader import get_settings

def create_driver(browser=None, headless=None):
    settings = get_settings({"browser": browser, "headless": headless})
    selected = settings["browser"]
    try:
        if selected == "chrome":
            options = ChromeOptions()
            if settings["headless"]: options.add_argument("--headless=new")
            options.add_argument("--window-size=1440,1000")
            options.add_argument("--disable-notifications")
            options.add_argument("--no-first-run")
            driver = webdriver.Chrome(options=options)
        elif selected == "edge":
            options = EdgeOptions()
            if settings["headless"]: options.add_argument("--headless=new")
            options.add_argument("--window-size=1440,1000")
            options.add_argument("--disable-notifications")
            driver = webdriver.Edge(options=options)
        else:
            raise ValueError(f"Unsupported browser: {selected}")
        driver.set_page_load_timeout(settings["page_load_timeout"])
        return driver
    except Exception as exc:
        raise RuntimeError(
            f"Unable to start {selected}. Install/update that browser and a compatible Selenium version; "
            f"Selenium Manager normally resolves the driver automatically. Original error: {exc}"
        ) from exc
