#!/usr/bin/env python3
"""
Blog image generator using Gemini Nano Banana (native image generation).

Usage:
    python3 generate.py --prompt "diagram description" --out /path/to/post/dir
    python3 generate.py --prompt "..." --out /path/to/post/dir --filename 2.png --model pro
"""

import argparse
import os
import sys
from pathlib import Path


def get_next_filename(out_dir: Path) -> str:
    """Auto-increment image filename (1.png, 2.png, ...)."""
    i = 1
    while (out_dir / f"{i}.png").exists():
        i += 1
    return f"{i}.png"


def generate_image(prompt: str, out_dir: Path, filename: str, model: str) -> Path:
    try:
        from google import genai
    except ImportError:
        print("ERROR: google-genai not installed. Run: pip install google-genai pillow", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set in environment.", file=sys.stderr)
        sys.exit(1)

    model_ids = {
        "flash": "gemini-3.1-flash-image-preview",
        "pro":   "gemini-3-pro-image-preview",
    }
    model_id = model_ids.get(model, model_ids["flash"])

    client = genai.Client(api_key=api_key)

    print(f"Generating image with {model_id}...")
    print(f"Prompt: {prompt[:120]}{'...' if len(prompt) > 120 else ''}")

    response = client.models.generate_content(
        model=model_id,
        contents=[prompt],
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename

    image_saved = False
    for part in response.parts:
        if part.inline_data is not None:
            image = part.as_image()
            image.save(str(out_path))
            image_saved = True
            break

    if not image_saved:
        # Fallback: check candidates
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.inline_data is not None:
                    image = part.as_image()
                    image.save(str(out_path))
                    image_saved = True
                    break

    if not image_saved:
        print("ERROR: No image in response. Model output:", file=sys.stderr)
        for part in response.parts:
            if part.text:
                print(part.text[:300], file=sys.stderr)
        sys.exit(1)

    return out_path


def main():
    parser = argparse.ArgumentParser(description="Generate blog images with Gemini Nano Banana")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--out", required=True, help="Output directory (post Page Bundle dir)")
    parser.add_argument("--filename", default=None, help="Output filename (default: auto-increment)")
    parser.add_argument("--model", default="flash", choices=["flash", "pro"],
                        help="flash = Nano Banana 2 (fast), pro = Nano Banana Pro (high quality)")
    args = parser.parse_args()

    out_dir = Path(args.out).expanduser().resolve()
    filename = args.filename or get_next_filename(out_dir)

    out_path = generate_image(args.prompt, out_dir, filename, args.model)

    print(f"\nSaved: {out_path}")
    print(f"\nMarkdown tag:")
    print(f"![diagram]({filename})")


if __name__ == "__main__":
    main()
