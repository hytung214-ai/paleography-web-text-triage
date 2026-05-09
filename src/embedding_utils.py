"""Shared utilities for embedding-based classifiers."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.preprocessing import LabelEncoder


EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-small"
LABEL_DESCRIPTIONS = {
    "kpt": "keep_primary_transcription",
    "kde": "keep_dictionary_entry",
    "ksd": "keep_scholarly_discussion",
    "noise": "discard_noise_irrelevant",
}


def load_split(data_dir: Path, split: str) -> pd.DataFrame:
    path = data_dir / f"{split}.csv"
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    expected = {"id", "text", "label", "source_url", "language"}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"{path} is missing columns: {sorted(missing)}")
    return df


def load_label_encoder(train_df: pd.DataFrame, model_dir: Path) -> LabelEncoder:
    model_dir.mkdir(parents=True, exist_ok=True)
    encoder_path = model_dir / "label_encoder.joblib"
    label_mapping_path = model_dir / "label_mapping.json"

    encoder = LabelEncoder()
    encoder.fit(train_df["label"])
    joblib.dump(encoder, encoder_path)

    label_mapping = {
        "classes": encoder.classes_.tolist(),
        "descriptions": LABEL_DESCRIPTIONS,
        "embedding_model": EMBEDDING_MODEL_NAME,
    }
    label_mapping_path.write_text(
        json.dumps(label_mapping, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return encoder


def encode_split(
    split: str,
    df: pd.DataFrame,
    data_dir: Path,
    batch_size: int,
    force: bool = False,
) -> np.ndarray:
    embedding_path = data_dir / f"{split}_embeddings.npy"
    if embedding_path.exists() and not force:
        return np.load(embedding_path)

    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    texts = [f"passage: {text}" for text in df["text"].tolist()]
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True,
    )
    np.save(embedding_path, embeddings)
    return embeddings


def evaluate_and_save(
    model_name: str,
    model,
    x_eval: np.ndarray,
    y_eval: np.ndarray,
    eval_df: pd.DataFrame,
    label_encoder: LabelEncoder,
    results_dir: Path,
    split: str = "validation",
) -> dict[str, float | str]:
    results_dir.mkdir(parents=True, exist_ok=True)
    predictions = model.predict(x_eval)
    predicted_labels = label_encoder.inverse_transform(predictions)
    gold_labels = label_encoder.inverse_transform(y_eval)

    report = classification_report(
        gold_labels,
        predicted_labels,
        labels=label_encoder.classes_,
        digits=4,
        zero_division=0,
    )
    (results_dir / f"{model_name}_{split}_report.txt").write_text(
        f"# {model_name} on {split}\n\n{report}\n",
        encoding="utf-8",
    )

    matrix = confusion_matrix(
        gold_labels,
        predicted_labels,
        labels=label_encoder.classes_,
    )
    matrix_df = pd.DataFrame(
        matrix,
        index=[f"gold_{label}" for label in label_encoder.classes_],
        columns=[f"pred_{label}" for label in label_encoder.classes_],
    )
    matrix_df.to_csv(results_dir / f"{model_name}_{split}_confusion_matrix.csv")

    error_df = eval_df.copy()
    error_df["gold_label"] = gold_labels
    error_df["predicted_label"] = predicted_labels
    error_df = error_df[error_df["gold_label"] != error_df["predicted_label"]]
    error_df.to_csv(results_dir / f"{model_name}_{split}_errors.csv", index=False)

    metrics = {
        "model": model_name,
        "split": split,
        "accuracy": accuracy_score(gold_labels, predicted_labels),
        "macro_f1": f1_score(gold_labels, predicted_labels, average="macro"),
        "num_errors": int(len(error_df)),
        "prediction_distribution": json.dumps(
            pd.Series(predicted_labels).value_counts().sort_index().to_dict(),
            ensure_ascii=False,
        ),
    }
    pd.DataFrame([metrics]).to_csv(
        results_dir / f"{model_name}_{split}_metrics.csv",
        index=False,
    )
    return metrics
