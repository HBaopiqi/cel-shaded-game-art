#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Build the installable ZIP and the single-document edition from the same skill."""
import json
import re
from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from validate_package import (
    MARKDOWN_LINK, PACKAGE_FILES, REFERENCE_FILES, REPO_ROOT, SKILL_NAME, SKILL_ROOT, validate,
)


def build_zip(output):
    with ZipFile(output, "w") as archive:
        for name in sorted(PACKAGE_FILES):
            entry = ZipInfo(f"{SKILL_NAME}/{name}")  # Fixed timestamp for repeatable builds.
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            data = (SKILL_ROOT / name).read_text(encoding="utf-8").encode("utf-8")
            archive.writestr(entry, data, compress_type=ZIP_DEFLATED)


def portable_markdown():
    reference_dir = SKILL_ROOT / "references"
    chapters = [reference_dir / name for name in (*REFERENCE_FILES[1:], REFERENCE_FILES[0])]
    source_map = reference_dir / "source-map.json"
    anchors = {path: f"ref-{path.stem}" for path in [*chapters, source_map]}
    chapter_titles = {}
    blocks = []

    for path in [SKILL_ROOT / "SKILL.md", *chapters]:
        content = path.read_text(encoding="utf-8")
        if path in anchors:
            chapter_titles[path.name] = content.splitlines()[0].removeprefix("# ")
            blocks.append(f'<a id="{anchors[path]}"></a>')
            content = re.sub(r"^(#{1,5})(?= )", r"#\1", content, flags=re.MULTILINE)
        else:
            content = re.sub(r"\A---\n.*?\n---\n+", "", content, count=1, flags=re.DOTALL)

        def link_to_section(match):
            label, target = match.groups()
            if target.startswith(("https://", "http://", "#")):
                return match[0]
            # Every relative reference must remain usable with the network disconnected.
            anchor = anchors[(path.parent / target).resolve()]
            return f"[{label}](#{anchor})"

        blocks.append(MARKDOWN_LINK.sub(link_to_section, content).strip())

    blocks.extend([f'<a id="{anchors[source_map]}"></a>', "## 逐段页码索引"])
    data = json.loads(source_map.read_text(encoding="utf-8"))
    for source in data["sources"]:
        blocks.append(f"### {source['id']} · {Path(source['title']).stem}")
        rows = ["| 中文版页序 | 内容 | 对应笔记 |", "| --- | --- | --- |"]
        for section in source["sections"]:
            start, end = section["start"], section["end"]
            pages = str(start) if start == end else f"{start}–{end}"
            links = [f"[{chapter_titles[name]}](#{anchors[reference_dir / name]})"
                     for name in section["references"]]
            rows.append(f"| {pages} | {section['topic']} | {' · '.join(links) or '背景'} |")
        blocks.append("\n".join(rows))
    return "\n\n".join(blocks) + "\n"


def main():
    errors = validate(SKILL_ROOT, for_release=True)
    if errors:
        raise SystemExit("\n".join(errors))
    output = REPO_ROOT / "dist"
    output.mkdir(exist_ok=True)
    zip_buffer = BytesIO()
    build_zip(zip_buffer)
    documents = {".zip": zip_buffer.getvalue(), ".md": portable_markdown().encode("utf-8")}
    for suffix, content in documents.items():
        destination = output / (SKILL_NAME + suffix)
        pending = NamedTemporaryFile(dir=output, delete=False)
        try:
            with pending:
                pending.write(content)
            Path(pending.name).replace(destination)
        finally:
            Path(pending.name).unlink(missing_ok=True)
        print(f"Built dist/{destination.name}")


if __name__ == "__main__":
    main()
