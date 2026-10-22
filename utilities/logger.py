import logging
from pathlib import Path
from utilities.config_reader import get_settings

def get_logger(name="triptrail"):
    settings = get_settings()
    folder = Path(settings["log_dir"]); folder.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        file_handler = logging.FileHandler(folder / "triptrail.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        logger.addHandler(file_handler); logger.addHandler(stream)
    return logger
