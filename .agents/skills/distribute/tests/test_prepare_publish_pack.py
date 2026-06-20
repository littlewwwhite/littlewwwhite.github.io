# input: unittest invokes the publish-pack preparer in dry-run mode
# output: verifies one-command pack and fill-plan generation without local preview server
# pos: regression tests for the 爱贝壳 handoff preparation entrypoint

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills" / "distribute" / "scripts" / "prepare_publish_pack.py"


class PreparePublishPackTest(unittest.TestCase):
    def test_dry_run_latest_generates_pack_and_plan_without_preview_server(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        post_dir = tmp / "content" / "posts" / "260522"
        post_dir.mkdir(parents=True)
        (post_dir / "index.md").write_text(
            "---\ntitle: \"Latest\"\ndate: 2026-05-22\n---\n\nBody.\n",
            encoding="utf-8",
        )

        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--latest",
                "--project-root",
                str(tmp),
                "--dry-run",
            ],
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["slug"], "260522")
        self.assertNotIn("preview_url", payload)
        self.assertNotIn("server", payload)
        self.assertEqual(payload["aibeike_url"], "chrome-extension://jejejajkcbhejfiocemmddgbkdlhhngm/options.html")
        self.assertFalse((tmp / "_dist" / "260522" / "preview.html").exists())
        self.assertTrue((tmp / "_dist" / "260522" / "aibeike-fill-plan.json").exists())
        self.assertEqual(payload["plan_path"], str((tmp / "_dist" / "260522" / "aibeike-fill-plan.json").resolve()))


if __name__ == "__main__":
    unittest.main()
