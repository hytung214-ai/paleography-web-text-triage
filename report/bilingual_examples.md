# Bilingual Example Table

This table uses examples from the held-out test set and is for explanation only. The original dataset and evaluation remain in Chinese because the classification task depends on genre and form signals in paleography materials. Translating all snippets into English would change primary transcriptions and dictionary entries into modern explanatory prose, making the evaluation less faithful to the original corpus-filtering task.

| Test id | Label | Original snippet | English gloss | Why this label fits |
|---:|---|---|---|---|
| 33 | `keep_primary_transcription` | 壬戌卜母壬歲惟小羊 | Oracle-bone style divination/transcription fragment with a cyclical date and ritual wording. | The snippet is primary textual material rather than modern explanation. Its value is the transcription form itself. |
| 223 | `keep_primary_transcription` | 癸卯貞惟先于大甲父丁 | Compact inscription-style line with divination formula wording and ancestral names. | The wording is formulaic and source-text-like, so it belongs to primary transcription. |
| 74 | `keep_dictionary_entry` | 《說文》：“心，人心。土藏，在身之中。象形。博士說以為火藏。” | A Shuowen-style dictionary definition for the character "heart", with graphic and semantic explanation. | It defines a character and explains its form and meaning, matching dictionary or reference-entry content. |
| 252 | `keep_dictionary_entry` | 「丑」、「爪」金文同形。「丑」後假借為干支字，而本義廢。參「爪」。 | A reference-style note explaining the relation between the bronze forms of two characters and giving a cross-reference. | The main function is lexical and graphological definition, not extended scholarly argument. |
| 111 | `keep_scholarly_discussion` | 又清華一《楚居》簡12“秦溪之上”不能讀為“乾溪之上”，李守奎先生在6月底清華國際會議論文已經指出了。 | Scholarly discussion about how a manuscript phrase should or should not be read, citing another scholar's argument. | It reasons about interpretation and cites research context, so it is research-oriented prose. |
| 305 | `keep_scholarly_discussion` | 之前的戰國文字研究，對構形變化的討論成果最爲豐富，相關認識可以説已經非常透徹深入。 | A scholarly statement about prior research on Warring States script forms and structural change. | It summarizes research knowledge and disciplinary context, which is typical scholarly discussion. |
| 359 | `discard_noise_irrelevant` | 字体大小：放大 缩小 原始字体 | Web interface text for changing font size. | It is navigation or interface text rather than useful corpus content. |
| 354 | `discard_noise_irrelevant` | 本文发布日期为2024年6月29日 | A page publication-date line. | It is webpage metadata, not transcription, dictionary content, or scholarly discussion itself. |
