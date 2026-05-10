"""Plot 2D projections of saved text embeddings."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data" / "processed"
RESULTS_DIR = ROOT_DIR / "results"
FIGURE_DIR = ROOT_DIR / "report" / "figures"

LABEL_ORDER = ["kde", "kpt", "ksd", "noise"]
LABEL_COLORS = {
    "kde": "#1f77b4",
    "kpt": "#ff7f0e",
    "ksd": "#2ca02c",
    "noise": "#d62728",
}
SPLIT_MARKERS = {
    "train": "o",
    "validation": "s",
    "test": "^",
}


def load_split(split: str) -> tuple[pd.DataFrame, np.ndarray]:
    frame = pd.read_csv(DATA_DIR / f"{split}.csv")
    embeddings = np.load(DATA_DIR / f"{split}_embeddings.npy")
    frame = frame.copy()
    frame["split"] = split
    return frame, embeddings


def load_all_data() -> tuple[pd.DataFrame, np.ndarray]:
    frames = []
    embedding_arrays = []
    for split in ["train", "validation", "test"]:
        frame, embeddings = load_split(split)
        frames.append(frame)
        embedding_arrays.append(embeddings)
    return pd.concat(frames, ignore_index=True), np.vstack(embedding_arrays)


def add_error_flags(frame: pd.DataFrame) -> pd.DataFrame:
    errors_path = RESULTS_DIR / "logistic_regression_test_errors.csv"
    errors = pd.read_csv(errors_path)
    error_ids = set(errors["id"].astype(str))
    pred_by_id = {
        str(row.id): row.predicted_label for row in errors.itertuples(index=False)
    }

    frame = frame.copy()
    frame["id_str"] = frame["id"].astype(str)
    frame["is_error"] = frame["id_str"].isin(error_ids)
    frame["predicted_label"] = frame["id_str"].map(pred_by_id)
    return frame


def project_embeddings(embeddings: np.ndarray, method: str) -> np.ndarray:
    if method == "pca":
        return PCA(n_components=2, random_state=42).fit_transform(embeddings)
    if method == "tsne":
        return TSNE(
            n_components=2,
            perplexity=30,
            init="pca",
            learning_rate="auto",
            random_state=42,
        ).fit_transform(embeddings)
    raise ValueError(f"Unknown projection method: {method}")


def plot_projection(frame: pd.DataFrame, method: str, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 5.2), dpi=180)

    for split, marker in SPLIT_MARKERS.items():
        for label in LABEL_ORDER:
            mask = (frame["split"] == split) & (frame["label"] == label)
            if not mask.any():
                continue
            ax.scatter(
                frame.loc[mask, "x"],
                frame.loc[mask, "y"],
                s=28 if split == "test" else 20,
                marker=marker,
                color=LABEL_COLORS[label],
                alpha=0.78 if split == "test" else 0.42,
                linewidths=0,
            )

    errors = frame[frame["is_error"]]
    ax.scatter(
        errors["x"],
        errors["y"],
        s=130,
        marker="x",
        color="black",
        linewidths=2.0,
        label="test error",
        zorder=5,
    )
    for row in errors.itertuples(index=False):
        ax.annotate(
            f"id {row.id}\n{row.label}->{row.predicted_label}",
            (row.x, row.y),
            xytext=(6, 6),
            textcoords="offset points",
            fontsize=7,
            color="black",
        )

    label_handles = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label=label,
            markerfacecolor=LABEL_COLORS[label],
            markersize=7,
        )
        for label in LABEL_ORDER
    ]
    split_handles = [
        plt.Line2D(
            [0],
            [0],
            marker=marker,
            color="#555555",
            label=split,
            linestyle="None",
            markersize=7,
        )
        for split, marker in SPLIT_MARKERS.items()
    ]
    error_handle = plt.Line2D(
        [0],
        [0],
        marker="x",
        color="black",
        label="test error",
        linestyle="None",
        markersize=8,
        markeredgewidth=2,
    )

    first_legend = ax.legend(
        handles=label_handles,
        title="Gold label",
        loc="upper left",
        frameon=True,
        fontsize=8,
        title_fontsize=9,
    )
    ax.add_artist(first_legend)
    ax.legend(
        handles=split_handles + [error_handle],
        title="Split / error",
        loc="lower right",
        frameon=True,
        fontsize=8,
        title_fontsize=9,
    )

    ax.set_title(f"{method.upper()} projection of E5 embeddings")
    ax.set_xlabel(f"{method.upper()} dimension 1")
    ax.set_ylabel(f"{method.upper()} dimension 2")
    ax.grid(True, linewidth=0.3, alpha=0.35)
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    frame, embeddings = load_all_data()
    frame = add_error_flags(frame)

    for method in ["pca", "tsne"]:
        coordinates = project_embeddings(embeddings, method)
        projected = frame.copy()
        projected["x"] = coordinates[:, 0]
        projected["y"] = coordinates[:, 1]
        projected.to_csv(FIGURE_DIR / f"embedding_distribution_{method}.csv", index=False)
        plot_projection(
            projected,
            method,
            FIGURE_DIR / f"embedding_distribution_{method}.png",
        )

    print(f"Saved figures and coordinates to {FIGURE_DIR}")


if __name__ == "__main__":
    main()
