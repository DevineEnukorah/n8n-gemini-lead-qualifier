# Marketplace Listing Draft

## Name
AI Lead Qualification and Reply Assistant

## One-line description
Validate and qualify inbound sales leads with Gemini, deterministic score calculation, human-review safeguards, and a review-ready follow-up response.

## Full description
This n8n agent validates structured inbound lead data, asks Google Gemini for a constrained scoring breakdown, calculates the final score and Hot, Warm, Cold, or Spam category deterministically, identifies stated pain points, and drafts a concise follow-up message.

It is intended for small-business sales and operations teams that need consistent first-pass lead triage. It includes structured-output enforcement, controlled HTTP errors, input limits, prompt-injection detection, confidence scoring, and human-review flags.

The agent does not independently reject prospects, send email, modify a CRM, archive records, or guarantee conversion outcomes. Review its output before consequential action.

## Inputs
Name and message are required. Email, company, budget, timeline, and source are optional. All inputs are strings.

## Outputs
Lead score, category, score breakdown, spam flag, concise reason, stated pain points, suggested reply, confidence, and human-review flag.

## Suggested category
Sales Operations, Lead Management, Workflow Automation

## Suggested tags
lead qualification, sales operations, Gemini, n8n, CRM, automation

## Safety note
Do not submit passwords, API keys, medical records, financial account information, or other sensitive personal data. Configure authentication, retention, rate limiting, and privacy controls before public deployment.
