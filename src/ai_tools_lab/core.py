from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from string import Formatter
from typing import Any

WORD_RE = re.compile(r"[A-Za-z\u0600-\u06FF][A-Za-z0-9_\u0600-\u06FF'-]*")
SENTENCE_RE = re.compile(r"(?<=[.!?؟])\s+")

@dataclass(frozen=True)
class PromptTask:
    title: str
    prompt: str
    tags: tuple[str, ...] = ()

@dataclass(frozen=True)
class PromptAnalysis:
    characters: int
    words: int
    sentences: int
    unique_words: int
    estimated_tokens: int
    placeholders: tuple[str, ...]
    warnings: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["placeholders"] = list(self.placeholders)
        data["warnings"] = list(self.warnings)
        return data

def _require_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not text.strip():
        raise ValueError("text must not be empty")
    return text

def clean_prompt(text: str) -> str:
    """Normalize whitespace and excessive punctuation without changing wording."""
    text = _require_text(text)
    text = re.sub(r"[ \t]+", " ", text.strip())
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"([!?؟.,])\1{2,}", r"\1", text)
    return text

def extractive_summary(text: str, max_sentences: int = 2) -> str:
    """Return important original sentences; no model or network call is used."""
    cleaned = clean_prompt(text)
    if not 1 <= max_sentences <= 20:
        raise ValueError("max_sentences must be between 1 and 20")
    sentences = [s.strip() for s in SENTENCE_RE.split(cleaned) if s.strip()]
    if len(sentences) <= max_sentences:
        return " ".join(sentences)
    frequencies = Counter(w.lower() for w in WORD_RE.findall(cleaned) if len(w) > 2)
    scored = []
    for index, sentence in enumerate(sentences):
        words = WORD_RE.findall(sentence)
        score = sum(frequencies[w.lower()] for w in words) / max(len(words), 1)
        scored.append((score, index))
    selected = sorted(index for _, index in sorted(scored, reverse=True)[:max_sentences])
    return " ".join(sentences[i] for i in selected)

def analyze_prompt(text: str) -> PromptAnalysis:
    cleaned = clean_prompt(text)
    words = WORD_RE.findall(cleaned)
    sentences = [s for s in SENTENCE_RE.split(cleaned) if s.strip()]
    placeholders = tuple(dict.fromkeys(field for _, field, _, _ in Formatter().parse(cleaned) if field))
    warnings: list[str] = []
    if len(words) < 4:
        warnings.append("Prompt is very short; add context and expected output.")
    if len(words) > 1500:
        warnings.append("Prompt is long; consider separating context from instructions.")
    if not re.search(r"\b(output|format|return|write|list|json|table|summary)\b|(?:اكتب|صيغة|نتيجة|قائمة|جدول|ملخص)", cleaned, re.I):
        warnings.append("No obvious output-format cue was detected.")
    return PromptAnalysis(len(cleaned), len(words), max(1, len(sentences)), len({w.lower() for w in words}), max(1, round(len(cleaned) / 4)), placeholders, tuple(warnings))

def render_template(template: str, values: dict[str, str], *, strict: bool = True) -> str:
    _require_text(template)
    fields = tuple(dict.fromkeys(field for _, field, _, _ in Formatter().parse(template) if field))
    missing = [field for field in fields if field not in values]
    if strict and missing:
        raise ValueError(f"missing template values: {', '.join(missing)}")
    safe = {field: values.get(field, "{" + field + "}") for field in fields}
    return template.format_map(safe)

def load_tasks(path: Path) -> list[PromptTask]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"could not read task file: {exc}") from exc
    if not isinstance(data, list):
        raise ValueError("task file must contain a JSON array")
    tasks: list[PromptTask] = []
    for index, item in enumerate(data):
        if not isinstance(item, dict) or not isinstance(item.get("title"), str) or not isinstance(item.get("prompt"), str):
            raise ValueError(f"task {index} requires string title and prompt")
        tags = item.get("tags", [])
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            raise ValueError(f"task {index} tags must be a list of strings")
        tasks.append(PromptTask(item["title"].strip(), clean_prompt(item["prompt"]), tuple(tags)))
    return tasks
