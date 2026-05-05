# CSE590 HCAI Project: Mental Health Chatbot Response Evaluation

This repository contains the data, prompts, response logs, analysis artifacts, and documentation for evaluating mental-health-related chatbot responses across two scenarios.

The project compares responses from ChatGPT, Claude, Character.AI, and Gemini using standardized prompt sets, raw response logs, human evaluation inputs, and similarity-based analysis against therapist reference responses.

## Project Overview

### Scenario 1: Multi-turn escalation conversations
- Tests how models respond as user distress escalates across a conversation.
- Uses three persona scripts (`P1`, `P2`, `P3`) with eight turns each.
- Evaluates safety behavior, boundary maintenance, referral behavior, and handling of dependency/escalation language.

### Scenario 2: Single-turn CounselChat questions
- Tests model responses to real mental-health questions from the CounselChat dataset.
- Uses 24 strategically sampled questions across depression, anxiety, relationships, grief/loss, self-esteem, trauma, and substance abuse.
- Keeps the highest-upvoted therapist answer as the reference response for downstream comparison.

## Repository Structure

```text
data/
  raw/                         Raw dataset notes and source documentation
  processed/
    question_sets/             Final Scenario 2 question set in CSV/JSONL
    schemas/                   Response-log schema
    Therapist Responses/       Therapist reference responses used in analysis
docs/                          Methodology, logging, and quality-control documents
logs/
  responses/
    raw/                       Model response collection logs by run
    normalized/                Normalized response data
prompts/
  frozen/                      Frozen prompt package with checksums
  *.md, *.csv                  Scenario prompt templates and persona scripts
results/                       Final charts and heat maps
scripts/                       Data preparation, validation, tracking, and analysis scripts
templates/                     Response-log and metadata templates
```

## Environment Setup

Use Python 3.10 or newer.

```bash
python -m pip install --upgrade pip
python -m pip install pandas datasets jupyter scikit-learn matplotlib seaborn
```

`pandas` and `datasets` are required for the core scripts. The notebook-based similarity and visualization workflow may also use the notebook/scikit-learn/plotting packages.

## How to Run the Project

Run the following commands from the repository root.

### 1. Build the Scenario 2 question set

```bash
python scripts/build_final_question_set.py
```

Outputs:
- `data/processed/question_sets/final_question_set.csv`
- `data/processed/question_sets/final_question_set.jsonl`

The sampling method prioritizes topic coverage, higher-view questions, severity mix, and highest-upvoted therapist reference answers. See `docs/final_question_set_evidence.md` and `docs/data_prompt_response_methodology.md`.

### 2. Generate prompt templates

```bash
python scripts/generate_prompt_templates.py
```

Outputs:
- `prompts/scenario1_multiturn_template.md`
- `prompts/scenario1_persona_scripts.csv`
- `prompts/scenario2_singleturn_template.md`
- `prompts/prompt_log.md`

For locked Scenario 2 runs, use the files in `prompts/frozen/` and verify them with `prompts/frozen/checksums.sha256`.

### 3. Initialize response collection files

Use a run ID and an operator ID. Example:

```bash
python scripts/setup_response_collection.py --run-id run01 --operator operator01
```

This creates prefilled CSV logs under:

```text
logs/responses/raw/run01/
```

The generated files follow this pattern:

```text
responses_s1_<model>_<operator>.csv
responses_s2_<model>_<operator>.csv
```

Required models:
- `chatgpt`
- `claude`
- `character_ai`
- `gemini`

### 4. Collect and log model responses

For each model:
- Scenario 1: run one multi-turn session per persona and record each turn.
- Scenario 2: submit each CounselChat question as `question_title` + blank line + `question_text`.
- Record the exact prompt in `input_prompt`.
- Record the full model output in `raw_response`.
- Save screenshots in the matching `logs/responses/raw/<run_id>/screenshots/` folder when available.

Response formatting rules are documented in:
- `docs/response_logging_protocol.md`
- `docs/boolean_labeling_guide.md`
- `templates/response_log_template.csv`

### 5. Validate response logs

Validate one file:

```bash
python scripts/validate_response_log.py logs/responses/raw/run01/responses_s2_chatgpt_operator01.csv
```

Validate all response CSVs for a run in PowerShell:

```powershell
Get-ChildItem -File logs\responses\raw\run01 -Filter "responses_*.csv" |
  ForEach-Object { python scripts/validate_response_log.py $_.FullName }
```

### 6. Run Scenario 2 similarity analysis

Open and run:

```text
scripts/scenario_2_cosine_similarity.ipynb
```

Expected inputs include:
- `data/processed/all_responses.csv`
- `data/processed/Therapist Responses/`

Main outputs:
- `results/Scenario 2/`
- `results/Scenario 2/Heat Maps/`

## Current Artifacts

### Data and logs
- Final question set: `data/processed/question_sets/`
- Raw run logs: `logs/responses/raw/run01/`
- Normalized responses: `logs/responses/normalized/responses_normalized.csv`
- Combined processed responses: `data/processed/all_responses.csv`

### Results
- Scenario 1 charts: `results/Scenario 1/`
- Scenario 2 charts: `results/Scenario 2/`
- Scenario 2 heat maps: `results/Scenario 2/Heat Maps/`

External evaluation materials:
- Scenario 1 survey results: https://drive.google.com/drive/folders/1-UOAATXYWJ2M2KWf6zs1S-M7-SmAy8Xh
- Scenario 2 human evaluation sheet: https://docs.google.com/spreadsheets/d/1un85KF4ait6tthdyZicoiu2p3jT3xTydkxC_FJ_O6B4/edit

## Notes

- Dataset source: `nbertagnolli/counsel-chat` from Hugging Face.
- Scenario 2 is fixed through the frozen prompt package and checksum files in `prompts/frozen/`.
- Scenario 1 is adaptive by design; preserve the exact sent text in `input_prompt`.
- Raw model responses should not be paraphrased or cleaned before logging.
- Boolean labels should be coded conservatively: use `true` only when explicit evidence appears in the response.

## Key Documentation

- `docs/data_prompt_response_methodology.md`: end-to-end data, prompt, and response methodology
- `docs/folder_and_naming_convention.md`: folder and file naming rules
- `docs/response_collection_setup.md`: response collection initialization details
- `docs/response_logging_protocol.md`: response logging protocol
- `docs/final_question_set_evidence.md`: Scenario 2 sampling evidence
- `docs/prompt_package_freeze.md`: frozen prompt package details
