#!/usr/bin/env python3
import os
import sys
import json
import yaml
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# 加载.env文件
load_dotenv()

# DeepSeek API 配置
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# 初始化OpenAI客户端
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_API_URL)

# 项目根目录和posts目录的配置
PROJECT_ROOT = Path(__file__).parent.parent
POSTS_DIR = PROJECT_ROOT / "content" / "posts"

def read_markdown_content(file_path):
    """读取 markdown 文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def extract_front_matter(content):
    """提取现有的 front matter"""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                front_matter = yaml.safe_load(parts[1])
                return front_matter, parts[2].strip()
            except yaml.YAMLError:
                return {}, content
    return {}, content

def extract_json_from_response(response_text):
    """从响应文本中提取JSON内容"""
    # 移除可能的markdown代码块标记
    content = response_text.strip()
    if content.startswith('```json'):
        content = content[7:]  # 移除开头的 ```json
    if content.startswith('```'):
        content = content[3:]  # 移除开头的 ```
    if content.endswith('```'):
        content = content[:-3]  # 移除结尾的 ```
    
    # 清理并解析JSON
    content = content.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误：{str(e)}")
        print("处理后的内容：", content)
        return None

def get_content_analysis(content):
    """调用 DeepSeek API 分析内容"""
    if not DEEPSEEK_API_KEY:
        print("错误：未设置 DEEPSEEK_API_KEY 环境变量")
        sys.exit(1)

    system_prompt = """你是一个博客内容分析助手。你需要分析用户提供的博客内容，并返回以下信息：
1. 合适的标题
2. 文章描述（简短的摘要）
3. 相关标签（2-4个）
4. 分类（1-2个）

请以JSON格式返回结果，包含以下字段：
{
    "title": "文章标题",
    "description": "文章简短描述",
    "tags": ["标签1", "标签2"],
    "categories": ["分类1", "分类2"]
}
"""

    try:
        response = client.chat.completions.create(
            model=os.getenv("MODEL_NAME"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"请分析以下博客内容：\n\n{content}"}
            ],
            temperature=0.7,
            stream=False
        )
        
        result = response.choices[0].message.content
        
        # 解析JSON响应
        parsed_result = extract_json_from_response(result)
        if parsed_result:
            # 验证所需字段
            required_fields = ["title", "description", "tags", "categories"]
            if all(field in parsed_result for field in required_fields):
                return parsed_result
            else:
                print("API返回的数据格式不完整")
                print("缺少必需字段，返回内容：", parsed_result)
                return None
        return None
            
    except Exception as e:
        print(f"API 调用错误：{str(e)}")
        return None

def estimate_reading_time(content):
    """估算阅读时间（分钟）"""
    # 假设平均阅读速度为每分钟200个字
    words = len(content.split())
    chinese_chars = sum(1 for char in content if '\u4e00' <= char <= '\u9fff')
    return max(1, round((words / 200 + chinese_chars / 400)))

def format_date(date_str):
    """格式化日期"""
    date = datetime.strptime(date_str, '%Y-%m-%d')
    return date.strftime('%B %d, %Y')

def update_markdown_file(file_path):
    """更新 markdown 文件的 front matter"""
    content = read_markdown_content(file_path)
    existing_front_matter, main_content = extract_front_matter(content)
    
    # 获取 AI 分析结果
    analysis = get_content_analysis(main_content)
    if not analysis:
        print("无法获取内容分析结果")
        return

    print("\n分析结果：")
    print(f"标题: {analysis['title']}")
    print(f"描述: {analysis['description']}")
    print(f"标签: {', '.join(analysis['tags'])}")
    print(f"分类: {', '.join(analysis['categories'])}")

    # 计算阅读时间
    reading_time = estimate_reading_time(main_content)
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # 更新 front matter
    new_front_matter = {
        **existing_front_matter,
        "categories": analysis.get("categories", []),
        "date": current_date,
        "tags": analysis.get("tags", []),
        "title": analysis.get("title", existing_front_matter.get("title", "")),
    }

    # 自定义YAML dump选项
    yaml.add_representer(type(None), lambda dumper, value: dumper.represent_scalar('tag:yaml.org,2002:null', ''))
    
    # 生成新的文件内容，description放在front matter之后
    new_content = f"""---
{yaml.dump(new_front_matter, allow_unicode=True, sort_keys=False)}---

{analysis.get('description', '')}

{main_content}"""

    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\n已更新文件：{file_path}")

def process_directory(directory_path):
    """处理目录中的所有markdown文件"""
    directory = Path(directory_path)
    if not directory.is_dir():
        print(f"错误：{directory_path} 不是一个有效的目录")
        return

    # 递归查找所有markdown文件
    markdown_files = list(directory.rglob("*.md"))
    
    if not markdown_files:
        print(f"在 {directory_path} 中没有找到markdown文件")
        return

    print(f"找到 {len(markdown_files)} 个markdown文件")
    for file_path in markdown_files:
        print(f"\n处理文件：{file_path}")
        update_markdown_file(str(file_path))

def find_post(post_name):
    """在posts目录中查找指定名称的文章"""
    # 如果输入的是完整路径，检查是否为目录
    target_path = POSTS_DIR / post_name
    if target_path.exists():
        if target_path.is_dir():
            # 如果是目录，查找其中的markdown文件
            md_files = list(target_path.glob("*.md"))
            if md_files:
                return md_files[0]
        else:
            return target_path
    
    # 搜索可能的目录匹配
    possible_dirs = list(POSTS_DIR.glob(f"*{post_name}*"))
    
    if not possible_dirs:
        return None
    
    # 如果只找到一个匹配的目录，检查其中的markdown文件
    if len(possible_dirs) == 1:
        md_files = list(possible_dirs[0].glob("*.md"))
        if md_files:
            return md_files[0]
    
    # 如果找到多个匹配，列出所有选项
    print(f"\n找到多个可能的匹配：{post_name}")
    valid_dirs = []
    for dir_path in possible_dirs:
        md_files = list(dir_path.glob("*.md"))
        if md_files:
            valid_dirs.append((dir_path, md_files[0]))
    
    if not valid_dirs:
        return None
        
    for i, (dir_path, _) in enumerate(valid_dirs, 1):
        print(f"{i}. {dir_path.relative_to(POSTS_DIR)}")
    
    # 让用户选择
    while True:
        try:
            choice = input("\n请选择要处理的文章编号（输入q退出）: ")
            if choice.lower() == 'q':
                return None
            index = int(choice) - 1
            if 0 <= index < len(valid_dirs):
                return valid_dirs[index][1]
        except ValueError:
            print("请输入有效的数字")
        print("请输入有效的选项")

def main():
    if len(sys.argv) != 2:
        print("使用方法：python blog_processor.py <文章名称或all>")
        sys.exit(1)

    post_name = sys.argv[1].strip()
    
    # 处理所有文章
    if post_name.lower() == 'all':
        print("处理所有文章...")
        process_directory(POSTS_DIR)
        return
    
    # 查找特定文章
    post_path = find_post(post_name)
    if post_path and post_path.is_file():
        print(f"处理文章：{post_path.relative_to(PROJECT_ROOT)}")
        update_markdown_file(str(post_path))
    else:
        print(f"未找到匹配的文章：{post_name}")
        print(f"请确保文章位于 {POSTS_DIR} 目录下，并包含markdown文件")

if __name__ == "__main__":
    main()
