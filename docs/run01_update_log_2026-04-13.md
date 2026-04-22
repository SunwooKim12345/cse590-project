# Run01 Update Log (2026-04-13)

## Current Status Summary

- S1 and S2 raw response collection is complete for all four models:
  - `chatgpt`
  - `claude`
  - `character_ai`
  - `gemini`
- Total collected raw responses: `192/192`.
- `response_language` is filled for all rows.
- `timestamp_utc` is intentionally blank.
- S1 is adaptive multi-turn collection; actual sent turns are preserved in `input_prompt` and S1 files are not checksum-locked.
- S2 remains the fixed/checksum-locked prompt condition.
- Boolean evaluation fields are intentionally blank for evaluator coding:
  - `safety_disclaimer_present`
  - `help_seeking_referral_present`
  - `source_citation_present`
- Normalized combined output exists at `logs/responses/normalized/responses_normalized.csv`.

## Current Validation Status

- All 8 raw response CSV files pass `scripts/validate_response_log.py`.
- The normalized response CSV passes `scripts/validate_response_log.py`.
- `docs/run01_progress_report.md` is synced to current raw response completion status.
- `prompts/frozen/checksums.sha256` verifies only S2 fixed prompt artifacts.

## Next Required Actions

1. Decide whether screenshot folders should be included in the submitted/git-tracked package.
2. Have evaluators manually fill the three boolean evaluation fields.
3. If evaluator labels are added to raw files, rebuild `logs/responses/normalized/responses_normalized.csv`.
4. Final review of `git diff` before commit/submission.
