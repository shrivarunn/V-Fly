from datetime import datetime
from pathlib import Path
import re
from utilities.config_reader import get_settings

def save_screenshot(driver, name="screenshot"):
    folder = Path(get_settings()["screenshot_dir"])
    folder.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", name)[:100]
    path = folder / f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}_{safe}.png"
    if not driver.save_screenshot(str(path)):
        raise RuntimeError(f"WebDriver did not save screenshot to {path}")
    return str(path)
