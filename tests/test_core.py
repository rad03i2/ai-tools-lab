from pathlib import Path
import json
import pytest
from ai_tools_lab.core import analyze_prompt, clean_prompt, extractive_summary, load_tasks, render_template

def test_clean_prompt_preserves_unicode_and_normalizes():
    assert clean_prompt("  مرحبا   بالعالم!!!  ") == "مرحبا بالعالم!"

def test_empty_rejected():
    with pytest.raises(ValueError): clean_prompt("   ")

def test_summary_is_extractive_and_ordered():
    text = "Cats sleep often. Cats are agile animals. Water freezes at zero degrees."
    out = extractive_summary(text, 2)
    assert out in text or all(sentence in text for sentence in out.split(". "))
    assert len(out) < len(text)

def test_summary_limit_validation():
    with pytest.raises(ValueError): extractive_summary("One sentence.", 0)

def test_analysis_detects_placeholders():
    result = analyze_prompt("Write a JSON summary for {topic} with {count} items.")
    assert result.placeholders == ("topic", "count")
    assert result.words > 0
    assert result.estimated_tokens > 0

def test_template_strict_and_non_strict():
    assert render_template("Hello {name}", {"name": "Radwan"}) == "Hello Radwan"
    with pytest.raises(ValueError): render_template("{a} {b}", {"a": "x"})
    assert render_template("{a} {b}", {"a": "x"}, strict=False) == "x {b}"

def test_load_tasks_validates_schema(tmp_path: Path):
    path = tmp_path / "tasks.json"
    path.write_text(json.dumps([{"title":"عربي", "prompt":"اكتب ملخصا واضحا.", "tags":["ar"]}], ensure_ascii=False), encoding="utf-8")
    tasks = load_tasks(path)
    assert tasks[0].title == "عربي"
    bad = tmp_path / "bad.json"; bad.write_text('{"title":"x"}', encoding="utf-8")
    with pytest.raises(ValueError): load_tasks(bad)
