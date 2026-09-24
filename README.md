# AI Tools Lab

A small, production-minded Python toolkit for preparing and inspecting prompts **locally and deterministically**. It does not call an AI provider: it cleans prompt text, produces extractive summaries, reports prompt statistics and placeholders, renders templates, and processes JSON task batches.

## Why this project exists
Prompt preparation often needs repeatable utilities before text is sent to a model. AI Tools Lab provides those utilities without API keys, network access, telemetry, or model-dependent output.

## Features
- Unicode-aware prompt cleaning for English and Arabic.
- Extractive summarization that only returns sentences from the supplied text.
- Prompt inspection: characters, words, sentence count, vocabulary size, rough token estimate, placeholders, and actionable warnings.
- Strict `{placeholder}` template rendering.
- Validated JSON batch processing.
- CLI and Python API; zero runtime dependencies.
- Predictable exit code `2` for invalid input.

## Preview
```text
$ ai-tools inspect "Write a JSON summary for {topic}." --json
{
  "words": 6,
  "placeholders": ["topic"],
  ...
}
```
The token value is an estimate based on character count, not a tokenizer result.

## Requirements & installation
Python 3.10+.

```bash
git clone https://github.com/rad03i2/ai-tools-lab.git
cd ai-tools-lab
python -m pip install -e .
```

For development: `python -m pip install -e . pytest`.

## Usage
```bash
ai-tools clean "  Write   a summary!!!  "
ai-tools summarize "Sentence one. Sentence two. Sentence three." -n 2
ai-tools inspect "Write JSON for {topic}." --json
ai-tools template "Explain {topic} in {language}" --value topic=water --value language=Arabic
ai-tools batch examples/tasks.json --json
cat prompt.txt | ai-tools inspect - --json
```

Python API:
```python
from ai_tools_lab import analyze_prompt, clean_prompt, extractive_summary

prompt = clean_prompt("  اكتب   ملخصاً واضحاً.  ")
print(analyze_prompt(prompt).to_dict())
print(extractive_summary(prompt, 1))
```

## Configuration
There are no environment variables, secrets, remote services, or configuration files. Behavior is controlled through function arguments and CLI flags.

## JSON task format
```json
[{"title":"Release notes", "prompt":"Summarize the changes clearly.", "tags":["docs"]}]
```
`title` and `prompt` must be strings; `tags` must be an array of strings.

## Project structure
```text
src/ai_tools_lab/   package, core logic and CLI
tests/              functional/unit tests
examples/            safe sample task data
web/                 standalone browser prompt playground
.github/workflows/   cross-platform CI
```

## Testing
```bash
python -m compileall -q src tests
pytest
```
CI runs on Ubuntu, Windows, and macOS with Python 3.10, 3.12, and 3.13.

## Security & privacy
All Python toolkit processing is local. Inputs are not uploaded or logged by the package. Treat prompts as potentially sensitive and review them before copying them into third-party AI services. The browser playground stores no data remotely. See [SECURITY.md](SECURITY.md).

## Limitations
- The summarizer is frequency-based and extractive; it does not understand meaning like an LLM.
- Token counts are rough estimates and must not be used for provider billing or hard context limits.
- Sentence splitting is intentionally lightweight and can be imperfect around abbreviations.
- Template syntax follows Python `str.format` conventions; untrusted templates should not be treated as executable code, but malformed braces are rejected by Python's formatter.
- This project does not send prompts to or evaluate responses from AI models.

## Optional roadmap
Optional future work may include pluggable tokenizer adapters and configurable stop-word sets while keeping the default offline path dependency-free.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Keep changes deterministic, tested, bilingual where user-facing documentation changes, and free of required cloud credentials.

## License
MIT — see [LICENSE](LICENSE).

## Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

# مختبر أدوات الذكاء الاصطناعي — العربية

حزمة Python صغيرة وعملية لتجهيز وفحص الموجّهات **محلياً وبنتائج حتمية**. لا تتصل بأي مزود ذكاء اصطناعي؛ بل تنظف النص، وتنتج ملخصاً استخراجياً، وتحلل بنية الموجّه، وتتعامل مع القوالب والمهام بصيغة JSON.

## لماذا يوجد المشروع؟
تحتاج الموجّهات غالباً إلى تنظيف وفحص متكرر قبل إرسالها إلى أي نموذج. يوفر المشروع هذه الأدوات من دون مفاتيح API أو اتصال شبكي أو تتبع استخدام، لذلك يمكن استخدامه كمرحلة تجهيز محلية قابلة للاختبار.

## المزايا
- تنظيف النص العربي والإنجليزي مع دعم Unicode.
- تلخيص استخراجي يعيد جملاً موجودة أصلاً في النص.
- إحصاءات للأحرف والكلمات والجمل والمفردات وتقدير تقريبي للرموز واكتشاف المتغيرات والتحذيرات.
- قوالب صارمة بصيغة `{name}`.
- معالجة ملفات مهام JSON بعد التحقق من بنيتها.
- واجهة أوامر وواجهة Python، ومن دون اعتماديات تشغيل خارجية.

## معاينة
```bash
ai-tools inspect "اكتب ملخصاً بصيغة JSON عن {topic}." --json
```
قيمة الرموز المعروضة **تقدير** وليست نتيجة tokenizer خاص بمزود معين.

## المتطلبات والتثبيت
يتطلب Python 3.10 أو أحدث:
```bash
git clone https://github.com/rad03i2/ai-tools-lab.git
cd ai-tools-lab
python -m pip install -e .
```
للتطوير: `python -m pip install -e . pytest`.

## الاستخدام
```bash
ai-tools clean "  اكتب   ملخصاً!!!  "
ai-tools summarize "الجملة الأولى. الجملة الثانية. الجملة الثالثة." -n 2
ai-tools template "اشرح {topic}" --value topic=الماء
ai-tools batch examples/tasks.json --json
```
ويمكن استيراد `clean_prompt` و`extractive_summary` و`analyze_prompt` مباشرة من `ai_tools_lab`.

## الإعداد
لا توجد متغيرات بيئة أو أسرار أو خدمات خارجية مطلوبة. جميع الخيارات تمر عبر معاملات الدوال أو خيارات سطر الأوامر.

## بنية المشروع
`src/ai_tools_lab` للكود، و`tests` للاختبارات، و`examples` للأمثلة، و`web` للواجهة التجريبية المحلية، و`.github/workflows` للتكامل المستمر.

## الاختبارات
```bash
python -m compileall -q src tests
pytest
```
تختبر CI المشروع على Ubuntu وWindows وmacOS وإصدارات Python 3.10 و3.12 و3.13.

## الأمان والخصوصية
المعالجة محلية ولا ترفع المدخلات أو تسجلها عن بعد. يجب التعامل مع الموجّهات كبيانات قد تكون حساسة ومراجعتها قبل نسخها إلى خدمات ذكاء اصطناعي خارجية. راجع [SECURITY.md](SECURITY.md).

## القيود
الملخص استخراجي قائم على تكرار الكلمات وليس فهماً دلالياً، وعدد الرموز تقديري فقط، وتقسيم الجمل خفيف وقد لا يغطي كل الاختصارات، ولا يرسل المشروع الموجّهات إلى نماذج ذكاء اصطناعي ولا يقيم إجاباتها.

## التطوير الاختياري
يمكن مستقبلاً إضافة محولات tokenizer اختيارية وقوائم كلمات توقف قابلة للتخصيص مع إبقاء المسار الافتراضي محلياً وخالياً من الاعتماديات.

## المساهمة
راجع [CONTRIBUTING.md](CONTRIBUTING.md). يجب أن تكون التغييرات قابلة للاختبار، حتمية، وآمنة ولا تتطلب بيانات سرية.

## الترخيص
MIT — راجع [LICENSE](LICENSE).

## المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
