from datetime import datetime
from pathlib import Path
import pytest
from utilities.config_reader import get_settings
from utilities.driver_factory import create_driver
from utilities.logger import get_logger
from utilities.screenshot_utils import save_screenshot

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=None, choices=["chrome","edge"], help="Browser: chrome or edge")
    parser.addoption("--base-url", action="store", default=None, help="TripTrail base URL")
    parser.addoption("--headless", action="store_true", default=None, help="Run browser headless")
    parser.addoption("--wait-timeout", action="store", type=int, default=None, help="Explicit wait timeout in seconds")

@pytest.fixture(scope="session")
def settings(request):
    values = get_settings({
        "browser": request.config.getoption("--browser"),
        "base_url": request.config.getoption("--base-url"),
        "headless": request.config.getoption("--headless"),
        "explicit_wait_timeout": request.config.getoption("--wait-timeout")
    })
    Path(values["screenshot_dir"]).mkdir(parents=True, exist_ok=True)
    Path(values["log_dir"]).mkdir(parents=True, exist_ok=True)
    Path(values["html_report"]).parent.mkdir(parents=True, exist_ok=True)
    return values

@pytest.fixture
def browser(settings, request):
    logger = get_logger()
    driver = create_driver(settings["browser"], settings["headless"])
    driver.set_window_size(1440, 1000)
    request.node._triptrail_driver = driver
    logger.info("Starting browser=%s test=%s base_url=%s", settings["browser"], request.node.nodeid, settings["base_url"])
    yield driver
    logger.info("Closing browser for test=%s", request.node.nodeid)
    try: driver.quit()
    except Exception as exc: logger.warning("Browser cleanup issue: %s", exc)

@pytest.fixture
def base_url(settings):
    return settings["base_url"]

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = getattr(item, "_triptrail_driver", None)
        logger = get_logger()
        if driver:
            try:
                path = save_screenshot(driver, item.nodeid)
                logger.error("Failure screenshot saved: %s", path)
                report.sections.append(("TripTrail screenshot", path))
            except Exception as exc:
                logger.error("Screenshot capture failed without masking test failure: %s", exc)
        else:
            logger.error("No browser instance available for failure screenshot.")
