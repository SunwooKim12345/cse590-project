# Final Question Set Confirmation Evidence

## Scope
This document confirms that `data/processed/question_sets/final_question_set.csv` satisfies the Scenario 2 sampling strategy in the project PDF (Section 3.2.1).

## Source Artifacts
- Question set file: `data/processed/question_sets/final_question_set.csv`
- Generator script: `scripts/build_final_question_set.py`
- Dataset source: `nbertagnolli/counsel-chat` (Hugging Face)
- Dataset policy in output fields:
  - `dataset_source = nbertagnolli/counsel-chat`
  - `dataset_snapshot = latest`
  - `sampling_strategy_id = pdf_s2`

## PDF Strategy Mapping (Section 3.2.1)
1. Select 20-25 unique questions across key topic categories.
2. Prioritize higher-view questions.
3. Include mixed severity (mild/informational + higher risk).
4. Use highest-upvoted therapist answer as reference answer for each selected question.
5. Strategic sampling (not random).

## Verification Results

| Criterion | Result | Evidence |
|---|---|---|
| Question count is 20-25 | PASS | `24` questions |
| Unique question IDs | PASS | `24/24` unique question IDs |
| Topic coverage across required categories | PASS | anxiety `4`, depression `4`, relationships `4`, grief-and-loss `3`, self-esteem `3`, trauma `3`, substance-abuse `3` |
| Higher-view priority applied | PASS | views range `300-6650`, median views `1022`; top-view examples included |
| Severity mix included | PASS | mild `15`, moderate `5`, high_risk `4`; higher-risk total `9` |
| Mild/informational included | PASS | informational mild count `13` |
| Reference answer = highest upvotes for each question | PASS | `24/24` matched max upvotes per question ID |
| Strategic (non-random) sampling | PASS | Rule-based selection by topic coverage + views priority + risk/informational constraints in `build_final_question_set.py` |

## Top View Examples in Final Set
- `S2Q01` (question_id `144`, anxiety): views `6650`
- `S2Q05` (question_id `14`, depression): views `5423`
- `S2Q02` (question_id `160`, anxiety): views `4205`
- `S2Q12` (question_id `715`, relationships): views `4005`
- `S2Q13` (question_id `716`, relationships): views `3414`

## Reproducibility Commands
```bash
cd c:\Users\USER\study\CSE590_group_project
python scripts/build_final_question_set.py --output-dir data/processed/question_sets --target-size 24
```

Validation commands used for this evidence:
```bash
@'
import pandas as pd
from datasets import load_dataset

df = pd.read_csv('data/processed/question_sets/final_question_set.csv')
print(len(df), df['question_id'].nunique())
print(df['topic'].value_counts())
print(df['severity'].value_counts())

raw = load_dataset('nbertagnolli/counsel-chat', split='train').to_pandas()
raw['questionID'] = raw['questionID'].astype(str)
raw['upvotes_num'] = pd.to_numeric(raw['upvotes'], errors='coerce').fillna(0).astype(int)
max_up = raw.groupby('questionID')['upvotes_num'].max().reset_index()
check = df.assign(question_id=df['question_id'].astype(str)).merge(
    max_up, left_on='question_id', right_on='questionID', how='left'
)
print((check['reference_answer_upvotes'] == check['upvotes_num']).all())
'@ | python -
```

## Decision
Final question set is confirmed for Scenario 2 execution under Member 2 responsibilities.
