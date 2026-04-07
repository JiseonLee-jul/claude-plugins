"""Verify structural integrity of the knowledge base wiki.

Input (stdin JSON):
    {"kb_root": "..."}

Output (stdout JSON):
    {"valid": true|false, "issues": [...], "stats": {...}}

Checks:
1. Every compiled raw file has a corresponding wiki/summaries/{name}.md
2. Every concept referenced in wiki/connections/ exists in wiki/concepts/
3. wiki/index.md lists all summaries and concepts (no orphans)
4. No broken internal links (][...] patterns with missing targets)
"""

import json
import re
import sys
from pathlib import Path

STATE_FILE = ".kb_state.json"


def load_state(kb_root: Path) -> dict:
    state_path = kb_root / STATE_FILE
    if state_path.exists():
        return json.loads(state_path.read_text(encoding="utf-8"))
    return {"compiled": {}}


def check_summaries(kb_root: Path, compiled: dict) -> list[str]:
    """Check every compiled raw file has a summary."""
    issues = []
    summaries_dir = kb_root / "wiki" / "summaries"
    for raw_name in compiled:
        stem = Path(raw_name).stem
        expected = summaries_dir / f"{stem}.md"
        if not expected.exists():
            issues.append(f"Missing summary for compiled source: {raw_name} (expected {expected.name})")
    return issues


def check_connections(kb_root: Path) -> list[str]:
    """Check every concept in connections/ exists in concepts/."""
    issues = []
    connections_dir = kb_root / "wiki" / "connections"
    concepts_dir = kb_root / "wiki" / "concepts"

    if not connections_dir.exists():
        return issues

    for conn_file in connections_dir.glob("*.md"):
        parts = conn_file.stem.split("--")
        for part in parts:
            concept_path = concepts_dir / f"{part}.md"
            if not concept_path.exists():
                issues.append(
                    f"Connection '{conn_file.name}' references non-existent concept: {part}.md"
                )
    return issues


def check_index(kb_root: Path) -> list[str]:
    """Check index.md references all summaries and concepts."""
    issues = []
    index_path = kb_root / "wiki" / "index.md"

    if not index_path.exists():
        return ["wiki/index.md does not exist"]

    index_content = index_path.read_text(encoding="utf-8")

    # Check summaries are listed
    summaries_dir = kb_root / "wiki" / "summaries"
    if summaries_dir.exists():
        for summary in summaries_dir.glob("*.md"):
            if summary.name not in index_content and summary.stem not in index_content:
                issues.append(f"Orphaned summary not in index: summaries/{summary.name}")

    # Check concepts are listed
    concepts_dir = kb_root / "wiki" / "concepts"
    if concepts_dir.exists():
        for concept in concepts_dir.glob("*.md"):
            if concept.name not in index_content and concept.stem not in index_content:
                issues.append(f"Orphaned concept not in index: concepts/{concept.name}")

    return issues


def check_broken_links(kb_root: Path) -> list[str]:
    """Check for broken internal markdown links."""
    issues = []
    wiki_dir = kb_root / "wiki"

    if not wiki_dir.exists():
        return issues

    link_pattern = re.compile(r"\]\(([^)]+)\)")

    for md_file in wiki_dir.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        for match in link_pattern.finditer(content):
            target = match.group(1)
            # Skip external URLs and anchors
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            # Resolve relative path
            target_path = (md_file.parent / target).resolve()
            if not target_path.exists():
                issues.append(
                    f"Broken link in {md_file.relative_to(wiki_dir)}: "
                    f"'{target}' -> file not found"
                )

    return issues


def gather_stats(kb_root: Path) -> dict:
    """Collect wiki statistics."""
    wiki_dir = kb_root / "wiki"
    stats = {
        "summaries": 0,
        "concepts": 0,
        "connections": 0,
        "index_lines": 0,
    }
    if (wiki_dir / "summaries").exists():
        stats["summaries"] = len(list((wiki_dir / "summaries").glob("*.md")))
    if (wiki_dir / "concepts").exists():
        stats["concepts"] = len(list((wiki_dir / "concepts").glob("*.md")))
    if (wiki_dir / "connections").exists():
        stats["connections"] = len(list((wiki_dir / "connections").glob("*.md")))
    if (wiki_dir / "index.md").exists():
        stats["index_lines"] = len((wiki_dir / "index.md").read_text(encoding="utf-8").splitlines())
    return stats


def main():
    data = json.loads(sys.stdin.read())
    kb_root = Path(data["kb_root"])

    state = load_state(kb_root)
    compiled = state.get("compiled", {})

    all_issues = []
    all_issues.extend(check_summaries(kb_root, compiled))
    all_issues.extend(check_connections(kb_root))
    all_issues.extend(check_index(kb_root))
    all_issues.extend(check_broken_links(kb_root))

    stats = gather_stats(kb_root)

    output = {
        "valid": len(all_issues) == 0,
        "issues": all_issues,
        "stats": stats,
    }
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
