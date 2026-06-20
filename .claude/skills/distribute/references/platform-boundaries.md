# Platform Boundaries

This distribute skill uses a small publishing surface:

| Platform | Artifact | Adaptation level | Publisher |
|---|---|---|---|
| X Premium | `longform.md` | deterministic Markdown cleanup | 爱贝壳 / X Web |
| 微信公众号 | `longform.md` | deterministic Markdown cleanup, optional HTML later | 爱贝壳 / WeChat editor |
| 知乎 | `longform.md` | deterministic Markdown cleanup | 爱贝壳 / Zhihu editor |
| 抖音图文 | `longform.md` plus optional `cards/` | deterministic reuse first | 爱贝壳 / Douyin creator center |
| 小红书 | `xhs.md` plus optional `cards/` | lossy adaptation allowed | 爱贝壳 / Xiaohongshu creator center |

Do not maintain per-platform model rewrites unless a platform proves that the shared artifact fails.

Default automation stops before the final publish/sync click.
