# Test Report

## Result

**Local test status: PASSED**

Version tested: `1.1.0`

Test environment:

- Python: 3.13
- Node.js: 22.16.0
- Workflow nodes: 11
- Representative fixtures: 16

## Executed checks

1. Package and workflow graph validation passed.
2. All node IDs, the webhook ID, and the workflow version ID were validated as UUIDs.
3. Every main-flow node was confirmed reachable from the webhook.
4. Both branches of each IF node were confirmed connected.
5. Node versions and critical parameters were checked.
6. Embedded prompt and parser schema consistency were checked.
7. Response codes 200, 400, and 502 were checked.
8. `Cache-Control: no-store` and `X-Content-Type-Options: nosniff` were checked.
9. Exported workflow content was scanned for credential references and common secret patterns.
10. Eleven deliberately invalid schema mutations were rejected.
11. Five thousand generated runtime responses were validated against the final JSON Schema.
12. Seven n8n expressions were compiled and evaluated with representative mock data.
13. All 16 fixtures were executed through the real validation Code-node source.
14. The validation and response-building Code nodes passed 170,000 randomized iterations on the final code across multiple seeds.
15. All 358,176 possible combinations of the four bounded score components were checked.
16. Category and score consistency was checked for Cold, Warm, Hot, and Spam.
17. Spam score breakdown normalization was checked.
18. Prompt-injection review and confidence capping were checked.
19. Unicode normalization, field limits, type validation, email validation, payload limits, and control-character removal were checked.
20. Reply word limits, duplicate pain-point removal, fallback behavior, and markup stripping were checked.
21. Python files passed bytecode compilation.
22. JavaScript test files passed `node --check`.
23. The final ZIP archive was extracted into a clean directory and the complete local test suite was executed again.

## High-impact defects corrected during the audit

- The original category and total score were model-controlled. Version 1.1.0 now calculates both deterministically from bounded component scores.
- The earlier workflow had no controlled response for Gemini or parser failures. Version 1.1.0 returns a generic HTTP 502 response.
- Node and workflow identifiers were changed to valid UUIDs.
- IF-node condition metadata was aligned with the current n8n version-2 condition format.
- Spam scoring was normalized so the displayed total equals the sum of the displayed score breakdown.
- Prompt-injection cases now force human review and cap confidence at 60.
- Model-generated HTML or script markup is removed from returned text.
- The prompt, parser schema, runtime schema, fixtures, CI workflow, and documentation now describe the same contract.

## Limitation

The live Google Gemini request was not executed because this environment does not have your Gemini credential or a running n8n instance. Local tests cover the workflow structure, expressions, Code nodes, schemas, routing contract, failure contract, and deterministic post-processing. You must complete the live n8n test plan before activating the production webhook.
