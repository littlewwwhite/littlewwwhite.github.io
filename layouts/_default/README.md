# layouts/_default

PaperMod 页面与 Markdown render hook 覆盖层，控制文章页、列表页和特定 Markdown 节点的输出。

| 文件 | 用途 |
| --- | --- |
| `_markup/` | Markdown 节点 render hook；不要在此目录放 `README.md`，Hugo 会尝试把它当模板解析。 |
| `about.html` | 关于页模板。 |
| `list.html` | 列表页模板。 |
| `single.html` | 文章详情页模板。 |
