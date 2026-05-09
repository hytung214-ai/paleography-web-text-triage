# Annotation Guidelines: Paleography Web Text Triage Classifier
# 标注指南：古文字学网页文本分流分类器

## Purpose
## 目的

This guideline defines how text snippets are labeled for the Paleography Web Text Triage Classifier. The classifier routes short web snippets into categories useful for building an Ancient Chinese paleography information retrieval corpus.

本指南说明古文字学网页文本分流分类器的数据如何标注。分类器的目标是把短网页片段分到适合古文字学信息检索语料建设的类别中。

The task is not to recognize ancient character shapes or to provide expert interpretation of inscriptions. The task is to identify the main function of a text snippet: scholarly discussion, primary transcription, dictionary or reference entry, or irrelevant noise.

本任务不是识别古文字字形，也不是进行专业铭文释读。标注时判断的是文本片段的主要功能：学术讨论、一手释文、字典或工具书条目，或无关噪声。

## Labels
## 标签

The dataset uses four short labels in the CSV files. Each short label maps to a full descriptive label.

数据集在 CSV 中使用四个短标签。每个短标签对应一个完整说明性标签。

| Short label | Full label |
|---|---|
| `ksd` | `keep_scholarly_discussion` |
| `kpt` | `keep_primary_transcription` |
| `kde` | `keep_dictionary_entry` |
| `noise` | `discard_noise_irrelevant` |

## Label Definitions
## 标签定义

### `ksd`: `keep_scholarly_discussion`

Use this label when the snippet contains scholarly, explanatory, or research-oriented prose about paleography, oracle bones, bronze inscriptions, excavated texts, ancient scripts, character forms, or script history.

当片段包含关于古文字学、甲骨文、金文、出土文献、古文字形体或文字史的学术性、解释性、研究性论述时，使用此标签。

Typical examples:

- encyclopedia-style explanations of oracle bone script or bronze inscriptions
- article abstracts, introductions, or research summaries
- interpretive discussion that cites scholars, manuscripts, inscriptions, or previous research

典型例子：

- 解释甲骨文、金文等对象的百科式段落
- 论文摘要、引言或研究综述
- 引用学者、简帛、铭文或既有研究的考释性讨论

Do not use this label for snippets that are mainly raw inscription text or dictionary definitions.

如果片段主要是原始释文或字典定义，不使用此标签。

### `kpt`: `keep_primary_transcription`

Use this label when the snippet mainly contains primary textual material, such as oracle-bone transcriptions, bronze inscription transcriptions, excavated-text fragments, numbered inscription lines, or ancient source text with minimal modern explanation.

当片段主要包含一手文本材料时，使用此标签，例如甲骨释文、金文释文、出土文献片段、带编号的铭文行，或几乎没有现代解释的古代原始文本。

Typical examples:

- compact divination or inscription lines
- bronze vessel inscription transcriptions
- excavated manuscript fragments
- source-text-like lines where the transcription itself is the useful content

典型例子：

- 简短的卜辞或铭文行
- 青铜器铭文释文
- 出土文献片段
- 释文本身是主要有用内容的一手文本

Do not use this label for a modern paragraph that explains the historical value or interpretation of the text. That should usually be `ksd`.

如果片段是现代段落，主要在解释文本的历史价值或释读问题，通常应标为 `ksd`。

### `kde`: `keep_dictionary_entry`

Use this label when the snippet is a dictionary-style, lexicon-style, or reference-style entry about a character, word, pronunciation, radical, gloss, form, variant, or short definition.

当片段是关于字、词、读音、部首、训释、字形、异体或简短定义的字典式、词典式、工具书式条目时，使用此标签。

Typical examples:

- Shuowen-style character definitions
- short lexical notes about character forms or meanings
- entries with pronunciation, radical, gloss, or cross-reference information
- reference notes that define a character rather than develop an argument

典型例子：

- 《说文》式字头解释
- 关于字形或字义的简短词条
- 包含读音、部首、训释或参见信息的条目
- 主要功能是定义某字，而不是展开学术论证的工具书说明

Do not use this label for extended scholarly argument. If the snippet discusses a research problem in prose, use `ksd`.

如果片段展开的是学术论证，而不是词条式定义，应标为 `ksd`。

### `noise`: `discard_noise_irrelevant`

Use this label when the snippet is irrelevant, too noisy, mostly navigation text, administrative text, advertising, login text, broken OCR, repeated formatting, publication metadata, or unrelated modern content.

当片段无关、噪声过多，或主要是网页导航、管理信息、广告、登录提示、破碎 OCR、重复格式、发布日期等元信息，或无关现代内容时，使用此标签。

Typical examples:

- login, register, search, previous page, next page, share, font-size controls
- page publication-date lines or boilerplate metadata without useful content
- unrelated modern text about shopping, weather, sports, or course administration
- OCR fragments that are too broken to function as transcription or dictionary content

典型例子：

- 登录、注册、搜索、上一页、下一页、分享、字体大小等网页控件文本
- 没有实质内容的发布日期或网页元信息
- 关于购物、天气、体育、课程事务等无关现代文本
- 破碎到无法作为释文或字典内容使用的 OCR 片段

Do not use this label for noisy but still usable dictionary, transcription, or scholarly content. Label by the main usable function when possible.

如果片段虽然有噪声但仍可作为字典条目、释文或学术内容使用，应尽量按主要可用功能标注，而不是直接标为噪声。

## Decision Rules
## 判定规则

Label the snippet by its main function, not by a single keyword.

根据片段的主要功能标注，而不是只根据单个关键词标注。

If the useful dominant content is inscription or source text, choose `kpt`.

如果主要有用内容是铭文、释文或一手文本，选择 `kpt`。

If the snippet defines a character, word, form, pronunciation, or gloss in a compact reference style, choose `kde`.

如果片段以紧凑工具书形式定义字、词、字形、读音或训释，选择 `kde`。

If the snippet explains, interprets, compares, cites research, or develops an argument in prose, choose `ksd`.

如果片段以段落形式解释、考释、比较、引用研究或展开论证，选择 `ksd`。

If the snippet is not useful for a paleography corpus, choose `noise`.

如果片段对古文字学语料库没有用，选择 `noise`。

If a snippet mixes metadata and transcription, choose `kpt` only when the transcription is the dominant useful content. If it is mostly structured metadata without useful prose, transcription, or dictionary content, choose `noise`.

如果片段同时包含元数据和释文，只有当释文是主要有用内容时才选择 `kpt`。如果主要是结构化元数据，没有可用论述、释文或字典内容，选择 `noise`。

Catalogue and metadata records are not a separate label in this version. Object numbers, collection IDs, bibliographic fields, and catalogue rows are treated as outside the main short-text classification task unless they contain useful prose, transcription, or dictionary content.

本版本不把目录和元数据记录设为单独标签。器号、馆藏号、书目信息和目录行等高度结构化内容，除非包含有用论述、释文或字典内容，否则视为本短文本分类任务之外的材料。

## Dataset Fields
## 数据字段

The final CSV files use five columns:

最终 CSV 文件使用五个字段：

| Field | Meaning |
|---|---|
| `id` | Unique sample identifier. |
| `text` | Text snippet used as classifier input. |
| `label` | One of `ksd`, `kpt`, `kde`, or `noise`. |
| `source_url` | Public source URL or source reference. |
| `language` | `chinese`, `english`, or `mixed`. |

## Quality Rules
## 质量规则

Keep snippets short and focused. A practical range is about 30 to 300 Chinese characters, or 20 to 200 English words.

片段应简短且聚焦。实际范围约为 30 到 300 个汉字，或 20 到 200 个英文词。

Record the source URL whenever possible.

尽可能记录来源 URL。

Avoid exact duplicate snippets.

避免完全重复的文本片段。

Do not collect real sensitive personal information.

不要收集真实敏感个人信息。

Do not copy long copyrighted passages.

不要复制大段受版权保护文本。

Use public sources and do not bypass access restrictions.

使用公开来源，不绕过访问限制。
