# Response Logging Protocol

## Purpose
Standardize response collection across models and scenarios so downstream scoring is consistent.

## Required columns
- `run_id`
- `timestamp_utc`
- `scenario_id`
- `question_set_item_id`
- `question_id`
- `model_name`
- `model_version`
- `platform`
- `prompt_id`
- `input_prompt`
- `raw_response`
- `response_language`
- `safety_disclaimer_present`
- `help_seeking_referral_present`
- `source_citation_present`
- `operator`
- `notes`

## Logging rules
1. Scenario 2 input must use `question_title + question_text` verbatim from final set.
2. Do not add role-priming text such as "act as therapist" in Scenario 2.
3. Save immediately after each model response to prevent data loss.
4. Store screenshots in a sibling folder with same `run_id`.
5. Use UTC timestamps in ISO-8601 (`YYYY-MM-DDTHH:MM:SSZ`).

## File locations
- Raw logs: `logs/responses/raw/`
- Normalized logs: `logs/responses/normalized/`
- Template: `templates/response_log_template.csv`
- Schema: `data/processed/schemas/response_log_schema.json`
