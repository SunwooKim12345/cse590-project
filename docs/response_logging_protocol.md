# Response Logging Protocol

## Purpose
Standardize response collection across models and scenarios so downstream scoring is consistent.

## Required columns
- `run_id`
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

## Evaluation columns
These may be left blank during response collection and filled later by evaluators:
- `safety_disclaimer_present`
- `help_seeking_referral_present`
- `source_citation_present`

## Scenario 1 logging
Scenario 1 is the multi-turn escalation condition.

Source prompt files:
- `prompts/frozen/scenario1_multiturn_template.md`
- `prompts/frozen/scenario1_persona_scripts.csv`

Execution rules:
1. Use `scenario1_persona_scripts.csv` as the baseline progression for persona, turn, and risk phase.
2. The next user prompt may be adapted slightly when needed to respond coherently to the model's prior answer.
3. Keep one continuous chat session per persona per model.
4. Start a new chat session when moving to the next persona.
5. Do not add clinical framing or role instructions beyond the user-facing turn text.
6. Capture each model response verbatim in `raw_response`.
7. Record the actual sent user text in `input_prompt`, even when it differs slightly from the baseline script.

Row mapping:
- `scenario_id`: `scenario1_multi_turn`
- `prompt_id`: `s1_prompt`
- `question_set_item_id`: `<persona_id>_T<turn_number>` such as `P1_T01`
- `question_id`: same value as `question_set_item_id`
- `input_prompt`: the actual user prompt sent for that turn

Scenario 1 has 3 personas (`P1`, `P2`, `P3`) and 8 turns per persona, for 24 rows per model.

Screenshots should be stored under:
- `logs/responses/raw/<run_id>/screenshots/s1_<model>/`

## Scenario 2 logging
Scenario 2 is the single-turn CounselChat question-answer condition.

Execution rules:
1. Use `question_title + blank line + question_text` verbatim from the final question set.
2. Do not add role-priming text such as "act as therapist".
3. Use one prompt per question item.
4. Capture the model response verbatim in `raw_response`.

Row mapping:
- `scenario_id`: `scenario2_single_turn`
- `prompt_id`: `s2_prompt`
- `question_set_item_id`: the final question-set item id, such as `S2Q01`
- `question_id`: the source CounselChat question id
- `input_prompt`: exact title/body prompt used

## Logging rules
1. Save immediately after each model response to prevent data loss.
2. Store screenshots in a sibling folder with same `run_id`.
3. Keep `response_language` filled when the language is clear.
4. Leave evaluator-owned boolean columns blank unless the evaluation team has already coded them.

## File locations
- Raw logs: `logs/responses/raw/`
- Normalized logs: `logs/responses/normalized/`
- Template: `templates/response_log_template.csv`
- Schema: `data/processed/schemas/response_log_schema.json`
