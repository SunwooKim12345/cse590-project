# Response Collection Setup

## Purpose
Prepare model-specific raw response logs so collection can start immediately.

## Setup command
```bash
cd c:\Users\USER\study\CSE590_group_project
python scripts/setup_response_collection.py --run-id run01 --operator member2
```

## What it generates
Under `logs/responses/raw/run01/`:
- `responses_s1_chatgpt_member2.csv`
- `responses_s1_claude_member2.csv`
- `responses_s1_character_ai_member2.csv`
- `responses_s1_gemini_member2.csv`
- `responses_s2_chatgpt_member2.csv`
- `responses_s2_claude_member2.csv`
- `responses_s2_character_ai_member2.csv`
- `responses_s2_gemini_member2.csv`
- `session_metadata.json`
- `collection_tracker.csv`
- `screenshots/` folders for each model/scenario

## Prefill behavior
- Scenario 1 logs are prefilled from `prompts/frozen/scenario1_persona_scripts.csv`.
- Scenario 2 logs are prefilled from `data/processed/question_sets/final_question_set.csv`.
- `input_prompt` is prefilled; you only add timestamp/response fields during collection.

## Validation
```bash
cd c:\Users\USER\study\CSE590_group_project
Get-ChildItem -File logs\responses\raw\run01 -Filter "responses_*.csv" | ForEach-Object { python scripts/validate_response_log.py $_.FullName }
```

## Progress sync automation (required models from scope plan)
The scope plan model set is fixed to:
- `chatgpt`
- `claude`
- `character_ai`
- `gemini`

Use this helper to audit progress and sync tracker:

```bash
cd c:\Users\USER\study\CSE590_group_project
python scripts/sync_collection_progress.py --run-id run01 --sync-tracker --write-report docs/run01_progress_report.md
```

Optional flags:
- `--fill-timestamps`: fills `timestamp_utc` where `raw_response` already exists
- `--autolabel`: fills empty boolean labels with heuristic defaults (manual review recommended)
