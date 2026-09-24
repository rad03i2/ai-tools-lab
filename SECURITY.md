# Security / الأمان

AI Tools Lab is an offline text-processing utility. It does not require credentials and should never need real API keys in tests, examples, or issues.

## Reporting
Please report security concerns privately through GitHub's available security reporting mechanism rather than publishing sensitive exploit details in a public issue.

## Scope and safe use
- The package does not transmit prompt content.
- JSON task files are treated as untrusted input and validated before conversion.
- Template rendering uses Python format syntax and is intended for local text preparation, not execution.
- Avoid putting secrets or personal information in prompts, screenshots, logs, or bug reports.
- If you later pass generated text to a third-party model, that provider's privacy and security terms apply.

## العربية
المشروع يعالج النص محلياً ولا يحتاج مفاتيح وصول. لا تضع أسراراً أو بيانات شخصية في الأمثلة أو البلاغات العامة. أبلغ عن الثغرات عبر قناة GitHub الأمنية الخاصة المتاحة للمستودع، وراجع سياسة أي مزود خارجي قبل إرسال النص إليه.
