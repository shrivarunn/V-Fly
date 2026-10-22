# TripTrail locator inventory

All primary locators are implemented in the website as IDs and/or `data-testid` attributes and mirrored in the Python page objects.

| Page | Purpose | Primary locator | Fallback locator | Expected state | Tests |
|---|---|---|---|---|---|
| Home | Origin | `#origin-input` | `[data-testid='origin-input']` | Select contains seeded cities | TC01, negative search |
| Home | Destination | `#destination-input` | `[data-testid='destination-input']` | Select contains seeded cities | TC01, same-route |
| Home | Departure date | `#departure-date-input` | `[data-testid='departure-date-input']` | Today or future | TC01, invalid date |
| Home | Passenger count | `#passenger-count-select` | `[data-testid='passenger-count-select']` | 1–6 | TC01, data-driven |
| Home | Swap route | `#swap-route-button` | `[data-testid='swap-route-button']` | Enabled button | Manual/extension |
| Home | Search | `#search-submit-button` | `[data-testid='search-submit-button']` | Enabled | TC01 |
| Results | Results list | `#results-list` | `[data-testid='results-list']` | Visible after search | TC01–TC03 |
| Results | Itinerary card | `[data-testid='itinerary-card']` | `[data-itinerary-id='HYD-BLR-101']` | Unique `data-itinerary-id` | TC01, TC08 |
| Results | Departure time | `[data-testid='itinerary-departure-time']` | `.journey > div:first-child strong` | `HH:MM` | TC03 |
| Results | Fare | `[data-testid='itinerary-fare']` | `[data-fare]` | Numeric `data-fare` | TC02, price sort |
| Results | Availability | `[data-testid='itinerary-availability']` | `.availability` | Seats left / Sold out | TC08 |
| Results | Price filter | `#price-filter` | `[data-testid='price-filter']` | Numeric range | TC02 |
| Results | Sort | `#departure-sort` | `[data-testid='departure-sort']` | Four sorting options | TC03 |
| Results | Select itinerary | `[data-testid='select-itinerary-button']` | Scoped button inside itinerary ID | Disabled if sold out | TC04, TC08 |
| Passenger | First name | `#passenger-first-name` | `[data-testid='passenger-first-name']` | Required | TC05, data-driven |
| Passenger | Surname | `#passenger-surname` | `[data-testid='passenger-surname']` | Required | TC05 |
| Passenger | Email | `#passenger-email` | `[data-testid='passenger-email']` | Valid email | data-driven |
| Passenger | Phone | `#passenger-phone` | `[data-testid='passenger-phone']` | Ten digits | data-driven |
| Passenger | Submit | `#passenger-form-submit` | `[data-testid='passenger-form-submit']` | Enabled | TC05 |
| Passenger | Surname error | `#surname-error` | `[data-testid='surname-error']` | Visible on invalid submit | TC05 |
| Seats | Seat map | `#seat-map` | `[data-testid='seat-map']` | Visible | TC06 |
| Seats | Selected list | `#selected-seat-list` | `[data-testid='selected-seat-list']` | Shows selected IDs | TC06 |
| Seats | Continue | `#seat-continue-button` | `[data-testid='seat-continue-button']` | Enabled only at exact count | TC06 |
| Terms | Dialog | `#terms-dialog` | `[data-testid='terms-dialog']` | Visible when opened | Modal test |
| Terms | Accept checkbox | `#terms-accept-checkbox` | `[data-testid='terms-accept-checkbox']` | Selected by user | TC07 |
| Terms | Continue | `#terms-continue-button` | `[data-testid='terms-continue-button']` | Disabled until accepted | TC07 |
| Review | Summary | `#reservation-summary` | `[data-testid='reservation-summary']` | Visible | TC06–TC07 |
| Review | Route | `#summary-route` | `[data-testid='summary-route']` | Selected route | TC04, TC06 |
| Review | Passengers | `#summary-passengers` | `[data-testid='summary-passengers']` | Synthetic passenger names | TC06 |
| Review | Seats | `#summary-seats` | `[data-testid='summary-seats']` | Selected seat IDs | TC06 |
| Review | Total | `#summary-total` | `[data-testid='summary-total']` | Numeric INR total | Review |

## Non-trivial locator note
The selection button is located relative to a card identified by its unique `data-itinerary-id`, e.g. `[data-itinerary-id='HYD-BLR-101'] [data-testid='select-itinerary-button']`. This avoids selecting the wrong repeated button based on DOM position, and keeps sold-out-state assertions scoped to the correct itinerary.
