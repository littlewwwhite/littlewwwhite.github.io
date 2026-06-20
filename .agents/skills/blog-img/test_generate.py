#!/usr/bin/env python3
import unittest

import generate


class MarkdownTagTest(unittest.TestCase):
    def test_formats_image_with_caption_as_markdown_title(self) -> None:
        tag = generate.format_markdown_tag(
            "architecture.png",
            "System architecture",
            "系统边界和核心数据流",
        )

        self.assertEqual(
            tag,
            '![System architecture](architecture.png "系统边界和核心数据流")',
        )

    def test_omits_markdown_title_when_caption_is_empty(self) -> None:
        tag = generate.format_markdown_tag("diagram.png", "Architecture", "")

        self.assertEqual(tag, "![Architecture](diagram.png)")


if __name__ == "__main__":
    unittest.main()
