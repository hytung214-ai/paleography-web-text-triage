"""Gradio demo for the paleography text triage classifier."""

from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")

import gradio as gr
import joblib
from sentence_transformers import SentenceTransformer


ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT_DIR / "models"

MODEL_PATH = MODEL_DIR / "logistic_regression.joblib"
LABEL_ENCODER_PATH = MODEL_DIR / "label_encoder.joblib"
LABEL_MAPPING_PATH = MODEL_DIR / "label_mapping.json"

LABEL_EXPLANATIONS = {
    "en": {
        "keep_dictionary_entry": "Dictionary-style or reference-style text about a character, word, pronunciation, gloss, or definition.",
        "keep_primary_transcription": "Primary textual material such as inscription text, oracle-bone transcription, bronze inscription transcription, or excavated-text fragments.",
        "keep_scholarly_discussion": "Scholarly, explanatory, or research-oriented prose about paleography, oracle bones, bronze inscriptions, excavated texts, or script history.",
        "discard_noise_irrelevant": "Irrelevant, noisy, navigational, advertising, broken OCR, or unrelated text that should not be kept for the corpus.",
    },
    "zh": {
        "keep_dictionary_entry": "字典式或工具书式内容，例如字头解释、读音、训释、字形说明或简短定义。",
        "keep_primary_transcription": "一手文本材料，例如甲骨释文、金文释文、出土文献片段或铭文文本。",
        "keep_scholarly_discussion": "关于古文字学、甲骨文、金文、出土文献或文字史的学术性、解释性或研究性论述。",
        "discard_noise_irrelevant": "无关或噪声文本，例如网页导航、广告、登录提示、破碎 OCR 或不适合进入语料库的内容。",
    },
}

LABEL_DISPLAY_NAMES = {
    "en": {
        "keep_dictionary_entry": "keep_dictionary_entry",
        "keep_primary_transcription": "keep_primary_transcription",
        "keep_scholarly_discussion": "keep_scholarly_discussion",
        "discard_noise_irrelevant": "discard_noise_irrelevant",
    },
    "zh": {
        "keep_dictionary_entry": "字典条目 / keep_dictionary_entry",
        "keep_primary_transcription": "一手释文 / keep_primary_transcription",
        "keep_scholarly_discussion": "学术讨论 / keep_scholarly_discussion",
        "discard_noise_irrelevant": "噪声或无关文本 / discard_noise_irrelevant",
    },
}

LANGUAGE_OPTIONS = ["English", "中文"]

UI_TEXT = {
    "en": {
        "title": "# Paleography Web Text Triage Classifier",
        "description": (
            "Classifies short Ancient Chinese paleography-related web snippets "
            "as scholarly discussion, primary transcription, dictionary entry, or noise."
        ),
        "language_label": "Language",
        "input_label": "Input text snippet",
        "input_placeholder": "Paste a paleography-related web text snippet here...",
        "submit": "Classify",
        "clear": "Clear",
        "prediction_label": "Predicted label",
        "confidence_label": "Class confidence",
        "explanation_label": "Label explanation",
        "examples_label": "Examples",
    },
    "zh": {
        "title": "# 古文字学网页文本分流分类器",
        "description": "将古文字学相关网页片段分为学术讨论、一手释文、字典条目或噪声/无关文本。",
        "language_label": "语言",
        "input_label": "输入文本片段",
        "input_placeholder": "在这里粘贴或输入一段古文字学相关网页文本片段...",
        "submit": "分类",
        "clear": "清空",
        "prediction_label": "预测类别",
        "confidence_label": "类别置信度",
        "explanation_label": "类别解释",
        "examples_label": "示例",
    },
}


def load_assets():
    label_mapping = json.loads(LABEL_MAPPING_PATH.read_text(encoding="utf-8"))
    embedding_model_name = label_mapping["embedding_model"]
    label_descriptions = label_mapping["descriptions"]

    embedding_model = SentenceTransformer(embedding_model_name)
    classifier = joblib.load(MODEL_PATH)
    label_encoder = joblib.load(LABEL_ENCODER_PATH)
    return embedding_model, classifier, label_encoder, label_descriptions


EMBEDDING_MODEL, CLASSIFIER, LABEL_ENCODER, LABEL_DESCRIPTIONS = load_assets()


def normalize_language(language: str) -> str:
    return "zh" if language == "中文" else "en"


def localize_label(full_label: str, language: str) -> str:
    return LABEL_DISPLAY_NAMES[language].get(full_label, full_label)


def format_confidences(confidences: dict[str, float], language: str) -> str:
    title = UI_TEXT[language]["confidence_label"]
    if not confidences:
        return f"### {title}\n"

    rows = ["| Label | Confidence |", "|---|---:|"]
    if language == "zh":
        rows = ["| 类别 | 置信度 |", "|---|---:|"]

    for label, probability in confidences.items():
        rows.append(f"| {label} | {probability:.1%} |")
    return f"### {title}\n\n" + "\n".join(rows)


def predict(text: str, language: str):
    output_language = normalize_language(language)
    cleaned_text = text.strip()
    if not cleaned_text:
        message = (
            "请输入一段古文字学相关网页文本。"
            if output_language == "zh"
            else "Paste a paleography-related web text snippet to classify it."
        )
        return (
            "无输入" if output_language == "zh" else "No input",
            format_confidences({}, output_language),
            message,
        )

    embedding = EMBEDDING_MODEL.encode(
        [f"passage: {cleaned_text}"],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    encoded_prediction = CLASSIFIER.predict(embedding)
    short_label = LABEL_ENCODER.inverse_transform(encoded_prediction)[0]
    full_label = LABEL_DESCRIPTIONS.get(short_label, short_label)

    probabilities = CLASSIFIER.predict_proba(embedding)[0]
    probability_labels = LABEL_ENCODER.inverse_transform(CLASSIFIER.classes_)
    confidences = {
        localize_label(LABEL_DESCRIPTIONS.get(label, label), output_language): float(
            probability
        )
        for label, probability in zip(probability_labels, probabilities)
    }
    confidences = dict(
        sorted(confidences.items(), key=lambda item: item[1], reverse=True)
    )

    explanation = LABEL_EXPLANATIONS[output_language].get(
        full_label,
        "暂无类别解释。" if output_language == "zh" else "No label explanation available.",
    )
    return (
        localize_label(full_label, output_language),
        format_confidences(confidences, output_language),
        explanation,
    )


EXAMPLES = [
    ["丸与完双声叠韵。"],
    ["己亥卜古貞有眾之十二月"],
    ["甲骨文是中国商代晚期刻写在龟甲和兽骨上的文字材料，对研究早期汉字形体和商代历史具有重要价值。"],
    ["登录 注册 搜索 首页 上一页 下一页 分享"],
]


def update_ui(language: str, text_value: str):
    output_language = normalize_language(language)
    text = UI_TEXT[output_language]

    if text_value and text_value.strip():
        predicted_label, confidences, explanation = predict(text_value, language)
    else:
        predicted_label = ""
        confidences = format_confidences({}, output_language)
        explanation = ""

    return (
        text["title"],
        text["description"],
        gr.update(label=text["input_label"], placeholder=text["input_placeholder"]),
        gr.update(value=text["submit"]),
        gr.update(value=text["clear"]),
        gr.update(label=text["prediction_label"], value=predicted_label),
        confidences,
        gr.update(label=text["explanation_label"], value=explanation),
        f"### {text['examples_label']}",
    )


with gr.Blocks(title="Paleography Web Text Triage Classifier") as demo:
    title_markdown = gr.Markdown(UI_TEXT["en"]["title"])
    description_markdown = gr.Markdown(UI_TEXT["en"]["description"])

    language_radio = gr.Radio(
        choices=LANGUAGE_OPTIONS,
        value="English",
        label=UI_TEXT["en"]["language_label"],
    )

    input_text = gr.Textbox(
        label=UI_TEXT["en"]["input_label"],
        lines=6,
        placeholder=UI_TEXT["en"]["input_placeholder"],
    )

    with gr.Row():
        submit_button = gr.Button(UI_TEXT["en"]["submit"], variant="primary")
        clear_button = gr.Button(UI_TEXT["en"]["clear"])

    prediction_output = gr.Textbox(label=UI_TEXT["en"]["prediction_label"])
    confidence_output = gr.Markdown(format_confidences({}, "en"))
    explanation_output = gr.Textbox(label=UI_TEXT["en"]["explanation_label"])

    examples_markdown = gr.Markdown(f"### {UI_TEXT['en']['examples_label']}")
    gr.Examples(
        examples=EXAMPLES,
        inputs=input_text,
        label=None,
    )

    submit_button.click(
        fn=predict,
        inputs=[input_text, language_radio],
        outputs=[prediction_output, confidence_output, explanation_output],
    )
    clear_button.click(
        fn=lambda language: (
            "",
            "",
            format_confidences({}, normalize_language(language)),
            "",
        ),
        inputs=language_radio,
        outputs=[
            input_text,
            prediction_output,
            confidence_output,
            explanation_output,
        ],
    )
    language_radio.change(
        fn=update_ui,
        inputs=[language_radio, input_text],
        outputs=[
            title_markdown,
            description_markdown,
            input_text,
            submit_button,
            clear_button,
            prediction_output,
            confidence_output,
            explanation_output,
            examples_markdown,
        ],
    )


if __name__ == "__main__":
    demo.launch()
