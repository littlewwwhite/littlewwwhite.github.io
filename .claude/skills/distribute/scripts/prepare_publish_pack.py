#!/usr/bin/env python3
# input: a Hugo project root and either --latest or --slug
# output: generated publish pack plus 爱贝壳 fill plan and URL
# pos: one-command entrypoint for 爱贝壳 handoff preparation

from __future__ import annotations

import argparse
import json
import sys
import webbrowser
from pathlib import Path

from build_aibeike_fill_plan import write_plan
from generate_publish_pack import AIBEIKE_URL, find_latest_post, generate


def resolve_post(project_root: Path, latest: bool, slug: str | None) -> Path:
    if latest:
        return find_latest_post(project_root)
    if not slug:
        raise RuntimeError("Provide --latest or --slug <slug>.")
    post = project_root / "content" / "posts" / slug / "index.md"
    if not post.exists():
        raise RuntimeError(f"Post not found: {post}")
    return post


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a publish pack, build a fill plan, and open 爱贝壳.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--latest", action="store_true", help="Use latest post by frontmatter date")
    source.add_argument("--slug", help="Use content/posts/<slug>/index.md")
    parser.add_argument("--project-root", type=Path, default=Path.cwd(), help="Hugo project root")
    parser.add_argument("--dry-run", action="store_true", help="Generate and print handoff details without opening browser")
    parser.add_argument("--no-browser", action="store_true", help="Generate handoff details without opening browser")
    args = parser.parse_args()

    try:
        project_root = args.project_root.resolve()
        post = resolve_post(project_root, args.latest, args.slug)
        out_dir = project_root / "_dist" / post.parent.name
        manifest = generate(post, out_dir, project_root)
        plan_path, _ = write_plan(out_dir / "manifest.json")
        if not args.dry_run and not args.no_browser:
            webbrowser.open(AIBEIKE_URL)
        print(json.dumps({
            "ok": True,
            "slug": manifest["slug"],
            "out": str(out_dir),
            "plan_path": str(plan_path),
            "aibeike_url": AIBEIKE_URL,
        }, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
