"""Validate the saved repository snapshot without executing analysis or using network."""
import argparse
import ast
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
COLLECTION = ROOT / "data_collection_2026-10-12"


def markdown_anchors(text):
    """GitHub-style heading IDs for the ordinary headings used in this README."""
    anchors, seen = set(), {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.MULTILINE):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        index = seen.get(slug, 0)
        anchors.add(slug if not index else f"{slug}-{index}")
        seen[slug] = index + 1
    return anchors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional JSON report destination")
    args = parser.parse_args()
    failures, checks = [], {}

    def require(condition, message):
        if not condition:
            failures.append(message)

    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8-sig")
    require(text.startswith("# PAL Allocation and Student Data"), "README title missing")
    links = re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text)
    checked_links = 0
    for destination in links:
        destination = destination.strip().strip("<>")
        parsed = urlsplit(destination)
        if parsed.scheme or parsed.netloc:
            continue
        checked_links += 1
        target = (ROOT / unquote(parsed.path)).resolve() if parsed.path else readme
        require(target.is_relative_to(ROOT), f"README link escapes repository: {destination}")
        require(target.exists(), f"README link missing: {destination}")
        if parsed.fragment and target.exists():
            require(target.suffix.lower() == ".md", f"Unsupported fragment target: {destination}")
            if target.suffix.lower() == ".md":
                require(unquote(parsed.fragment) in markdown_anchors(target.read_text(encoding="utf-8-sig")),
                        f"README heading anchor missing: {destination}")
    checks["readme_relative_links_and_anchors"] = checked_links

    inventory = COLLECTION / "analysis/cleaned_file_inventory.csv"
    with inventory.open(encoding="utf-8-sig", newline="") as handle:
        entries = list(csv.DictReader(handle))
    names = [entry["file"] for entry in entries]
    require(len(entries) == 29 and len(set(names)) == 29, "Inventory must contain 29 unique CSVs")
    clean = COLLECTION / "analysis/cleaned"
    require(set(names) == {path.name for path in clean.glob("*.csv")}, "Cleaned CSV inventory/file mismatch")
    for entry in entries:
        path = clean / entry["file"]
        if not path.exists():
            failures.append(f"Missing cleaned CSV: {path.name}")
            continue
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader)
            rows = 0
            for number, row in enumerate(reader, 2):
                rows += 1
                require(len(row) == len(header), f"Ragged CSV: {path.name}:{number}")
        require(rows == int(entry["rows"]), f"Row count mismatch: {path.name}")
        require(len(header) == int(entry["columns"]), f"Column count mismatch: {path.name}")
    checks["cleaned_csvs"] = len(entries)

    notebooks = {}
    for name, expected in [("alberta_ircc_preliminary_analysis.ipynb", 9),
                           ("pal_allocation_admissions_and_timeline.ipynb", 6)]:
        notebook = json.loads((COLLECTION / "analysis" / name).read_text(encoding="utf-8-sig"))
        cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
        executed = sum(isinstance(cell.get("execution_count"), int) for cell in cells)
        errors = sum(output.get("output_type") == "error" for cell in cells for output in cell.get("outputs", []))
        require(len(cells) == expected and executed == expected, f"Notebook executed-cell count: {name}")
        require(errors == 0, f"Notebook contains error outputs: {name}")
        notebooks[name] = {"code_cells": len(cells), "executed": executed, "error_outputs": errors}
    checks["saved_notebooks"] = notebooks

    hashes = json.loads((COLLECTION / "research/readme_review/evidence_hashes_before.json").read_text(encoding="utf-8-sig"))
    for name, expected in hashes.items():
        path = COLLECTION / name
        require(path.exists(), f"Missing sampled evidence: {name}")
        if path.exists():
            require(hashlib.sha256(path.read_bytes()).hexdigest() == expected, f"Evidence checksum changed: {name}")
    checks["sampled_evidence_hashes"] = len(hashes)

    scripts = sorted(set((ROOT / "scripts").glob("*.py")) | set((COLLECTION / "scripts").glob("*.py")))
    for path in scripts:
        try:
            ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        except (SyntaxError, UnicodeError) as exc:
            failures.append(f"Python syntax: {path.relative_to(ROOT)}: {exc}")
    checks["python_scripts_parsed_without_execution"] = len(scripts)

    result = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True)
    tracked = [item for item in result.stdout.decode("utf-8").split("\0") if item]
    require(bool(tracked), "Git index is empty; stage files or validate a clone")
    forbidden = {"__pycache__", ".ipynb_checkpoints", "_dependencies", "_kernels", ".venv", "venv", ".pytest_cache"}
    largest = 0
    for name in tracked:
        path = ROOT / name
        require(not (set(path.relative_to(ROOT).parts) & forbidden), f"Runtime/cache directory tracked: {name}")
        require(path.suffix.lower() not in {".pyc", ".pyo"}, f"Python cache tracked: {name}")
        require(path.is_file(), f"Tracked file missing in worktree: {name}")
        if path.is_file():
            size = path.stat().st_size
            largest = max(largest, size)
            require(size <= 100 * 1024 * 1024, f"Tracked file exceeds GitHub 100 MiB limit: {name}")
    checks["git_tracked_files"] = len(tracked)
    checks["largest_tracked_file_bytes"] = largest
    report = {"passed": not failures, "checks": checks, "failures": failures,
              "scope": "Saved outputs, local links, selected hashes and syntax; no network requests or fresh analysis execution."}
    payload = json.dumps(report, indent=2)
    print(payload)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
