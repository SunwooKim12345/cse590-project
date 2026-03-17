#!/usr/bin/env python
"""Create response-collection starter files for Scenario 1 and Scenario 2."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

DEFAULT_MODELS = ["chatgpt", "claude", "character_ai", "gemini"]
RESPONSE_COLUMNS = [
    "run_id",
    "timestamp_utc",
    "scenario_id",
    "question_set_item_id",
    "question_id",
    "model_name",
    "model_version",
    "platform",
    "prompt_id",
    "input_prompt",
    "raw_response",
    "response_language",
    "safety_disclaimer_present",
    "help_seeking_referral_present",
    "source_citation_present",
    "operator",
    "notes",
]


def build_s2_records(question_set_path: Path, run_id: str, operator: str) -> list[dict]:
    df = pd.read_csv(question_set_path)
    records: list[dict] = []
    for _, row in df.iterrows():
        prompt = f"{row['question_title']}\n\n{row['question_text']}"
        records.append(
            {
                "run_id": run_id,
                "timestamp_utc": "",
                "scenario_id": "scenario2_single_turn",
                "question_set_item_id": row["question_set_item_id"],
                "question_id": str(row["question_id"]),
                "model_name": "",
                "model_version": "",
                "platform": "",
                "prompt_id": "s2_prompt",
                "input_prompt": prompt,
                "raw_response": "",
                "response_language": "",
                "safety_disclaimer_present": "",
                "help_seeking_referral_present": "",
                "source_citation_present": "",
                "operator": operator,
                "notes": "",
            }
        )
    return records


def build_s1_records(persona_path: Path, run_id: str, operator: str) -> list[dict]:
    parsed_rows: list[dict] = []
    lines = persona_path.read_text(encoding="utf-8-sig").splitlines()
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.split(",", 3)
        if len(parts) < 4:
            continue
        parsed_rows.append(
            {
                "persona_id": parts[0].strip(),
                "turn_number": parts[1].strip(),
                "phase": parts[2].strip(),
                "user_message": parts[3].strip(),
            }
        )

    df = pd.DataFrame(parsed_rows)
    records: list[dict] = []
    for _, row in df.iterrows():
        item_id = f"{row['persona_id']}_T{int(row['turn_number']):02d}"
        records.append(
            {
                "run_id": run_id,
                "timestamp_utc": "",
                "scenario_id": "scenario1_multi_turn",
                "question_set_item_id": item_id,
                "question_id": item_id,
                "model_name": "",
                "model_version": "",
                "platform": "",
                "prompt_id": "s1_prompt",
                "input_prompt": row["user_message"],
                "raw_response": "",
                "response_language": "",
                "safety_disclaimer_present": "",
                "help_seeking_referral_present": "",
                "source_citation_present": "",
                "operator": operator,
                "notes": "",
            }
        )
    return records


def write_model_csv(records: list[dict], model: str, output_path: Path) -> None:
    df = pd.DataFrame(records)
    df["model_name"] = model
    df = df[RESPONSE_COLUMNS]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="run01", help="Session identifier.")
    parser.add_argument("--operator", default="member2", help="Operator name.")
    parser.add_argument(
        "--models",
        default=",".join(DEFAULT_MODELS),
        help="Comma-separated model keys.",
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root that contains prompts/, data/, and logs/.",
    )
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    run_id = args.run_id.strip()
    operator = args.operator.strip()
    models = [m.strip() for m in args.models.split(",") if m.strip()]
    if not models:
        raise ValueError("At least one model is required.")

    question_set_path = root / "data" / "processed" / "question_sets" / "final_question_set.csv"
    persona_path = root / "prompts" / "frozen" / "scenario1_persona_scripts.csv"
    if not persona_path.exists():
        persona_path = root / "prompts" / "scenario1_persona_scripts.csv"

    if not question_set_path.exists():
        raise FileNotFoundError(f"Missing question set: {question_set_path}")
    if not persona_path.exists():
        raise FileNotFoundError(f"Missing Scenario 1 script: {persona_path}")

    s1_records = build_s1_records(persona_path, run_id, operator)
    s2_records = build_s2_records(question_set_path, run_id, operator)

    run_dir = root / "logs" / "responses" / "raw" / run_id
    files_created: list[str] = []
    for model in models:
        s1_file = run_dir / f"responses_s1_{model}_{operator}.csv"
        s2_file = run_dir / f"responses_s2_{model}_{operator}.csv"
        write_model_csv(s1_records, model, s1_file)
        write_model_csv(s2_records, model, s2_file)
        files_created.extend([str(s1_file), str(s2_file)])

        (run_dir / "screenshots" / f"s1_{model}").mkdir(parents=True, exist_ok=True)
        (run_dir / "screenshots" / f"s2_{model}").mkdir(parents=True, exist_ok=True)

    metadata = {
        "run_id": run_id,
        "operator": operator,
        "models": models,
        "scenarios": ["scenario1_multi_turn", "scenario2_single_turn"],
        "question_set_file": "data/processed/question_sets/final_question_set.csv",
        "scenario1_script_file": str(persona_path.relative_to(root)).replace("\\", "/"),
        "prompt_package": "prompts/frozen",
        "status": "ready_for_collection",
        "files_created": [str(Path(f).relative_to(root)).replace("\\", "/") for f in files_created],
    }
    metadata_path = run_dir / "session_metadata.json"
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    tracker_rows = []
    for model in models:
        tracker_rows.append(
            {
                "scenario_id": "scenario1_multi_turn",
                "model_name": model,
                "total_items": len(s1_records),
                "completed_items": 0,
                "status": "not_started",
            }
        )
        tracker_rows.append(
            {
                "scenario_id": "scenario2_single_turn",
                "model_name": model,
                "total_items": len(s2_records),
                "completed_items": 0,
                "status": "not_started",
            }
        )
    tracker_df = pd.DataFrame(tracker_rows)
    tracker_path = run_dir / "collection_tracker.csv"
    tracker_df.to_csv(tracker_path, index=False, encoding="utf-8-sig")

    print(f"Prepared run: {run_id}")
    print(f"Run directory: {run_dir}")
    print(f"Scenario 1 rows/model: {len(s1_records)}")
    print(f"Scenario 2 rows/model: {len(s2_records)}")
    print("Created files:")
    for rel in metadata["files_created"]:
        print(f"- {rel}")
    print(f"- {str(metadata_path.relative_to(root)).replace(chr(92), '/')}")
    print(f"- {str(tracker_path.relative_to(root)).replace(chr(92), '/')}")


if __name__ == "__main__":
    main()
