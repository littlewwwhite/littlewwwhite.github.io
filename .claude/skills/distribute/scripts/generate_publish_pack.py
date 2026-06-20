#!/usr/bin/env python3
# input: a Hugo post markdown file and an output directory
# output: local publishing pack files for long-form platforms and Xiaohongshu
# pos: deterministic pack generator behind the distribute skill

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


BLOG_BASE_URL = "https://littlewwwhite.github.io/posts"
AIBEIKE_URL = "chrome-extension://jejejajkcbhejfiocemmddgbkdlhhngm/options.html"


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text
    match = re.match(r"^---\n(.*?)\n---\n?", text, flags=re.DOTALL)
    if not match:
        return {}, text
    metadata: dict[str, object] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return metadata, text[match.end() :]


def frontmatter_date(metadata: dict[str, object]) -> str:
    value = metadata.get("date")
    return str(value or "")


def find_latest_post(project_root: Path) -> Path:
    candidates: list[tuple[str, str, Path]] = []
    for post in (project_root / "content" / "posts").glob("*/index.md"):
        metadata, _ = parse_frontmatter(post.read_text(encoding="utf-8"))
        candidates.append((frontmatter_date(metadata), post.parent.name, post))
    if not candidates:
        raise RuntimeError(f"No posts found under {project_root / 'content' / 'posts'}")
    candidates.sort(reverse=True)
    return candidates[0][2]


def infer_project_root(post: Path) -> Path:
    resolved = post.resolve()
    for parent in resolved.parents:
        if parent.name == "posts" and parent.parent.name == "content":
            return parent.parent.parent
    return Path.cwd().resolve()


def strip_hugo_shortcodes(text: str) -> str:
    text = re.sub(r"\{\{<.*?>\}\}", "", text, flags=re.DOTALL)
    text = re.sub(r"\{\{%.*?%\}\}", "", text, flags=re.DOTALL)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def extract_mermaid_blocks(text: str, out_dir: Path) -> str:
    assets_dir = out_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    count = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        source = match.group(1).strip() + "\n"
        path = assets_dir / f"mermaid-{count}.mmd"
        path.write_text(source, encoding="utf-8")
        return f"\n\n> Mermaid diagram source saved at `assets/{path.name}`.\n\n"

    return re.sub(r"```mermaid\n(.*?)```", replace, text, flags=re.DOTALL)


def rewrite_image_links(text: str, slug: str) -> str:
    def replace(match: re.Match[str]) -> str:
        alt = match.group(1)
        target = match.group(2)
        if re.match(r"^[a-z]+://", target) or target.startswith("#") or target.startswith("/"):
            return match.group(0)
        return f"![{alt}]({BLOG_BASE_URL}/{slug}/{target})"

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace, text)


def build_longform(post: Path, out_dir: Path) -> tuple[dict[str, object], str]:
    raw = post.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(raw)
    slug = post.parent.name
    body = strip_hugo_shortcodes(body)
    body = extract_mermaid_blocks(body, out_dir)
    body = rewrite_image_links(body, slug)
    title = str(metadata.get("title") or post.parent.name)
    source = f"{BLOG_BASE_URL}/{slug}/"
    longform = f"# {title}\n\n{body.rstrip()}\n\n---\n\n原文：{source}\n"
    return metadata, longform


def plain_paragraphs(markdown: str) -> list[str]:
    text = re.sub(r"```.*?```", "", markdown, flags=re.DOTALL)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def build_xhs(title: str, longform: str) -> str:
    paragraphs = [
        p for p in plain_paragraphs(longform)
        if not p.startswith("原文：") and p.strip() != title
    ]
    body = "\n\n".join(paragraphs[:4])
    if len(body) > 1300:
        body = body[:1297].rstrip() + "..."
    return (
        f"{title}\n\n"
        f"{body}\n\n"
        "#技术博客 #AI工程 #软件架构 #开发者"
    )


def build_manifest(
    post: Path,
    out_dir: Path,
    metadata: dict[str, object],
    title: str,
) -> dict[str, object]:
    slug = post.parent.name
    manifest = {
        "title": title,
        "slug": slug,
        "source": str(post),
        "blog_url": f"{BLOG_BASE_URL}/{slug}/",
        "aibeike_url": AIBEIKE_URL,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "artifacts": {
            "longform": "longform.md",
            "xiaohongshu": "xhs.md",
            "assets": "assets/",
            "cards": "cards/",
        },
        "platforms": {
            "x": {"source": "longform.md", "publisher": "aibeike", "content_type": "article_or_dynamic"},
            "wechat": {"source": "longform.md", "publisher": "aibeike", "content_type": "article"},
            "zhihu": {"source": "longform.md", "publisher": "aibeike", "content_type": "article"},
            "douyin": {"source": "longform.md", "publisher": "aibeike", "content_type": "imagetext"},
            "xiaohongshu": {"source": "xhs.md", "publisher": "aibeike", "content_type": "imagetext"},
        },
        "metadata": metadata,
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def generate(post: Path, out_dir: Path, project_root: Path | None = None) -> dict[str, object]:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "cards").mkdir(exist_ok=True)
    metadata, longform = build_longform(post, out_dir)
    title = str(metadata.get("title") or post.parent.name)
    (out_dir / "longform.md").write_text(longform, encoding="utf-8")
    (out_dir / "xhs.md").write_text(build_xhs(title, longform), encoding="utf-8")
    stale_preview = out_dir / "preview.html"
    if stale_preview.exists():
        stale_preview.unlink()
    return build_manifest(post, out_dir, metadata, title)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a local cross-platform publish pack.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--post", type=Path, help="Path to a Hugo post markdown file")
    source.add_argument("--latest", action="store_true", help="Use the latest post by frontmatter date")
    parser.add_argument("--project-root", type=Path, help="Project root for --latest and default output")
    parser.add_argument("--out", type=Path, help="Output directory, defaults to _dist/<slug>")
    args = parser.parse_args()
    try:
        if args.latest:
            project_root = (args.project_root or Path.cwd()).resolve()
            post = find_latest_post(project_root)
        else:
            post = args.post.resolve()
            project_root = (args.project_root.resolve() if args.project_root else infer_project_root(post))
        out_dir = args.out or project_root / "_dist" / post.parent.name
        manifest = generate(post, out_dir, project_root)
        print(json.dumps({"ok": True, "out": str(out_dir), "slug": manifest["slug"]}, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
