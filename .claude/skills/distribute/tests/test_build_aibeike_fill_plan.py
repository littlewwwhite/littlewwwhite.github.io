# input: unittest invokes the Aibeike fill-plan builder with generated publish packs
# output: verifies deterministic browser-fill instructions without final submit actions
# pos: regression tests for the distribute skill's Aibeike handoff contract

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
GENERATE_SCRIPT = ROOT / "skills" / "distribute" / "scripts" / "generate_publish_pack.py"
PLAN_SCRIPT = ROOT / "skills" / "distribute" / "scripts" / "build_aibeike_fill_plan.py"


class BuildAibeikeFillPlanTest(unittest.TestCase):
    def test_build_plan_from_manifest(self) -> None:
        import tempfile

        tmp = Path(tempfile.mkdtemp())
        post_dir = tmp / "content" / "posts" / "260522"
        post_dir.mkdir(parents=True)
        post = post_dir / "index.md"
        post.write_text(
            """---
title: "Memory Ledger Notes"
date: 2026-05-22
---

第一段总结：这篇文章解释为什么 memory ledger 值得保留。

第二段说明 X Premium、公众号、知乎可以复用长文。
""",
            encoding="utf-8",
        )
        out_dir = tmp / "_dist" / "260522"
        subprocess.run(
            [sys.executable, str(GENERATE_SCRIPT), "--post", str(post), "--out", str(out_dir), "--project-root", str(tmp)],
            check=True,
            text=True,
            capture_output=True,
        )

        result = subprocess.run(
            [sys.executable, str(PLAN_SCRIPT), "--manifest", str(out_dir / "manifest.json")],
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        plan_path = Path(payload["plan_path"])
        self.assertTrue(plan_path.exists())
        plan = json.loads(plan_path.read_text(encoding="utf-8"))

        self.assertFalse(plan["submit"])
        self.assertEqual(plan["title"], "Memory Ledger Notes")
        self.assertEqual(plan["surfaces"][0]["id"], "article_import")
        self.assertEqual(plan["surfaces"][0]["tab"], "文章")
        self.assertEqual(plan["surfaces"][0]["fields"]["article_url"]["value"], "https://littlewwwhite.github.io/posts/260522/")
        self.assertEqual(plan["surfaces"][0]["fields"]["title"]["value"], "Memory Ledger Notes")
        self.assertIn("第一段总结", plan["surfaces"][0]["fields"]["summary"]["value"])
        self.assertEqual(plan["surfaces"][0]["platforms"], ["微信公众号", "知乎专栏", "X(Premium)"])
        self.assertEqual(plan["surfaces"][1]["id"], "imagetext_seed")
        self.assertEqual(plan["surfaces"][1]["fields"]["body"]["source"], "xhs.md")
        self.assertIn("#技术博客", plan["surfaces"][1]["fields"]["body"]["value"])
        self.assertEqual(plan["surfaces"][1]["platforms"], ["小红书", "抖音(图文)"])

    def test_missing_artifact_is_reported(self) -> None:
        import tempfile

        tmp = Path(tempfile.mkdtemp())
        manifest = tmp / "manifest.json"
        manifest.write_text(
            json.dumps(
                {
                    "title": "Broken",
                    "slug": "260522",
                    "blog_url": "https://littlewwwhite.github.io/posts/260522/",
                    "aibeike_url": "chrome-extension://jejejajkcbhejfiocemmddgbkdlhhngm/options.html",
                    "artifacts": {"longform": "longform.md", "xiaohongshu": "xhs.md"},
                }
            ),
            encoding="utf-8",
        )

        result = subprocess.run(
            [sys.executable, str(PLAN_SCRIPT), "--manifest", str(manifest)],
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing publish artifact", result.stderr)


if __name__ == "__main__":
    unittest.main()
