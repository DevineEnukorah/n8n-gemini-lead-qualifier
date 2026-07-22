# Changelog

## 1.1.0 - 2026-07-22

- Added deterministic score calculation from four bounded component scores.
- Separated spam detection from sales qualification thresholds.
- Added controlled HTTP 502 handling for model and parser failures.
- Added valid UUIDs for workflow, webhook, and node identifiers.
- Strengthened type, size, Unicode, email, and prompt-injection validation.
- Added deterministic human-review enforcement and 150-word reply enforcement.
- Expanded representative fixtures from 5 to 16.
- Added schema mutation tests and 10,000 Code-node fuzz iterations.
- Updated CI to run Python and Node tests.

## 1.0.0 - 2026-07-22

- Replaced the hardcoded sample lead with dynamic webhook input.
- Added validation, structured output, API responses, tests, documentation, and licensing.
