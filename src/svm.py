"""Linear SVM classifier on sentence embeddings."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
from sklearn.svm import LinearSVC

from embedding_utils import (
    encode_split,
    evaluate_and_save,
    load_label_encoder,
    load_split,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--model-dir", type=Path, default=Path("models"))
    parser.add_argument("--results-dir", type=Path, default=Path("results"))
    parser.add_argument("--eval-split", default="validation", choices=["validation", "test"])
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--force-embeddings", action="store_true")
    args = parser.parse_args()

    train_df = load_split(args.data_dir, "train")
    eval_df = load_split(args.data_dir, args.eval_split)
    label_encoder = load_label_encoder(train_df, args.model_dir)

    x_train = encode_split("train", train_df, args.data_dir, args.batch_size, args.force_embeddings)
    x_eval = encode_split(args.eval_split, eval_df, args.data_dir, args.batch_size, args.force_embeddings)
    y_train = label_encoder.transform(train_df["label"])
    y_eval = label_encoder.transform(eval_df["label"])

    model = LinearSVC(
        class_weight="balanced",
        random_state=args.random_state,
    )
    model.fit(x_train, y_train)

    args.model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.model_dir / "linear_svm.joblib")

    metrics = evaluate_and_save(
        "linear_svm",
        model,
        x_eval,
        y_eval,
        eval_df,
        label_encoder,
        args.results_dir,
        split=args.eval_split,
    )
    print(metrics)


if __name__ == "__main__":
    main()
