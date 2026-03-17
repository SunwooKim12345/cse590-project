#!/usr/bin/env python
"""Validate response log CSV against required columns."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = [
    "run_id",
    "timestamp_utc",
    "scenario_id",
    "question_set_item_id",
    "question_id",
    "model_name",
    "prompt_id",
    "input_prompt",
    "raw_response",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", help="Path to response log CSV")
    args = parser.parse_args()

    path = Path(args.csv_path)
    if not path.exists():
        print(f"ERROR: file not found: {path}")
        sys.exit(1)

    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        print("ERROR: missing required columns")
        for col in missing:
            print(f"- {col}")
        sys.exit(1)

    empty_prompt = (df["input_prompt"].fillna("").str.strip() == "").sum()
    empty_resp = (df["raw_response"].fillna("").str.strip() == "").sum()

    print(f"OK: {path}")
    print(f"rows: {len(df)}")
    print(f"empty input_prompt rows: {empty_prompt}")
    print(f"empty raw_response rows: {empty_resp}")


if __name__ == "__main__":
    main()
