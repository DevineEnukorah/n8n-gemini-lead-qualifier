# Gemini Lead Qualification Agent

Production-oriented n8n workflow for validating inbound lead data, assessing sales fit with Google Gemini, enforcing structured model output, calculating the final score deterministically, and returning a stable JSON API response.

## Version

`1.1.0`

## Implemented workflow

1. Receives a JSON POST request through an n8n Webhook.
2. Validates field types, required values, email format, field lengths, and total payload size.
3. Normalizes Unicode and removes control characters.
4. Detects common prompt-injection patterns and carries the security flag through the workflow.
5. Requests a structured scoring breakdown from Google Gemini.
6. Returns a controlled HTTP 502 response when model execution or parsing fails.
7. Calculates the total score and category in code instead of trusting the model's arithmetic.
8. Enforces confidence, category-boundary, spam, and prompt-injection review rules.
9. Returns HTTP 200, 400, or 502 JSON responses with no-store security headers.

The workflow does not automatically reject leads, send email, update a CRM, or archive submissions.

## Input contract

All supplied fields must be strings. `name` and `message` are required.

```json
{
  "name": "Ada Bello",
  "email": "ada@example.com",
  "company": "FinServe Ltd",
  "message": "We need to automate invoice reconciliation across three systems.",
  "budget": "$8,000-$12,000",
  "timeline": "4 weeks",
  "source": "website"
}
```

Limits: name 120, email 254, company 160, message 5000, budget 120, timeline 120, source 120 characters. Total JSON payload limit is 12,000 characters.

## Success response

```json
{
  "success": true,
  "result": {
    "lead_score": 82,
    "category": "Hot",
    "score_breakdown": {
      "service_fit": 35,
      "budget_authority": 20,
      "urgency": 15,
      "requirements_clarity": 12
    },
    "spam_detected": false,
    "summary_reason": "Strong automation fit with stated authority and timeline.",
    "pain_points": ["Manual invoice reconciliation", "Disconnected systems"],
    "suggested_reply": "Thank you for reaching out. Would you be available for a 15-minute discovery call?",
    "confidence": 90,
    "requires_human_review": false
  },
  "meta": {
    "request_id": "execution-id",
    "received_at": "2026-07-22T00:00:00.000Z",
    "workflow_version": "1.1.0",
    "model_provider": "Google Gemini",
    "automated_assessment": true
  }
}
```

## Installation and live testing

1. Import `workflow.json` into a current n8n installation.
2. Open **Google Gemini Chat Model** and attach your Gemini credential.
3. Confirm `models/gemini-3.1-flash-lite` appears in the model list. Select a currently supported Gemini model if your account does not expose it.
4. Do not activate the workflow yet.
5. Open **Lead Webhook**, select **Listen for test event**, and copy the test URL.
6. Follow `tests/LIVE_TEST_PLAN.md` and submit every fixture. The `tests/send_fixture.py` helper sends only the fixture input object.
7. Review all output, especially boundary cases and human-review flags.
8. Configure webhook authentication, network rate limiting, retention, monitoring, and privacy notices before publishing the production URL.
9. Activate only after all live tests pass.

## Local tests

```bash
python tests/run_all.py
```

The local suite validates the workflow graph, UUIDs, node configuration, schemas, expressions, response codes, headers, documentation, fixture structure, Code-node behavior, 10,000 deterministic fuzz iterations per standard run, and invalid-schema mutations.

## Important limitation

Local testing cannot execute the live Google Gemini API without a valid credential and an n8n runtime. The final model call must therefore be tested manually in n8n before activation. This repository includes a complete live test plan for that step.

## Security and privacy

Lead data is untrusted. Do not submit passwords, API keys, medical records, financial account data, or other sensitive personal data. Prompt-injection detection is heuristic, not comprehensive. Human review remains required for ambiguous, regulated, low-confidence, or consequential cases.

### AI provider failure responses

Successful qualifications return HTTP 200 with a JSON response.

Input validation failures return HTTP 400 with a JSON response.

Some Google Gemini credential, unsupported-model, connection, or AI sub-node failures may be handled directly by n8n before the workflow reaches its custom error branch. In those cases, the webhook may return HTTP 502 with a plain-text response such as:

```text
error code: 502

## Licence

MIT. See `LICENSE`.
