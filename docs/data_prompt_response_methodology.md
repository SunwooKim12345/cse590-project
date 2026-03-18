# Data, Prompt, and Response Formatting Methodology

## 1) Purpose and Scope
This document explains how we:
- composed and selected questions for Scenario 1 (S1) and Scenario 2 (S2),
- collected model responses,
- standardized response formatting for downstream evaluation.

The workflow is aligned with the project plan requirements for the Member 2 role.

## 2) Question Composition and Rationale

### 2.1 Scenario 1 (S1): Multi-turn Escalation Prompts
Source file:
- `prompts/frozen/scenario1_persona_scripts.csv`

Composition method:
- Three personas (`P1`, `P2`, `P3`)
- Eight user turns per persona (`24` turns total)
- Structured progression by phase:
  - `rapport` (early conversation)
  - `dependency` (attachment/boundary pressure)
  - `escalation` (higher-risk language)

Why this composition:
- It tests whether chatbot behavior changes across turns, not only in a single reply.
- It supports evaluation of boundary maintenance, risk detection, and referral behavior under escalation.
- It keeps turn ordering consistent across models for fair comparison.

### 2.2 Scenario 2 (S2): CounselChat Single-turn Questions
Source files:
- Input dataset: `nbertagnolli/counsel-chat`
- Sampling script: `scripts/build_final_question_set.py`
- Output set: `data/processed/question_sets/final_question_set.csv`

Composition method:
- Target size: `24` unique questions (within the 20-25 requirement)
- Topic coverage across core categories:
  - depression, anxiety, relationships, grief-and-loss, self-esteem, trauma, substance-abuse
- View-priority strategy:
  - higher `views` (and `upvotes` tie support) are prioritized
- Severity mix:
  - include both mild/informational and higher-risk content
- Reference answer policy:
  - for each question, keep the highest-upvoted therapist answer

Why this composition:
- It reflects real user demand (view counts), not random sampling.
- It preserves topic diversity so results are not dominated by one category.
- It includes risk diversity so both routine and sensitive cases are evaluated.
- It keeps a stable human reference for comparison.

## 3) Prompt Execution Rules

### 3.1 S1 Rules
- Use each `user_message` verbatim and in order.
- Keep a single chat session per persona (P1, then new session P2, then new session P3).
- Do not rewrite or simplify user turns.

### 3.2 S2 Rules
- Prompt format is strictly:
  - `question_title`
  - blank line
  - `question_text`
- No role priming (for example, do not add "act as a therapist").
- One prompt per question item.

## 4) Response Collection Procedure

Setup script:
- `scripts/setup_response_collection.py`

Generated run artifacts:
- `logs/responses/raw/<run_id>/responses_s1_<model>_<operator>.csv`
- `logs/responses/raw/<run_id>/responses_s2_<model>_<operator>.csv`
- `logs/responses/raw/<run_id>/session_metadata.json`
- `logs/responses/raw/<run_id>/collection_tracker.csv`

Collection approach:
1. Initialize run files using the setup script.
2. For each model, record responses into prefilled CSV rows.
3. Save immediately after each response.
4. Store screenshots in the corresponding run folder.
5. Validate CSV structure using `scripts/validate_response_log.py`.

## 5) Response Format Standardization

Template and schema:
- CSV template: `templates/response_log_template.csv`
- JSON schema: `data/processed/schemas/response_log_schema.json`

Required fields (core):
- `run_id`, `timestamp_utc`, `scenario_id`, `question_set_item_id`, `question_id`
- `model_name`, `prompt_id`, `input_prompt`, `raw_response`

Additional analysis fields:
- `model_version`, `platform`, `response_language`
- `safety_disclaimer_present`
- `help_seeking_referral_present`
- `source_citation_present`
- `operator`, `notes`

Formatting rules:
- Keep `input_prompt` as the exact prompt used.
- Store full model output in `raw_response` without paraphrasing.
- Use UTC ISO-8601 timestamps (`YYYY-MM-DDTHH:MM:SSZ`).
- Use conservative boolean coding (mark `true` only when explicit textual evidence is present).

Boolean labeling guide:
- `docs/boolean_labeling_guide.md`

## 6) Quality Control and Reproducibility

Reproducibility controls:
- Frozen prompt package: `prompts/frozen/`
- Prompt integrity files:
  - `prompts/frozen/prompt_package_manifest.json`
  - `prompts/frozen/checksums.sha256`
- Question-set evidence:
  - `docs/final_question_set_evidence.md`

Validation command example:
```bash
python scripts/validate_response_log.py logs/responses/raw/run01/responses_s2_chatgpt_member2.csv
```

## 7) Summary
The final workflow ensures:
- consistent question composition across S1 and S2,
- strategy-aligned sampling for S2,
- standardized response logging for all models,
- reproducible and auditable data processing for later evaluation.
