# Dataset Log

## Current source
- dataset_name: `nbertagnolli/counsel-chat`
- provider: Hugging Face Datasets
- pull_status: `latest`
- rows_loaded: `2775`
- unique_questions: `940`

## Processing policy
1. Keep one reference therapist answer per question.
2. Reference answer = highest upvoted answer for that `question_id`.
3. Sampling for final set:
   - 20-25 unique questions
   - topic coverage from project plan (`depression`, `anxiety`, `relationships`, `grief-and-loss`, `self-esteem`, `trauma`, `substance-abuse`)
   - prioritize higher views
   - include mild/informational + higher-risk mix
   - strategic sampling (not random)

## Change notes
- Initial generation pipeline and final question set produced.
- Sampling logic updated to explicitly match PDF strategy and prompt generation automated via script.
