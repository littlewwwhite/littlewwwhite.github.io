#!/usr/bin/env python3
"""
GPT-only blog image generator.

Usage:
    python3 generate.py --prompt "..." --out /path/to/post/dir
    python3 generate.py --prompt "..." --out /path/to/post/dir --filename 2.png --quality high
    python3 generate.py --provider openai --prompt "..." --out /path/to/post/dir

Env vars:
    CHATFIRE_API_KEY      ChatFire-hosted gpt-image-* endpoint
"""

import argparse
import io
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


CHATFIRE_BASE = "https://api.chatfire.cn/v1"


def get_next_filename(out_dir: Path) -> str:
    i = 1
    while (out_dir / f"{i}.png").exists():
        i += 1
    return f"{i}.png"


def build_request(payload: dict) -> urllib.request.Request:
    api_key = os.environ.get("CHATFIRE_API_KEY")
    if not api_key:
        print("ERROR: CHATFIRE_API_KEY not set in environment.", file=sys.stderr)
        sys.exit(1)

    return urllib.request.Request(
        f"{CHATFIRE_BASE}/images/generations",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )


def generate_openai(prompt: str, out_path: Path, model: str, size: str, quality: str) -> None:
    payload = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size,
    }
    if quality:
        payload["quality"] = quality

    print(f"[openai] model={model} size={size} quality={quality or 'default'}")
    body = None
    last_err = None
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(build_request(payload), timeout=300) as resp:
                body = json.loads(resp.read().decode())
            break
        except urllib.error.HTTPError as e:
            print(f"ERROR: HTTP {e.code}: {e.read().decode()[:500]}", file=sys.stderr)
            sys.exit(1)
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            last_err = e
            wait = 2 ** attempt
            print(
                f"[openai] attempt {attempt}/3 failed ({e.__class__.__name__}: {e}); retrying in {wait}s",
                file=sys.stderr,
            )
            time.sleep(wait)

    if body is None:
        print(f"ERROR: all retries failed. Last error: {last_err}", file=sys.stderr)
        sys.exit(1)

    items = body.get("data") or []
    if not items:
        print(f"ERROR: Empty data in response: {json.dumps(body)[:500]}", file=sys.stderr)
        sys.exit(1)

    first = items[0]
    if "b64_json" in first and first["b64_json"]:
        import base64

        img_bytes = base64.b64decode(first["b64_json"])
    elif "url" in first and first["url"]:
        with urllib.request.urlopen(first["url"], timeout=180) as r:
            img_bytes = r.read()
    else:
        print(f"ERROR: No image payload in response: {json.dumps(first)[:500]}", file=sys.stderr)
        sys.exit(1)

    try:
        from PIL import Image
    except ImportError:
        print("ERROR: pillow not installed. Run: pip install pillow", file=sys.stderr)
        sys.exit(1)

    img = Image.open(io.BytesIO(img_bytes))
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA")
    img.save(str(out_path), format="PNG")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate GPT blog images")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--out", required=True, help="Output directory (post Page Bundle dir)")
    parser.add_argument("--filename", default=None, help="Output filename (default: auto-increment N.png)")
    parser.add_argument(
        "--provider",
        default="openai",
        choices=["openai"],
        help="Backward-compatible no-op. Only openai/gpt-image-* is supported.",
    )
    parser.add_argument(
        "--model",
        default="gpt-image-2",
        help="gpt-image-2|gpt-image-1.5|gpt-image-1",
    )
    parser.add_argument("--size", default="1024x1024", help="1024x1024, 1792x1024, or 1024x1792")
    parser.add_argument("--quality", default="high", help="high|medium|low. Pass empty string to skip.")
    args = parser.parse_args()

    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = args.filename or get_next_filename(out_dir)
    out_path = out_dir / filename

    quality = args.quality if args.quality != "" else ""
    generate_openai(args.prompt, out_path, args.model, args.size, quality)

    print(f"\nSaved: {out_path}")
    print("\nMarkdown tag:")
    print(f"![diagram]({filename})")


if __name__ == "__main__":
    main()
