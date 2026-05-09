"""Clean and split the raw snippet dataset.

The raw CSV uses five columns:
id,text,label,source_url,language

Cleaning is conservative: only leading/trailing whitespace is removed.
Internal spaces in the text are preserved.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


EXPECTED_COLUMNS = ["id", "text", "label", "source_url", "language"]
VALID_LABELS = {"kpt", "kde", "ksd", "noise"}
VALID_LANGUAGES = {"chinese", "english", "mixed"}


def sort_by_id(df: pd.DataFrame) -> pd.DataFrame:
    sorted_df = df.copy()
    sorted_df["_id_sort"] = pd.to_numeric(sorted_df["id"], errors="coerce")
    sorted_df = sorted_df.sort_values(["_id_sort", "id"]).drop(columns=["_id_sort"])
    return sorted_df.reset_index(drop=True)


def load_and_clean(input_path: Path) -> pd.DataFrame:
    df = pd.read_csv(input_path, dtype=str, keep_default_na=False)

    if list(df.columns) != EXPECTED_COLUMNS:
        raise ValueError(
            f"Expected columns {EXPECTED_COLUMNS}, but found {list(df.columns)}"
        )

    for column in EXPECTED_COLUMNS:
        df[column] = df[column].astype(str).str.strip()

    missing_required = df[["id", "text", "label"]].eq("").any(axis=1)
    if missing_required.any():
        bad_ids = df.loc[missing_required, "id"].tolist()
        raise ValueError(f"Rows with missing id, text, or label: {bad_ids}")

    invalid_labels = sorted(set(df["label"]) - VALID_LABELS)
    if invalid_labels:
        raise ValueError(f"Invalid labels found: {invalid_labels}")

    invalid_languages = sorted(set(df["language"]) - VALID_LANGUAGES)
    if invalid_languages:
        raise ValueError(f"Invalid language values found: {invalid_languages}")

    duplicate_text_count = int(df.duplicated(subset=["text"]).sum())
    if duplicate_text_count:
        print(f"Warning: found {duplicate_text_count} exact duplicate text rows.")

    return df


def split_dataset(
    df: pd.DataFrame,
    validation_size: float,
    test_size: float,
    random_state: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train_df, temp_df = train_test_split(
        df,
        test_size=validation_size + test_size,
        random_state=random_state,
        stratify=df["label"],
        shuffle=True,
    )

    relative_test_size = test_size / (validation_size + test_size)
    validation_df, test_df = train_test_split(
        temp_df,
        test_size=relative_test_size,
        random_state=random_state,
        stratify=temp_df["label"],
        shuffle=True,
    )

    return sort_by_id(train_df), sort_by_id(validation_df), sort_by_id(test_df)


def print_summary(name: str, df: pd.DataFrame) -> None:
    print(f"\n{name}: {len(df)} rows")
    print(df["label"].value_counts().sort_index().to_string())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/raw/collected_snippets.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--validation-size", type=float, default=0.15)
    parser.add_argument("--test-size", type=float, default=0.15)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    df = load_and_clean(args.input)
    train_df, validation_df, test_df = split_dataset(
        df,
        validation_size=args.validation_size,
        test_size=args.test_size,
        random_state=args.random_state,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    sort_by_id(df).to_csv(args.output_dir / "cleaned_snippets.csv", index=False)
    train_df.to_csv(args.output_dir / "train.csv", index=False)
    validation_df.to_csv(args.output_dir / "validation.csv", index=False)
    test_df.to_csv(args.output_dir / "test.csv", index=False)

    print_summary("cleaned", df)
    print_summary("train", train_df)
    print_summary("validation", validation_df)
    print_summary("test", test_df)
    print(f"\nWrote files to {args.output_dir}")


if __name__ == "__main__":
    main()
