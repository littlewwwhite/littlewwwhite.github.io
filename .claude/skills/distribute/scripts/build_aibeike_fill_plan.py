#!/usr/bin/env python3
# input: a generated publish-pack manifest or Hugo post selector
# output: a deterministic 爱贝壳 fill-plan JSON file that stops before final sync
# pos: browser-automation handoff contract for the distribute skill

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from generate_publish_pack import (
    AIBEIKE_URL,
    find_latest_post,
    generate,
    plain_paragraphs,
)


PLAN_NAME = "aibeike-fill-plan.json"


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_required(pack_dir: Path, relative_path: str) -> str:
    path = pack_dir / relative_path
    if not path.exists():
        raise RuntimeError(f"Missing publish artifact: {path}")
    return path.read_text(encoding="utf-8")


def summarize_longform(title: str, longform: str, limit: int = 180) -> str:
    for paragraph in plain_paragraphs(longform):
        cleaned = paragraph.strip()
        if not cleaned or cleaned == title or cleaned.startswith("原文："):
            continue
        if len(cleaned) <= limit:
            return cleaned
        return cleaned[: limit - 3].rstrip() + "..."
    return title


def media_files(pack_dir: Path) -> list[str]:
    cards_dir = pack_dir / "cards"
    if not cards_dir.exists():
        return []
    allowed = {".jpg", ".jpeg", ".png", ".webp"}
    return [
        str(path.relative_to(pack_dir))
        for path in sorted(cards_dir.iterdir())
        if path.is_file() and path.suffix.lower() in allowed
    ]


def artifact_path(manifest: dict[str, object], key: str, fallback: str) -> str:
    artifacts = manifest.get("artifacts")
    if isinstance(artifacts, dict):
        value = artifacts.get(key)
        if isinstance(value, str):
            return value
    return fallback


def build_plan(manifest_path: Path) -> dict[str, object]:
    manifest = read_json(manifest_path)
    pack_dir = manifest_path.parent
    title = str(manifest.get("title") or manifest.get("slug") or "")
    slug = str(manifest.get("slug") or pack_dir.name)
    blog_url = str(manifest.get("blog_url") or "")
    aibeike_url = str(manifest.get("aibeike_url") or AIBEIKE_URL)

    longform_name = artifact_path(manifest, "longform", "longform.md")
    xhs_name = artifact_path(manifest, "xiaohongshu", "xhs.md")
    longform = read_required(pack_dir, longform_name)
    xhs = read_required(pack_dir, xhs_name)
    summary = summarize_longform(title, longform)

    plan: dict[str, object] = {
        "title": title,
        "slug": slug,
        "source_manifest": str(manifest_path),
        "aibeike_url": aibeike_url,
        "submit": False,
        "surfaces": [
            {
                "id": "article_import",
                "tab": "文章",
                "intent": "Import the canonical blog article and sync it to long-form platforms.",
                "fields": {
                    "article_url": {
                        "placeholder_contains": "文章链接",
                        "value": blog_url,
                    },
                    "title": {
                        "placeholder": "标题",
                        "value": title,
                    },
                    "summary": {
                        "placeholder": "摘要(选填)",
                        "value": summary,
                    },
                },
                "source": longform_name,
                "content_chars": len(longform),
                "platforms": ["微信公众号", "知乎专栏", "X(Premium)"],
                "stop_before": "开始同步",
            },
            {
                "id": "imagetext_seed",
                "tab": "动态",
                "intent": "Use the Xiaohongshu seed as the short-form image-text draft.",
                "fields": {
                    "body": {
                        "placeholder": "分享新鲜事...",
                        "source": xhs_name,
                        "value": xhs,
                    }
                },
                "media": {
                    "source_dir": "cards",
                    "files": media_files(pack_dir),
                    "required_for": ["小红书", "抖音(图文)"],
                },
                "content_chars": len(xhs),
                "platforms": ["小红书", "抖音(图文)"],
                "stop_before": "开始同步",
            },
        ],
    }
    return plan


def write_plan(manifest_path: Path) -> tuple[Path, dict[str, object]]:
    plan = build_plan(manifest_path)
    plan_path = manifest_path.parent / PLAN_NAME
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    return plan_path, plan


def resolve_post(project_root: Path, latest: bool, slug: str | None) -> Path:
    if latest:
        return find_latest_post(project_root)
    if not slug:
        raise RuntimeError("Provide --manifest, --latest, or --slug <slug>.")
    post = project_root / "content" / "posts" / slug / "index.md"
    if not post.exists():
        raise RuntimeError(f"Post not found: {post}")
    return post


def resolve_manifest(args: argparse.Namespace) -> Path:
    if args.manifest:
        return args.manifest.resolve()
    project_root = args.project_root.resolve()
    post = resolve_post(project_root, args.latest, args.slug)
    out_dir = project_root / "_dist" / post.parent.name
    manifest = generate(post, out_dir, project_root)
    return out_dir / "manifest.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build an 爱贝壳 browser-fill plan from a publish pack.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--manifest", type=Path, help="Path to _dist/<slug>/manifest.json")
    source.add_argument("--latest", action="store_true", help="Generate a plan for the latest post")
    source.add_argument("--slug", help="Generate a plan for content/posts/<slug>/index.md")
    parser.add_argument("--project-root", type=Path, default=Path.cwd(), help="Hugo project root")
    args = parser.parse_args()

    try:
        manifest_path = resolve_manifest(args)
        plan_path, plan = write_plan(manifest_path)
        print(
            json.dumps(
                {
                    "ok": True,
                    "slug": plan["slug"],
                    "plan_path": str(plan_path),
                    "surfaces": [surface["id"] for surface in plan["surfaces"]],  # type: ignore[index]
                    "submit": plan["submit"],
                },
                ensure_ascii=False,
            )
        )
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
