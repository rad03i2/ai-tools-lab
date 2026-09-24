from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from . import __version__
from .core import analyze_prompt, clean_prompt, extractive_summary, load_tasks, render_template

def _read(value: str | None) -> str:
    if value == "-" or value is None:
        return sys.stdin.read()
    return value

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ai-tools", description="Local deterministic prompt utilities")
    p.add_argument("--version", action="version", version=f"ai-tools-lab {__version__} — Radwan Abdulhadi Ahmed / @rad03i2")
    sub = p.add_subparsers(dest="command", required=True)
    clean = sub.add_parser("clean", help="normalize a prompt")
    clean.add_argument("text", nargs="?", default="-")
    summary = sub.add_parser("summarize", help="create an extractive summary")
    summary.add_argument("text", nargs="?", default="-")
    summary.add_argument("-n", "--sentences", type=int, default=2)
    inspect = sub.add_parser("inspect", help="measure a prompt and report warnings")
    inspect.add_argument("text", nargs="?", default="-")
    inspect.add_argument("--json", action="store_true")
    template = sub.add_parser("template", help="render {placeholders}")
    template.add_argument("text")
    template.add_argument("--value", action="append", default=[], metavar="KEY=VALUE")
    batch = sub.add_parser("batch", help="process a JSON task file")
    batch.add_argument("path", type=Path)
    batch.add_argument("--json", action="store_true")
    return p

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "clean":
            print(clean_prompt(_read(args.text)))
        elif args.command == "summarize":
            print(extractive_summary(_read(args.text), args.sentences))
        elif args.command == "inspect":
            result = analyze_prompt(_read(args.text))
            if args.json:
                print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
            else:
                print(f"Words: {result.words}\nEstimated tokens: {result.estimated_tokens}\nPlaceholders: {', '.join(result.placeholders) or '-'}")
                for warning in result.warnings: print(f"Warning: {warning}")
        elif args.command == "template":
            values: dict[str, str] = {}
            for pair in args.value:
                if "=" not in pair: raise ValueError("--value must use KEY=VALUE")
                key, value = pair.split("=", 1); values[key] = value
            print(render_template(args.text, values))
        elif args.command == "batch":
            rows = [{"title": t.title, "tags": list(t.tags), "clean": t.prompt, "summary": extractive_summary(t.prompt)} for t in load_tasks(args.path)]
            if args.json: print(json.dumps(rows, ensure_ascii=False, indent=2))
            else:
                for row in rows: print(f"\n## {row['title']}\nTags: {', '.join(row['tags'])}\nClean: {row['clean']}\nSummary: {row['summary']}")
        return 0
    except (ValueError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr); return 2

if __name__ == "__main__":
    raise SystemExit(main())
