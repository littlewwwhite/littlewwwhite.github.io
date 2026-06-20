# input: pytest invokes the publish-pack generator with a Hugo page bundle fixture
# output: verifies the generated cross-platform publishing artifacts without local preview files
# pos: regression tests for the distribute skill's local publishing pack contract

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills" / "distribute" / "scripts" / "generate_publish_pack.py"


class GeneratePublishPackTest(unittest.TestCase):
    def test_generate_pack_creates_longform_xhs_and_manifest(self) -> None:
        with self.subTest("generate pack"):
            import tempfile

            tmp = Path(tempfile.mkdtemp())
            post_dir = tmp / "content" / "posts" / "260522"
            post_dir.mkdir(parents=True)
            post = post_dir / "index.md"
            post.write_text(
                """---
title: "Memory Ledger Notes"
date: 2026-05-22
tags:
  - Agent
---

开头第一段说明为什么 memory ledger 值得写。

![Architecture](architecture.png)

{{< figure src="ignored.png" >}}

```mermaid
graph TD
  A --> B
```

第二段保留一个具体判断：长文平台应该复用 canonical artifact。

```python
print("keep code")
```
""",
                encoding="utf-8",
            )
            (post_dir / "architecture.png").write_bytes(b"fake")

            out_dir = tmp / "_dist" / "260522"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--post", str(post), "--out", str(out_dir)],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))
            longform = (out_dir / "longform.md").read_text(encoding="utf-8")
            xhs = (out_dir / "xhs.md").read_text(encoding="utf-8")

            self.assertEqual(manifest["slug"], "260522")
            self.assertEqual(manifest["title"], "Memory Ledger Notes")
            self.assertNotIn("preview_url", manifest)
            self.assertNotIn("preview", manifest["artifacts"])
            self.assertEqual(manifest["platforms"]["x"]["source"], "longform.md")
            self.assertEqual(manifest["platforms"]["xiaohongshu"]["source"], "xhs.md")
            self.assertFalse((out_dir / "preview.html").exists())
            self.assertNotIn("title:", longform)
            self.assertNotIn("{{<", longform)
            self.assertIn(
                "![Architecture](https://littlewwwhite.github.io/posts/260522/architecture.png)",
                longform,
            )
            self.assertNotIn("```mermaid", longform)
            self.assertIn("```python", longform)
            self.assertIn("Memory Ledger Notes", xhs)
            self.assertEqual(xhs.count("Memory Ledger Notes"), 1)
            self.assertIn("canonical artifact", xhs)

    def test_latest_mode_uses_frontmatter_date_and_default_output(self) -> None:
        import tempfile

        tmp = Path(tempfile.mkdtemp())
        older = tmp / "content" / "posts" / "260101"
        newer = tmp / "content" / "posts" / "260522"
        older.mkdir(parents=True)
        newer.mkdir(parents=True)
        (older / "index.md").write_text(
            "---\ntitle: \"Older\"\ndate: 2026-01-01\n---\n\nOld body.\n",
            encoding="utf-8",
        )
        (newer / "index.md").write_text(
            "---\ntitle: \"Newer\"\ndate: 2026-05-22\n---\n\nNew body.\n",
            encoding="utf-8",
        )

        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--latest", "--project-root", str(tmp)],
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["slug"], "260522")
        self.assertNotIn("preview_url", payload)
        out_dir = tmp / "_dist" / "260522"
        self.assertFalse((out_dir / "preview.html").exists())
        manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["title"], "Newer")
        self.assertNotIn("preview_url", manifest)
        self.assertEqual(manifest["aibeike_url"], "chrome-extension://jejejajkcbhejfiocemmddgbkdlhhngm/options.html")

    def test_latest_mode_requires_a_post(self) -> None:
        import tempfile

        tmp = Path(tempfile.mkdtemp())
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--latest", "--project-root", str(tmp)],
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No posts found", result.stderr)


if __name__ == "__main__":
    unittest.main()
