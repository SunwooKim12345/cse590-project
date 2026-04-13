# Run01 Priority Checklist (2026-04-13)

Scope:
- workspace: `c:\Users\USER\study\CSE590_group_project`
- run folder: `logs/responses/raw/run01`

Current snapshot (synced):
- total response files: `8`
- total expected rows: `192`
- collected raw responses: `96` (all S2 files complete)
- remaining raw responses to collect: `96` (all S1 files)
- `collection_tracker.csv` synced to current state

## Priority order

1. Complete Scenario 1 (S1) collection for all models
2. Fill timestamps and boolean labels for newly collected S1 rows
3. Fill missing timestamps/boolean labels in S2 non-chatgpt files
4. Run full validation + move QA-passed outputs to `logs/responses/normalized/`

## File-by-file task board

### P0 (already completed)
- [x] `responses_s2_chatgpt_member2.csv`: raw responses collected and validated
- [x] `responses_s2_claude_member2.csv`: raw responses collected and validated
- [x] `responses_s2_gemini_member2.csv`: raw responses collected and validated
- [x] `responses_s2_character_ai_member2.csv`: raw responses collected and validated

### P1 (now required): S1 raw response collection
- [ ] `responses_s1_chatgpt_member2.csv`
  - [ ] Collect 24 `raw_response` (P1-P3, 8 turns each)
  - [ ] Fill `timestamp_utc` + boolean labels
  - [ ] Confirm screenshots under `screenshots/s1_chatgpt/`
  - [ ] Validate CSV
- [ ] `responses_s1_claude_member2.csv`
  - [ ] Collect 24 `raw_response`
  - [ ] Fill `timestamp_utc` + boolean labels
  - [ ] Confirm screenshots under `screenshots/s1_claude/`
  - [ ] Validate CSV
- [ ] `responses_s1_gemini_member2.csv`
  - [ ] Collect 24 `raw_response`
  - [ ] Fill `timestamp_utc` + boolean labels
  - [ ] Confirm screenshots under `screenshots/s1_gemini/`
  - [ ] Validate CSV
- [ ] `responses_s1_character_ai_member2.csv`
  - [ ] Collect 24 `raw_response`
  - [ ] Fill `timestamp_utc` + boolean labels
  - [ ] Confirm screenshots under `screenshots/s1_character_ai/`
  - [ ] Validate CSV

### P2 (metadata/label cleanup before normalization)
- [ ] Fill missing `timestamp_utc` in S2 files except chatgpt
- [ ] Fill boolean labels in S2 files except chatgpt
- [ ] Re-run progress sync/report after labeling

## Validation commands

Validate one file:

```bash
python scripts/validate_response_log.py logs/responses/raw/run01/<responses_file>.csv
```

Sync tracker/report from current CSVs:

```bash
python scripts/sync_collection_progress.py --project-root CSE590_group_project --run-id run01 --sync-tracker --write-report docs/run01_progress_report.md
```

## Done criteria

- `raw_response` not empty for all 192 rows across 8 files
- `timestamp_utc` not empty for all 192 rows
- three boolean labels completed for all rows (conservative coding)
- screenshots stored per model/scenario folder
- validation passes for all files
- QA-passed files moved to `logs/responses/normalized/`
