# Paleography Web Text Triage Classifier

This project builds an embedding-based classifier for triaging short web text snippets related to Ancient Chinese paleography. The goal is to decide whether a snippet should be kept as scholarly discussion, primary transcription, dictionary/reference content, or discarded as noise when building a specialized paleography information retrieval corpus.

The current system primarily targets Chinese paleography-related text. English interface text is provided for usability, but the training and evaluation data are Chinese; English or mixed-language test inputs are outside the main target distribution and may be over-classified as `noise`.

The task is not ancient character recognition. It is a corpus filtering and document routing task: given a short text snippet from a public web source, classify what kind of material it is and whether it is useful for a paleography-focused collection.

## Research Question

Can sentence embeddings help classify and filter web text snippets for inclusion in an Ancient Chinese paleography information retrieval corpus?

## Hugging Face Resources

These links should be updated after publication:

- Dataset: `TODO`
- Model: `TODO`
- Space demo: `TODO`

## Label Set

The final dataset uses four labels:

| Short label | Full label | Meaning |
|---|---|---|
| `ksd` | `keep_scholarly_discussion` | Scholarly, explanatory, or research-oriented prose about paleography, oracle bones, bronze inscriptions, excavated texts, or script history. |
| `kpt` | `keep_primary_transcription` | Primary textual material such as oracle-bone transcriptions, bronze inscription transcriptions, excavated-text fragments, or inscription-like source text. |
| `kde` | `keep_dictionary_entry` | Dictionary-style or reference-style entries about characters, words, pronunciations, glosses, forms, or short definitions. |
| `noise` | `discard_noise_irrelevant` | Irrelevant, noisy, navigational, administrative, advertising, broken OCR, or otherwise unsuitable text. |

Metadata and catalogue records also exist in the wider paleography data environment. They are not used as a separate label in this project because they are highly structured. Object numbers, collection IDs, bibliographic fields, database rows, and catalogue fields are better handled by field extraction, table parsing, or database-specific processing than by short-text semantic classification.

## Dataset

The dataset contains 400 manually labeled Chinese snippets collected from public paleography-related web sources and reference pages. The intended input is therefore a Chinese snippet from a paleography-related webpage or reference source.

| Split | Rows | Per-label distribution |
|---|---:|---|
| Train | 280 | 70 per label |
| Validation | 60 | 15 per label |
| Test | 60 | 15 per label |
| Total | 400 | 100 per label |

Each CSV row contains:

- `id`: unique sample identifier
- `text`: input snippet
- `label`: one of `kpt`, `kde`, `ksd`, or `noise`
- `source_url`: source page or source reference
- `language`: currently `chinese`

The processed files are:

- `data/processed/train.csv`
- `data/processed/validation.csv`
- `data/processed/test.csv`

The original evaluation remains in Chinese. This is intentional: translating all snippets into English would change the genre signals that the task depends on, especially for primary transcriptions and dictionary entries. For readability, `report/bilingual_examples.md` provides representative test-set examples with English glosses. Users should test the demo with Chinese paleography-related snippets; English examples may receive unreliable predictions and can be biased toward `discard_noise_irrelevant`.

## Method

The system uses the sentence embedding model `intfloat/multilingual-e5-small`. Each snippet is encoded with the E5-style prefix:

```text
passage: {text}
```

Embeddings are normalized and saved as NumPy arrays:

- `data/processed/train_embeddings.npy`
- `data/processed/validation_embeddings.npy`
- `data/processed/test_embeddings.npy`

Three classifiers were trained on top of the embeddings:

1. Average embedding baseline: nearest class centroid in embedding space
2. Logistic Regression
3. Linear SVM

The final Gradio demo uses Logistic Regression because it tied with Linear SVM on the test set and supports class probabilities through `predict_proba`.

## Evaluation

All models were evaluated on validation and test splits. The test set was held out for final evaluation.

| Model | Validation Accuracy | Validation Macro F1 | Validation Errors | Test Accuracy | Test Macro F1 | Test Errors |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8500 | 0.8433 | 9 | 0.9333 | 0.9298 | 4 |
| Linear SVM | 0.8667 | 0.8623 | 8 | 0.9333 | 0.9298 | 4 |
| Average Embedding Baseline | 0.8667 | 0.8666 | 8 | 0.9167 | 0.9141 | 5 |

For Logistic Regression and Linear SVM, the test confusion matrix was:

| Gold \ Predicted | `kde` | `kpt` | `ksd` | `noise` |
|---|---:|---:|---:|---:|
| `kde` | 15 | 0 | 0 | 0 |
| `kpt` | 0 | 15 | 0 | 0 |
| `ksd` | 2 | 1 | 11 | 1 |
| `noise` | 0 | 0 | 0 | 15 |

The main error pattern is that `keep_scholarly_discussion` is sometimes confused with dictionary entries, primary transcriptions, or noise. This is understandable because short scholarly comments in paleography often contain character explanations, quoted source text, or bibliographic-looking phrases.

Detailed reports are stored in `results/`, including classification reports, confusion matrices, and error files.

## Demo

The project includes a Gradio demo with English and Chinese interface modes. The interface can be shown in either language, but the classifier itself is intended mainly for Chinese paleography-related snippets. Users can paste a snippet and receive:

- predicted label
- class confidence table
- short label explanation

Run locally:

```bash
conda activate lt
python app.py
```

Or use the full interpreter path used during development:

```bash
/home/huanyu/miniconda3/envs/lt/bin/python app.py
```

Then open:

```text
http://127.0.0.1:7860
```

## Reproducing the Pipeline

Install dependencies:

```bash
pip install -r requirements.txt
```

Prepare the cleaned data and splits:

```bash
python src/prepare_data.py
```

Train and evaluate the average embedding baseline:

```bash
python src/average_baseline.py --eval-split validation
python src/average_baseline.py --eval-split test
```

Train and evaluate Logistic Regression:

```bash
python src/logistic_regression.py --eval-split validation
python src/logistic_regression.py --eval-split test
```

Train and evaluate Linear SVM:

```bash
python src/svm.py --eval-split validation
python src/svm.py --eval-split test
```

The scripts reuse existing embedding files unless `--force-embeddings` is passed.

## Repository Structure

```text
data/
  raw/
  processed/
models/
  average_baseline.joblib
  logistic_regression.joblib
  linear_svm.joblib
  label_encoder.joblib
  label_mapping.json
results/
  *_metrics.csv
  *_report.txt
  *_confusion_matrix.csv
  *_errors.csv
src/
  app.py
  average_baseline.py
  embedding_utils.py
  logistic_regression.py
  prepare_data.py
  svm.py
report/
  bilingual_examples.md
app.py
requirements.txt
README.md
```

## Limitations

- The dataset is small and domain-specific, with 400 manually labeled samples.
- All final samples are Chinese, so performance on English or mixed-language sources is not tested. English inputs may be incorrectly treated as out-of-domain noise.
- Some labels are inherently ambiguous. Short scholarly comments may look like dictionary entries or primary source quotations.
- The dataset is drawn from a limited set of public sources, so source style may influence the classifier.
- Metadata and catalogue records were excluded as a separate class because they are better treated as structured extraction problems.

## Privacy and Ethics

The dataset uses public scholarly, reference, transcription, and webpage snippets. It does not intentionally include private or sensitive personal information. The classifier is intended for corpus filtering and research data organization, not for authoritative paleographic interpretation.

## AI Tool Reflection

AI coding assistance was used to help design the pipeline, write scripts, inspect errors, build the Gradio demo, and revise documentation. The outputs were manually checked by running the code, reading the generated files, comparing metrics, and correcting inconsistencies such as the original five-label plan versus the final four-label implementation.
