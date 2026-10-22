# V-Fly — Travel Search and Reservation (Academic Demo)

V-Fly is a fictional travel search and reservation workflow built to demonstrate a React/TypeScript frontend alongside a separate Python Selenium WebDriver 4 + pytest automation framework. It is a complete local academic project, not a real travel service.

> **Demo-only restriction:** no real reservation, payment, ticket issuance, external booking API, cloud database, or real passenger data is used. Enter synthetic details only. The final page is a local simulated review.

## Features

- Responsive route search, seeded itinerary results, numeric price filtering and time/price sorting.
- Passenger validation, seat map with available/selected/occupied states, terms modal + optional iframe, and final review.
- Workflow state persisted in browser session storage, browser Back/Forward support, and guarded direct navigation.
- Page Object Model, explicit waits, Chrome/Edge driver factory, data-driven CSV/JSON, screenshot-on-failure, logging and pytest-html.
- A separate `unittest.TestCase` example.

## Technology

- Frontend: React 18, TypeScript, Vite, Tailwind CSS, React Router.
- Automation: Python 3.10+, Selenium 4, pytest, pytest-html, standard library.
- Recommended: Node.js 20 LTS or newer, npm 10+, Chrome or Microsoft Edge updated to a current stable version.

## Repository structure

```text
TripTrail/
├── app/                         # React/TypeScript/Vite frontend
│   └── src/{components,data,hooks,lib,pages,routes,styles,types}/
├── config/settings.json         # Runtime defaults
├── data/                        # Synthetic CSV and JSON datasets
├── pages/                       # Selenium Page Objects and BasePage
├── tests/                       # pytest acceptance, negative and data-driven tests
├── unittest_examples/           # Independent unittest example
├── utilities/                   # Config, driver, waits, data, screenshots, logging
├── artifacts/screenshots/        # Failure screenshots
├── artifacts/logs/               # Framework log
├── reports/                      # Self-contained HTML report
├── conftest.py
├── pytest.ini
├── requirements.txt
└── LOCATOR_INVENTORY.md
```

## Setup: Windows PowerShell

Open one terminal in the repository root (`TripTrail`).

### 1. Install prerequisites
Install Python 3.10+ and Node.js 20 LTS+ from their official installers. Install/update Chrome or Microsoft Edge. Verify:

```powershell
python --version
node --version
npm --version
```

### 2. Install frontend dependencies

```powershell
cd app
npm install
cd ..
```

### 3. Create a Python virtual environment and install automation dependencies

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` in that terminal, or invoke `.venv\Scripts\python.exe` directly.

### 4. Start the website

From the repository root:

```powershell
cd app
npm run dev
```

Vite prints the actual local URL, normally `http://127.0.0.1:5173`. Keep this terminal open. In a second terminal, return to the repository root and activate the virtual environment.

### 5. Configure URL/browser

Edit `config/settings.json`, or use environment variables:

```powershell
$env:TRIPTRAIL_BASE_URL = "http://127.0.0.1:5173"
$env:TRIPTRAIL_BROWSER = "chrome"
$env:TRIPTRAIL_HEADLESS = "false"
$env:TRIPTRAIL_WAIT_TIMEOUT = "10"
```

Pytest flags override settings where supplied: `--base-url`, `--browser`, `--headless`, and `--wait-timeout`.

### 6. Run tests

```powershell
# Complete suite (website must already be running)
pytest

# Self-contained HTML report
pytest --html=reports/pytest-report.html --self-contained-html

# One test
pytest tests/test_search.py::test_tc01_search_seeded_route

# Eight core acceptance scenarios
pytest tests/test_search.py::test_tc01_search_seeded_route `
       tests/test_price_filter.py::test_tc02_maximum_price_filter `
       tests/test_sorting.py::test_tc03_departure_sort_is_fully_ascending `
       tests/test_itinerary_selection.py::test_tc04_itinerary_selection_preserves_route_date_and_fare `
       tests/test_passenger_validation.py::test_tc05_missing_surname_displays_error_and_does_not_advance `
       tests/test_seat_selection.py::test_tc06_selected_seat_appears_in_reservation_review `
       tests/test_terms_acceptance.py::test_tc07_terms_must_be_accepted_before_review `
       tests/test_sold_out.py::test_tc08_sold_out_itinerary_is_not_selectable

# Chrome, visible
pytest --browser=chrome

# Edge, visible
pytest --browser=edge

# Headless Chrome
pytest --browser=chrome --headless

# Alternate URL and wait timeout
pytest --base-url=http://127.0.0.1:5173 --wait-timeout=15
```

### 7. unittest comparison

With the website running:

```powershell
python -m unittest unittest_examples.test_triptrail_unittest -v
```

The example uses `setUpClass`/`tearDownClass` and one class-scoped browser. The pytest suite uses a fresh function-scoped browser for test isolation.

## macOS/Linux equivalents

```bash
cd app && npm install
cd ..
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd app && npm run dev
# In another terminal from repository root:
pytest --browser=chrome --headless
python -m unittest unittest_examples.test_triptrail_unittest -v
```

## Browser and driver management

The driver factory uses Selenium Manager through `webdriver.Chrome()` / `webdriver.Edge()` and does not hardcode driver paths. Selenium Manager may download or resolve a compatible driver on first run, so the machine needs internet access for first-time resolution in some environments. A compatible installed browser is required. If startup fails, update Selenium and the browser, confirm the browser launches manually, and inspect the exception printed by the driver factory. Firefox is not implemented in this version.

## Configuration reference

`config/settings.json` contains:
- `base_url`: local Vite URL.
- `browser`: `chrome` or `edge`.
- `explicit_wait_timeout`, `page_load_timeout`: positive seconds.
- `headless`: boolean.
- `screenshot_dir`, `log_dir`, `html_report`: output locations.

Environment overrides: `TRIPTRAIL_BASE_URL`, `TRIPTRAIL_BROWSER`, `TRIPTRAIL_WAIT_TIMEOUT`, `TRIPTRAIL_PAGELOAD_TIMEOUT`, `TRIPTRAIL_HEADLESS`, `TRIPTRAIL_SCREENSHOT_DIR`, `TRIPTRAIL_LOG_DIR`, `TRIPTRAIL_HTML_REPORT`.

## Data-driven testing

- `data/search_cases.csv`: `case_id,origin,destination,passengers,expected_result`.
- `data/passenger_cases.csv`: `case_id,first_name,surname,email,phone,expected_valid`.
- `data/itinerary_data.json`: the seeded itinerary inventory mirrored by the frontend.
- `data/seat_data.json`: seat rows, occupied seats and selection rule.

`utilities/data_reader.py` validates required CSV columns, parses passenger counts and booleans, and raises actionable errors for missing, malformed or empty files. Values use `.example.test` email domains and fictional names.

## Locator inventory

See [`LOCATOR_INVENTORY.md`](LOCATOR_INVENTORY.md) for page, purpose, primary/fallback selector, expected state and relevant tests. The app intentionally exposes IDs and `data-testid` attributes. For repeated itinerary cards, the stable parent ID `data-itinerary-id` is combined with a child locator rather than selecting a button by index. The page objects use the same primary selectors.

## Synchronization and test architecture

`BasePage` wraps `WebDriverWait` and Selenium expected conditions for visibility, clickability, presence, disappearance and URL changes. Page objects contain locators and user actions; assertions stay in test modules. There are no fixed `time.sleep()` calls. React state changes are synchronous and tests wait for meaningful elements before reading them. Each pytest browser fixture is function-scoped and is quit in teardown.

## Artifacts and evidence

- Screenshots: `artifacts/screenshots/` (captured on a failed test call when a driver exists).
- Logs: `artifacts/logs/triptrail.log`.
- HTML report: `reports/pytest-report.html` when run with the documented `--html` option.
- The default root configuration intentionally does not force HTML report generation on every invocation; use the explicit command above.

To create a **real failure screenshot** for faculty evidence, temporarily introduce a controlled failing assertion in a browser test, e.g. change the expected itinerary count in `tests/test_search.py` from `3` to `999`, run that single test, and confirm a timestamped PNG appears in `artifacts/screenshots/`. Then revert the assertion and rerun the test. Do not submit the intentional failure as a passing result. Screenshots/reports are generated only by actually executing the tests; this repository does not contain fabricated execution evidence.

## Example debugging workflow

If a price-filter test returns a fare above the limit, inspect `data-testid="itinerary-fare"` and its numeric `data-fare` attribute in DevTools, confirm `price-filter` updates the React range state, then inspect the actual fare list collected by `SearchResultsPage.fares()`. Check the test log and failure screenshot before changing a selector or assertion.

## Troubleshooting

- **Connection refused:** start Vite in `app/` and verify the URL shown by Vite matches `base_url`.
- **Browser fails to start:** update Chrome/Edge, install the matching browser, upgrade Selenium, and allow Selenium Manager network access if needed.
- **No screenshot after a failure:** confirm the failure occurred during the test call phase and a WebDriver was created; screenshot failures are logged without masking the original failure.
- **No HTML report:** run with `--html=reports/pytest-report.html --self-contained-html`; pytest-html is installed by `requirements.txt`.
- **Unexpected empty results:** verify route spelling/case against the seeded data in `app/src/data/itineraries.ts`.
- **Past date test is inconsistent:** the website uses local calendar date and rejects earlier dates. Run with machine date/time configured correctly.

## Acceptance coverage

| Scenario | Test module |
|---|---|
| TC01 Search seeded route | `tests/test_search.py` |
| TC02 Maximum-price filter | `tests/test_price_filter.py` |
| TC03 Full departure sorting | `tests/test_sorting.py` |
| TC04 Select itinerary and preserve details | `tests/test_itinerary_selection.py` |
| TC05 Missing surname | `tests/test_passenger_validation.py` |
| TC06 Seat appears in review | `tests/test_seat_selection.py` |
| TC07 Terms acceptance | `tests/test_terms_acceptance.py` |
| TC08 Sold-out itinerary | `tests/test_sold_out.py` |

Additional tests cover same-route rejection, missing route, past date, empty filters, reset, ascending/descending price, invalid email, occupied seats, insufficient seats for multiple passengers, modal and iframe behavior, browser Back/Forward, direct workflow navigation and CSV-parametrized tests.

## Known limitations

- The application is a seeded client-side simulation and has no server, user account, live inventory, or persistence beyond the browser session.
- It intentionally ends at review; there is no booking, payment, or ticket issuance.
- Browser execution depends on the host OS, installed browser, and Selenium Manager support. This generated repository has not been represented as having passed real browser tests unless you run them locally.
- The iframe is a local `srcDoc` demonstration for switching-context practice, not a third-party site.

## Faculty evidence checklist

- [ ] Capture Node/Python versions and install commands.
- [ ] Start the website and record the Vite URL.
- [ ] Run `pytest --collect-only` and retain output.
- [ ] Run the mandatory eight scenarios and retain the real HTML report.
- [ ] Verify failed-test screenshot behavior using the controlled failure procedure, then revert.
- [ ] Inspect screenshots/logs and ensure no real personal data appears.
- [ ] Run at least one browser configuration in Chrome and Edge if both are available.
- [ ] Run the independent unittest example.
- [ ] Include a short demo of search → filter/sort → select → passengers → seats → terms → review.

**No real reservations or payments occur in V-Fly.**
