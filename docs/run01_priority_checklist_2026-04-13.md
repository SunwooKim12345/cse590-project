# Run01 Priority Checklist (2026-04-13)

Scope:
- workspace: `c:\Users\USER\study\CSE590_group_project`
- run folder: `logs/responses/raw/run01`

Current snapshot:
- total response files: `8`
- total expected rows: `192`
- collected raw responses: `192`
- response language filled rows: `192`
- S1 prompt mode: adaptive baseline; actual sent turns are preserved in `input_prompt`
- S2 prompt mode: fixed/checksum-locked
- evaluator-owned boolean labels are intentionally blank
- normalized output exists at `logs/responses/normalized/responses_normalized.csv`

## Completed

- [x] S1 raw response collection for `chatgpt`, `claude`, `character_ai`, `gemini`
- [x] S2 raw response collection for `chatgpt`, `claude`, `character_ai`, `gemini`
- [x] `response_language` filled for all rows
- [x] `timestamp_utc` left blank by project decision
- [x] Boolean evaluation fields left blank for evaluator coding:
  - `safety_disclaimer_present`
  - `help_seeking_referral_present`
  - `source_citation_present`
- [x] Raw CSV validation passes for all 8 response files
- [x] Normalized combined CSV created and validated
- [x] Progress report synced

## Remaining

- [ ] Decide whether to include screenshot folders in the submitted/git-tracked artifact.
- [ ] Evaluators manually code the three boolean evaluation fields.
- [ ] After evaluator coding, regenerate or update normalized outputs if labels are filled in raw files.
- [ ] Final `git diff` review before commit/submission.

## Validation commands

Validate one file:

```bash
python scripts/validate_response_log.py logs/responses/raw/run01/<responses_file>.csv
```

Validate normalized output:

```bash
python scripts/validate_response_log.py logs/responses/normalized/responses_normalized.csv
```

Sync tracker/report from current CSVs:

```bash
python scripts/sync_collection_progress.py --run-id run01 --sync-tracker --write-report docs/run01_progress_report.md
```

## Done criteria for current collection package

- `raw_response` not empty for all 192 rows across 8 files
- `input_prompt` not empty for all 192 rows
- `response_language` filled for all 192 rows
- evaluator-owned boolean fields intentionally blank
- validation passes for all raw response files
- `logs/responses/normalized/responses_normalized.csv` has 192 rows and validates
