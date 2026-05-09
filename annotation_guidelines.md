# Annotation Guidelines: Paleography Web Text Triage Classifier
# 标注指南：古文字学网页文本分流分类器

## Project Purpose
## 项目目的

This dataset supports a classifier that routes web text snippets into useful categories for building an Ancient Chinese paleography information retrieval corpus.
该数据集用于支持一个分类器，将网页文本片段分流到适合构建中国古文字学信息检索语料库的类别中。

The task is not to identify ancient character shapes.
本任务不是识别古文字字形。

The task is not to professionally interpret oracle bone or bronze inscriptions.
本任务也不是专业释读甲骨文或金文。

The task is to classify the function and usefulness of a text snippet.
本任务是分类一个文本片段的功能和可用性。

## Label Set
## 标签体系

### `keep_scholarly_discussion`

Use this label when the snippet contains scholarly, explanatory, or research-oriented prose about paleography, oracle bones, bronze inscriptions, excavated texts, Chinese script history, or related topics.
当片段包含关于古文字学、甲骨文、金文、出土文献、中国文字史或相关主题的学术性、解释性或研究性论述时，使用此标签。

Positive example type 1: an encyclopedia paragraph explaining oracle bone script.
正例类型 1：解释甲骨文的百科段落。

Positive example type 2: an article abstract discussing bronze inscriptions or excavated manuscripts.
正例类型 2：讨论金文或出土文献的论文摘要。

Negative example: a database row that mainly contains inscription text should usually be `keep_primary_transcription`, not this label.
反例：主要包含铭文释文的数据库行通常应标为 `keep_primary_transcription`，而不是此标签。

### `keep_primary_transcription`

Use this label when the snippet mainly contains primary textual material, such as oracle-bone transcriptions, bronze inscription transcriptions, excavated-text transcriptions, numbered inscription text, or ancient text fragments.
当片段主要包含一手文本材料，例如甲骨释文、金文释文、出土文献释文、带编号铭文文本或古文献片段时，使用此标签。

Positive example type 1: a bronze inscription transcription from a search result page.
正例类型 1：来自检索结果页的一段金文释文。

Positive example type 2: a short ancient text or inscription line with minimal explanation.
正例类型 2：几乎没有解释的一小段古文或铭文文本。

Negative example: a modern paragraph explaining the historical importance of oracle bones should be `keep_scholarly_discussion`, not this label.
反例：解释甲骨文历史重要性的现代段落应标为 `keep_scholarly_discussion`，而不是此标签。

### `keep_dictionary_entry`

Use this label when the snippet is a dictionary-style, lexicon-style, or reference-style entry about a character, word, pronunciation, radical, gloss, or short definition.
当片段是关于字、词、读音、部首、训释或简短定义的字典式、词典式或工具书式条目时，使用此标签。

Positive example type 1: a Shuowen-style entry explaining a character.
正例类型 1：《说文》式的字头解释。

Positive example type 2: a modern dictionary entry with pronunciation, meaning, and character information.
正例类型 2：包含读音、释义和字形信息的现代字典条目。

Negative example: a museum object record that only lists period, material, and accession number should be `discard_noise_irrelevant`, not this label.
反例：只列出年代、材质和馆藏编号的博物馆器物记录应标为 `discard_noise_irrelevant`，而不是此标签。

### `discard_noise_irrelevant`

Use this label when the snippet is irrelevant, too noisy, mostly navigation text, advertising text, login text, broken OCR, repeated formatting, or unrelated modern content.
当片段无关、噪声过多、主要是网页导航、广告、登录提示、破碎 OCR、重复格式文本或无关现代内容时，使用此标签。

Positive example type 1: webpage menu text such as login, register, search, previous page, next page, and share buttons.
正例类型 1：登录、注册、搜索、上一页、下一页、分享按钮等网页菜单文字。

Positive example type 2: unrelated modern text about shopping, sports, weather, or course administration.
正例类型 2：关于购物、体育、天气或课程事务的无关现代文本。

Negative example: noisy but still recognizable Shuowen OCR should usually be `keep_dictionary_entry` unless the noise makes it unusable.
反例：有噪声但仍可识别的《说文》OCR 通常应标为 `keep_dictionary_entry`，除非噪声严重到不可用。

## General Annotation Rules
## 通用标注规则

Label the snippet by its main function, not by a single keyword.
根据片段的主要功能标注，而不是只根据单个关键词标注。

If a snippet contains both metadata and transcription, choose `keep_primary_transcription` when the transcription is the useful dominant content.
如果片段同时包含元数据和释文，且释文是主要有用内容，选择 `keep_primary_transcription`。

If the text is mostly structured metadata without useful prose, transcription, or dictionary content, choose `discard_noise_irrelevant`.
如果文本主要是结构化元数据，且没有有用论述、释文或字典内容，选择 `discard_noise_irrelevant`。

Metadata and catalogue records are not a separate label in this version. They exist in the source environment, but because they are highly structured, they are treated as outside the main short-text classification task unless they include useful prose, transcription, or dictionary content.
元数据和目录记录在此版本中不是单独标签。它们确实存在于数据来源环境中，但由于高度结构化，本项目将它们视为短文本分类任务之外的材料；除非其中包含有用论述、释文或字典内容，否则不作为保留类别处理。

If the text is mostly inscription or source text, choose `keep_primary_transcription`.
如果文本主要是铭文或一手文本，选择 `keep_primary_transcription`。

If the text explains or discusses a topic in prose, choose `keep_scholarly_discussion`.
如果文本以段落形式解释或讨论某个主题，选择 `keep_scholarly_discussion`。

If the text defines a character or word, choose `keep_dictionary_entry`.
如果文本定义某个字或词，选择 `keep_dictionary_entry`。

If the text is not useful for a paleography corpus, choose `discard_noise_irrelevant`.
如果文本对古文字学语料库没有用，选择 `discard_noise_irrelevant`。

## Data Collection Rules
## 数据收集规则

Keep snippets short and focused.
保持片段简短且聚焦。

Recommended snippet length is 30 to 300 Chinese characters or 20 to 200 English words.
推荐片段长度为 30 到 300 个汉字，或 20 到 200 个英文词。

Record the source URL whenever possible.
尽可能记录来源 URL。

Do not collect long copyrighted passages.
不要收集大段受版权保护文本。

Do not include real sensitive personal information.
不要包含真实敏感个人信息。

Avoid exact duplicate snippets.
避免完全重复的文本片段。

Use `chinese`, `english`, or `mixed` for the language field.
语言字段使用 `chinese`、`english` 或 `mixed`。

Use the five CSV columns `id`, `text`, `label`, `source_url`, and `language`.
CSV 使用五个字段：`id`、`text`、`label`、`source_url` 和 `language`。

## Day 2 Target Counts
## 第二天目标数量

| Label | Target Count | Minimum Count |
|---|---:|---:|
| `keep_scholarly_discussion` | 100 | 30 |
| `keep_primary_transcription` | 100 | 30 |
| `keep_dictionary_entry` | 100 | 30 |
| `discard_noise_irrelevant` | 100 | 30 |

The target dataset size is 400 samples.
目标数据集规模是 400 条样本。

The minimum workable dataset size is 120 samples.
最低可行数据集规模是 120 条样本。
