import csv, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def read_csv(filename, required_columns):
    path = Path(filename)
    if not path.is_absolute(): path = ROOT / "data" / path
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if not reader.fieldnames:
                raise ValueError(f"CSV {path} has no header row")
            missing = set(required_columns) - set(reader.fieldnames)
            if missing: raise ValueError(f"CSV {path} is missing required columns: {', '.join(sorted(missing))}")
            rows = list(reader)
            if not rows: raise ValueError(f"CSV {path} contains no data rows")
            return rows
    except OSError as exc:
        raise ValueError(f"Cannot read CSV {path}: {exc}") from exc

def read_json(filename, expected_type=None):
    path = Path(filename)
    if not path.is_absolute(): path = ROOT / "data" / path
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read valid JSON from {path}: {exc}") from exc
    if expected_type and not isinstance(value, expected_type):
        raise ValueError(f"JSON {path} must contain {expected_type.__name__}")
    return value

def search_cases():
    rows = read_csv("search_cases.csv", ["case_id","origin","destination","passengers","expected_result"])
    for row in rows:
        try: row["passengers"] = int(row["passengers"])
        except ValueError as exc: raise ValueError(f"Invalid passenger count in case {row['case_id']}") from exc
    return rows

def passenger_cases():
    rows = read_csv("passenger_cases.csv", ["case_id","first_name","surname","email","phone","expected_valid"])
    for row in rows: row["expected_valid"] = row["expected_valid"].strip().lower() == "true"
    return rows
