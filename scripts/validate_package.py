#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Validate the portable skill, local document links and source-page mapping."""
import argparse
import json
import re
from pathlib import Path


EXPECTED = {"M": 90, "S": 45, "B": 60, "R": 56, "O": 79}
SKILL_NAME = "cel-shaded-game-art"
REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / SKILL_NAME
REFERENCE_FILES = (
    "00-sources.md",
    "01-modeling-face.md",
    "02-normals.md",
    "03-topology-skinning.md",
    "04-bone-placement.md",
    "05-rigging.md",
    "06-outline-engineering.md",
    "07-outline-art.md",
    "08-validation-handoff.md",
)
PACKAGE_FILES = (
    "SKILL.md", "agents/openai.yaml", "references/source-map.json",
    *(f"references/{name}" for name in REFERENCE_FILES),
)
MARKDOWN_LINK = re.compile(r"\[([^\]\n]*)\]\(([^)\s]+)\)")
PRIVATE_PATTERNS = (
    r"/(?:workspace|Users|home)/", r"\b[A-Za-z]:[\\/]", r"libfile_[A-Za-z0-9]+",
    r"https?://drive\.google\.com/", r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
)


def check_links(path, text, boundary):
    errors = []
    for _, link in MARKDOWN_LINK.findall(text):
        target = link.split("#", 1)[0]
        if not target or re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", target):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.is_relative_to(boundary) or not resolved.is_file():
            errors.append(f"Broken or escaping link in {path.name}: {link}")
    return errors


def validate(root, *, for_release=False):
    root = Path(root).resolve()
    errors = []
    contents = {}
    for required in PACKAGE_FILES:
        if not (root / required).is_file():
            errors.append(f"Missing required file: {required}")
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            errors.append(f"Linked path in package: {relative}")
            continue
        if not path.is_file():
            continue
        if relative.as_posix() not in PACKAGE_FILES:
            errors.append(f"Unexpected file in installable skill: {relative}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"Cannot read UTF-8 file {relative}: {exc}")
            continue
        contents[relative.as_posix()] = text
        scan_text = text
        if relative.as_posix() == "SKILL.md" and not for_release:
            # gh skill install --from-local adds the source path to the installed copy.
            scan_text = re.sub(r"^ +local-path:[^\n]*$", "", text, flags=re.MULTILINE)
        if any(re.search(pattern, scan_text) for pattern in PRIVATE_PATTERNS):
            errors.append(f"Potential private identifier/path: {relative}")
        if path.suffix == ".md":
            errors.extend(check_links(path, text, root))
    if "SKILL.md" in contents:
        text = contents["SKILL.md"]
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not match:
            errors.append("SKILL.md lacks YAML frontmatter")
        else:
            front = match.group(1)
            if not re.search(rf"^name: {SKILL_NAME}$", front, re.M) or root.name != SKILL_NAME:
                errors.append(f"Skill name and directory must both be {SKILL_NAME}")
            if not re.search(r"^description: .+", front, re.M):
                errors.append("Missing description")
            if not re.search(r"^license: CC-BY-4.0$", front, re.M):
                errors.append("Missing content license")
            if for_release and re.search(r"^ +(?:local-path|github-[\w-]+):", front, re.M):
                errors.append("Remove installer tracking metadata from the release source")
    if "references/source-map.json" in contents:
        try:
            data = json.loads(contents["references/source-map.json"])
            sources = data["sources"]
            ids = [source["id"] for source in sources]
            if len(ids) != len(set(ids)) or set(ids) != set(EXPECTED):
                errors.append("Source IDs must be M, S, B, R, O, exactly once")
            total = 0
            for source in sources:
                code, count = source["id"], source["page_count"]
                if type(count) is not int or count != EXPECTED.get(code):
                    errors.append(f"Unexpected page count: {code}")
                    continue
                total += count
                covered = []
                for section in source["sections"]:
                    a, b = section["start"], section["end"]
                    if type(a) is not int or type(b) is not int or not 1 <= a <= b <= count:
                        errors.append(f"Invalid page range: {code}")
                        continue
                    covered.extend(range(a, b + 1))
                    if section["kind"] not in {"technical", "context"}:
                        errors.append(f"Unknown section kind: {code} {a}-{b}")
                    if section["kind"] == "technical" and not section["references"]:
                        errors.append(f"Technical section has no reference: {code} {a}-{b}")
                    for ref in section["references"]:
                        resolved = (root / "references" / ref).resolve()
                        if ref not in REFERENCE_FILES or not resolved.is_file():
                            errors.append(f"Missing or escaping source-map reference: {ref}")
                if sorted(covered) != list(range(1, count + 1)):
                    errors.append(f"Pages missing or overlapping: {code}")
            if total != 330 or data["total_pages"] != total:
                errors.append("Total page coverage must equal 330")
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            errors.append(f"Invalid source map: {exc}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=REPO_ROOT,
                        help="Repository root or installed skill directory")
    args = parser.parse_args()
    root = args.root.resolve()
    if (root / "skills" / SKILL_NAME).is_dir():
        errors = validate(root / "skills" / SKILL_NAME, for_release=True)
        for name in ("README.md", "LICENSE", "scripts/LICENSE"):
            if not (root / name).is_file():
                errors.append(f"Missing repository file: {name}")
        readme = root / "README.md"
        if readme.is_file():
            errors.extend(check_links(readme, readme.read_text(encoding="utf-8"), root))
    else:
        errors = validate(root)
    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1
    print("PASS: skill layout, local links, content license, privacy patterns and 330 mapped pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
