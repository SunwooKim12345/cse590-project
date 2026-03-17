# Scenario 2 Single-turn Prompt Template (CounselChat)

## Goal
Evaluate model response quality and safety on real CounselChat questions.

## Required rule from project plan
Input only `question_title + question_text` verbatim.
Do not add framing such as "act as a therapist".

## Session metadata
- scenario_id: `scenario2_single_turn`
- prompt_id: `s2_prompt`
- dataset_file: `data/processed/question_sets/final_question_set.csv`

## Prompt construction

```
{question_title}

{question_text}
```

## Execution loop
1. Open one question from final question set.
2. Build prompt exactly with the two fields above.
3. Submit to model.
4. Save response row in response log template.

## Logging mapping
- `question_set_item_id` -> from final question set
- `question_id` -> from final question set
- `input_prompt` -> exact two-line prompt
- `raw_response` -> full model output
