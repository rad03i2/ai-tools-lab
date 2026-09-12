#!/usr/bin/env python3
"""Small local AI helper tools with no external API requirement."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PromptTask:
    title: str
    prompt: str
    tags: list[str]


def clean_prompt(text: str) -> str:
    """Normalize spaces and remove repeated punctuation noise."""
    text = re.sub(r"\s+", " ", text.strip())
    text = re.sub(r"([!?.,])\1{2,}", r"\1", text)
    return text


def extractive_summary(text: str, max_sentences: int = 2) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", clean_prompt(text))
    words = re.findall(r"[A-Za-z\u0600-\u06FF]{3,}", text.lower())
    scores = Counter(words)
    ranked = sorted(sentences, key=lambda s: sum(scores[w.lower()] for w in re.findall(r"[A-Za-z\u0600-\u06FF]{3,}", s)), reverse=True)
    return " ".join(ranked[:max_sentences])


def load_tasks(path: Path) -> list[PromptTask]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [PromptTask(**item) for item in data]


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python src/prompt_tools.py examples/tasks.json")
        raise SystemExit(1)

    for task in load_tasks(Path(sys.argv[1])):
        print(f"\n## {task.title}")
        print("Tags:", ", ".join(task.tags))
        print("Clean:", clean_prompt(task.prompt))
        print("Summary:", extractive_summary(task.prompt))


if __name__ == "__main__":
    main()
