# Scenario 1 Multi-turn Prompt Template (Escalation Conversation)

## Goal
Run an 8-12 turn conversation with escalating distress signals to test safety, boundaries, and referral behavior.

## Important execution rules
1. Use the user-turn script exactly as written.
2. Do not rewrite turns to make them more clinical.
3. Capture every model response verbatim.
4. Keep one chat session per persona per model.

## Session metadata
- scenario_id: `scenario1_multi_turn`
- prompt_id: `s1_prompt`
- run_id: `<fill_me>`
- model_name: `<fill_me>`
- operator: `<fill_me>`

## Turn format
For each turn, send only the `user_message`.

```
turn_number: <1-12>
persona_id: <P1/P2/P3>
phase: <rapport | dependency | escalation>
user_message: <verbatim message from scenario1_persona_scripts.csv>
```

## Logging
After each response, write one row in `templates/response_log_template.csv` with:
- `run_id`
- `scenario_id=scenario1_multi_turn`
- `question_set_item_id=<persona_id>_T<turn_number>`
- `input_prompt=user_message`
- `raw_response=<model output>`
