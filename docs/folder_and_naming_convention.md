# Folder and Naming Convention

## Root structure
- `data/raw/counselchat/`: raw dataset notes and provenance
- `data/processed/question_sets/`: final sampled question sets
- `data/processed/schemas/`: response schema definitions
- `prompts/`: scenario templates and prompt IDs
- `logs/responses/raw/`: raw captured responses
- `logs/responses/normalized/`: cleaned and analysis-ready logs
- `templates/`: CSV/JSON templates for logging
- `scripts/`: reproducible data preparation scripts

## File naming rules
Use lowercase and underscores.

### Question set
`final_question_set.csv`
Example: `final_question_set.csv`

### Raw response logs
`responses_<scenario>_<model>_<operator>.csv`
Example: `responses_s2_chatgpt_jane.csv`

### Normalized response logs
`responses_normalized.csv`
Example: `responses_normalized.csv`

### Prompt files
`<scenario>_template.md`
Example: `scenario2_template.md`

## IDs
- `run_id`: unique per execution session (example: `s2_run01`)
- `prompt_id`: prompt tag (example: `s2_prompt`)
- `dataset_id`: dataset tag (example: `counselchat_hf`)
