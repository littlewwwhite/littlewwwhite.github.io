## 功能
- 执行下列信息即可自动优化生成内容：
	tools/blog_optimizer.py 仅仅负责优化文章，包括格式，内容
	tools/blog_processor.py 负责优化内容并上传



- tools 文件夹下仅负责内容的优化
sh tools/blog.sh

post 文件夹下仅负责内容的生成
播客 md 文件名不能包含中文，否则会报错

latex 要用 $$ 包裹，否则会报错，且在一行内，如下

```md
$$y(t) = \underbrace{g(t)}_{\text{趋势项}} + \underbrace{s(t)}_{\text{季节项}} + \underbrace{h(t)}_{\text{节假日项}} + \epsilon_t$$
```

