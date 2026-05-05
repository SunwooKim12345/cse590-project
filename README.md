# CES590 Member 2 Workspace (Data and Prompt Lead)

This workspace is organized for the Member 2 scope in the HCAI project.

## Deliverables in this folder
- Final question set: `data/processed/question_sets/`
- Prompt templates: `prompts/`
- Standardized response logging format: `templates/` and `data/processed/schemas/`
- Clean dataset structure and tracking docs: `docs/` and `data/raw/counselchat/`
- All therapist responses used: `data/processed/Therapist Responses/`
- Scenario 2 Master (used for cosine similarity, choosing responses for human evaluation, and creating heat maps): `scripts/scenario_2_cosine_similarity.ipynb`

## Results
- Scenario 1: https://drive.google.com/drive/folders/1-UOAATXYWJ2M2KWf6zs1S-M7-SmAy8Xh
- Scenario 2
   - Cosine Similarity Heatmaps: `results/Scenario 2/Heat Maps`
   - Human Evaluation: https://docs.google.com/spreadsheets/d/1un85KF4ait6tthdyZicoiu2p3jT3xTydkxC_FJ_O6B4/edit

## Quick start
1. Build the final question set from CounselChat:
   ```bash
   python scripts/build_final_question_set.py
   ```
2. Generate prompt templates:
   ```bash
   python scripts/generate_prompt_templates.py
   ```
3. Use prompt templates:
   - `prompts/scenario1_multiturn_template.md`
   - `prompts/scenario2_singleturn_template.md`
   - for S2 locked runs, use `prompts/frozen/` copies and `docs/prompt_package_freeze.md`
   - for S1 adaptive runs, keep the actual sent turn text in `input_prompt`
4. Create response collection starter files:
   ```bash
   python scripts/setup_response_collection.py --run-id run01 --operator member2
   ```
5. Record model outputs using:
   - `templates/response_log_template.csv`
   - naming rules in `docs/folder_and_naming_convention.md`
6. Sync progress for required models (ChatGPT/Claude/Character.AI/Gemini):
   ```bash
   python scripts/sync_collection_progress.py --run-id run01 --sync-tracker --write-report docs/run01_progress_report.md
   ```

## Scenario alignment to project plan
- Scenario 1: multi-turn escalation conversations (8-12 user turns)
- Scenario 2: single-turn CounselChat Q&A (questionTitle + questionText verbatim)

## Notes
- The question sampler follows the project PDF strategy: strategic (non-random) sampling, high-view priority, severity mix, and highest-upvoted reference answer per question.
- Dataset source: `nbertagnolli/counsel-chat` (Hugging Face)
