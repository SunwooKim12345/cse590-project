#!/usr/bin/env python
"""Build a Scenario 2 final question set from the CounselChat dataset.

Sampling strategy follows the project PDF:
- Select 20-25 unique questions.
- Cover key topic categories (depression, anxiety, relationships,
  grief-and-loss, self-esteem, trauma, substance-abuse).
- Prioritize higher-view questions.
- Include a mix of mild/informational and higher-risk questions.
- Use the highest-upvoted therapist answer as the reference answer.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re

import pandas as pd
from datasets import load_dataset

DATASET_NAME = "nbertagnolli/counsel-chat"
CORE_TOPICS = [
    "depression",
    "anxiety",
    "relationships",
    "grief-and-loss",
    "self-esteem",
    "trauma",
    "substance-abuse",
]
MAX_PER_TOPIC = 4
DEFAULT_TARGET_SIZE = 24

HIGH_RISK_PATTERN = re.compile(
    r"\b(?:suicid|kill myself|end my life|don't want to live|self[- ]?harm|cutting|overdose|abuse|assault|panic attack|hopeless|worthless|can't go on)\b",
    flags=re.IGNORECASE,
)
MODERATE_PATTERN = re.compile(
    r"\b(?:depress|anxiet|trauma|ptsd|grief|addict|alcohol|drug|abandon|anger|lonely|crying|insomnia|sleep)\b",
    flags=re.IGNORECASE,
)
INFORMATIONAL_TITLE_PATTERN = re.compile(
    r"^(?:is|are|am|can|could|do|does|did|what|why|how|should|would|will)\b",
    flags=re.IGNORECASE,
)


def to_int(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(0).astype(int)


def normalize_text(text: str) -> str:
    if text is None:
        return ""
    value = str(text).strip()
    if value.lower() in {"nan", "none"}:
        return ""
    return " ".join(value.split())


def classify_severity(title: str, body: str) -> str:
    text = f"{title or ''} {body or ''}".strip()
    if HIGH_RISK_PATTERN.search(text):
        return "high_risk"
    if MODERATE_PATTERN.search(text):
        return "moderate"
    return "mild"


def is_informational_question(title: str, body: str) -> bool:
    clean_title = normalize_text(title)
    clean_body = normalize_text(body)
    if INFORMATIONAL_TITLE_PATTERN.search(clean_title):
        return True

    lower_text = f"{clean_title} {clean_body}".lower()
    informational_phrases = [
        "is it normal",
        "how do i",
        "what can i do",
        "am i",
        "should i",
    ]
    return any(p in lower_text for p in informational_phrases)


def aggregate_reference_rows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["questionID"] = df["questionID"].astype(str)
    df["upvotes_num"] = to_int(df["upvotes"])
    df["views_num"] = to_int(df["views"])
    df["questionTitle"] = df["questionTitle"].map(normalize_text)
    df["questionText"] = df["questionText"].map(normalize_text)
    df["answerText"] = df["answerText"].map(normalize_text)

    ranked = df.sort_values(
        ["questionID", "upvotes_num", "views_num"], ascending=[True, False, False]
    )
    one_per_question = ranked.groupby("questionID", as_index=False).first()

    # Backfill title/text from any row of the same questionID when top-ranked row is sparse.
    def first_non_empty(series: pd.Series) -> str:
        for value in series:
            clean = normalize_text(value)
            if clean:
                return clean
        return ""

    title_map = (
        df.sort_values(["questionID", "views_num"], ascending=[True, False])
        .groupby("questionID")["questionTitle"]
        .apply(first_non_empty)
    )
    text_map = (
        df.sort_values(["questionID", "views_num"], ascending=[True, False])
        .groupby("questionID")["questionText"]
        .apply(first_non_empty)
    )

    one_per_question["questionID"] = one_per_question["questionID"].astype(str)
    one_per_question["questionTitle"] = (
        one_per_question["questionID"].map(title_map).fillna("").map(normalize_text)
    )
    one_per_question["questionText"] = (
        one_per_question["questionID"].map(text_map).fillna("").map(normalize_text)
    )
    one_per_question["answerText"] = one_per_question["answerText"].map(normalize_text)
    one_per_question["has_question_text"] = one_per_question["questionText"] != ""
    one_per_question["severity"] = one_per_question.apply(
        lambda row: classify_severity(row["questionTitle"], row["questionText"]), axis=1
    )
    one_per_question["is_higher_risk"] = one_per_question["severity"].isin(["high_risk", "moderate"])
    one_per_question["is_informational"] = one_per_question.apply(
        lambda row: is_informational_question(row["questionTitle"], row["questionText"]), axis=1
    )
    one_per_question["view_priority_score"] = (
        one_per_question["views_num"] * 10 + one_per_question["upvotes_num"]
    )
    return one_per_question


def pick_first(candidates: pd.DataFrame, selected_ids: set[str]) -> pd.Series | None:
    for _, row in candidates.iterrows():
        qid = row["questionID"]
        if qid not in selected_ids:
            return row
    return None


def try_add_row(
    row: pd.Series | None,
    selected_rows: list[pd.Series],
    selected_ids: set[str],
    topic_counts: Counter,
) -> bool:
    if row is None:
        return False
    qid = row["questionID"]
    if qid in selected_ids:
        return False
    selected_rows.append(row)
    selected_ids.add(qid)
    topic_counts[row["topic"]] += 1
    return True


def choose_next_candidate(
    remaining: pd.DataFrame,
    topic_counts: Counter,
    need_higher_risk: bool,
    need_informational_mild: bool,
    respect_topic_cap: bool,
) -> pd.Series | None:
    candidates = remaining
    if respect_topic_cap:
        candidates = candidates[candidates["topic"].map(lambda t: topic_counts[t] < MAX_PER_TOPIC)]
    if candidates.empty:
        return None

    if need_higher_risk:
        pool = candidates[candidates["is_higher_risk"]]
        if not pool.empty:
            return pool.iloc[0]

    if need_informational_mild:
        pool = candidates[(~candidates["is_higher_risk"]) & (candidates["is_informational"])]
        if not pool.empty:
            return pool.iloc[0]

    return candidates.iloc[0]


def build_question_set(target_size: int) -> pd.DataFrame:
    raw = load_dataset(DATASET_NAME, split="train").to_pandas()
    per_question = aggregate_reference_rows(raw)

    # S2 prompt requires title + text; exclude rows with empty question text.
    core_pool = per_question[
        per_question["topic"].isin(CORE_TOPICS) & per_question["has_question_text"]
    ].copy()
    core_pool = core_pool.sort_values(
        ["view_priority_score", "views_num", "upvotes_num"],
        ascending=[False, False, False],
    ).reset_index(drop=True)

    selected_rows: list[pd.Series] = []
    selected_ids: set[str] = set()
    topic_counts: Counter = Counter()

    # Base coverage pass: explicitly cover each core topic.
    min_per_topic = 3 if target_size >= len(CORE_TOPICS) * 3 else 2
    for topic in CORE_TOPICS:
        topic_df = core_pool[core_pool["topic"] == topic]
        if topic_df.empty:
            continue

        pass_pools: list[pd.DataFrame] = []
        pass_pools.append(topic_df[topic_df["is_higher_risk"]])
        mild_info_df = topic_df[(~topic_df["is_higher_risk"]) & (topic_df["is_informational"])]
        if mild_info_df.empty:
            mild_info_df = topic_df[~topic_df["is_higher_risk"]]
        pass_pools.append(mild_info_df)
        if min_per_topic >= 3:
            pass_pools.append(topic_df)

        for pool in pass_pools:
            if len(selected_rows) >= target_size:
                break
            if topic_counts[topic] >= min_per_topic:
                break
            chosen = pick_first(pool if not pool.empty else topic_df, selected_ids)
            try_add_row(chosen, selected_rows, selected_ids, topic_counts)

    remaining = core_pool[~core_pool["questionID"].isin(selected_ids)].copy().reset_index(drop=True)

    min_higher_risk = max(8, target_size // 3)
    min_informational_mild = max(6, target_size // 4)

    while len(selected_rows) < target_size and not remaining.empty:
        current_df = pd.DataFrame(selected_rows)
        higher_risk_count = int(current_df["is_higher_risk"].sum()) if not current_df.empty else 0
        informational_mild_count = int(
            ((~current_df["is_higher_risk"]) & (current_df["is_informational"])).sum()
        ) if not current_df.empty else 0

        need_higher_risk = higher_risk_count < min_higher_risk
        need_info_mild = informational_mild_count < min_informational_mild

        chosen = choose_next_candidate(
            remaining,
            topic_counts,
            need_higher_risk,
            need_info_mild,
            respect_topic_cap=True,
        )
        if chosen is None:
            chosen = choose_next_candidate(
                remaining,
                topic_counts,
                need_higher_risk,
                need_info_mild,
                respect_topic_cap=False,
            )
        if chosen is None:
            break

        added = try_add_row(chosen, selected_rows, selected_ids, topic_counts)
        if not added:
            break
        remaining = remaining[remaining["questionID"] != chosen["questionID"]]

    selected = pd.DataFrame(selected_rows).copy()
    selected = selected.sort_values(["topic", "views_num"], ascending=[True, False]).reset_index(drop=True)
    selected.insert(0, "question_set_item_id", [f"S2Q{idx:02d}" for idx in range(1, len(selected) + 1)])
    selected["scenario_id"] = "scenario2_single_turn"
    selected["selection_reason"] = (
        "pdf_strategy_topic_coverage+high_views+severity_mix+highest_upvoted_reference"
    )
    selected["sampling_strategy_id"] = "pdf_s2"
    selected["dataset_source"] = DATASET_NAME
    selected["dataset_snapshot"] = "latest"

    final_cols = [
        "question_set_item_id",
        "scenario_id",
        "questionID",
        "topic",
        "severity",
        "is_informational",
        "views_num",
        "upvotes_num",
        "questionTitle",
        "questionText",
        "answerText",
        "questionLink",
        "selection_reason",
        "sampling_strategy_id",
        "dataset_source",
        "dataset_snapshot",
    ]
    return selected[final_cols].rename(
        columns={
            "questionID": "question_id",
            "views_num": "views",
            "upvotes_num": "reference_answer_upvotes",
            "questionTitle": "question_title",
            "questionText": "question_text",
            "answerText": "reference_therapist_answer",
            "questionLink": "question_link",
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        default="data/processed/question_sets",
        help="Directory to write CSV/JSONL outputs.",
    )
    parser.add_argument(
        "--target-size",
        type=int,
        default=DEFAULT_TARGET_SIZE,
        help="Final question count (must be 20-25).",
    )
    args = parser.parse_args()

    if args.target_size < 20 or args.target_size > 25:
        raise ValueError("--target-size must be between 20 and 25.")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    question_set = build_question_set(target_size=args.target_size)

    csv_path = output_dir / "final_question_set.csv"
    jsonl_path = output_dir / "final_question_set.jsonl"

    question_set.to_csv(csv_path, index=False, encoding="utf-8-sig")
    question_set.to_json(jsonl_path, orient="records", lines=True, force_ascii=False)

    print(f"Wrote {len(question_set)} questions")
    print("Topic distribution:")
    print(question_set["topic"].value_counts().to_string())
    print("Severity distribution:")
    print(question_set["severity"].value_counts().to_string())
    print(csv_path)
    print(jsonl_path)


if __name__ == "__main__":
    main()
