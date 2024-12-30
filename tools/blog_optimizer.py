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

def optimize_content(content):
    """优化博客内容"""
    system_prompt = """你是一个专业的技术博客编辑，擅长优化技术文章的结构和表达。
请帮助优化以下技术博客文章，使其更易于阅读和理解，同时保持作者的专业风格。

优化原则：
1. 保持技术准确性
2. 改善文章结构，使其更有逻辑性
3. 优化段落组织，增加可读性
4. 添加适当的过渡语句
5. 保持专业的写作风格
6. 确保中文表达的流畅性
7. 适当添加示例说明
8. 保持技术文章的严谨性

请返回优化后的完整文章内容。"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"请优化以下文章内容：\n\n{content}"}
            ],
            temperature=0.7,
            stream=False
        )
        
        return response.choices[0].message.content
            
    except Exception as e:
        print(f"API 调用错误：{str(e)}")
        return None

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

def update_markdown_file(file_path):
    """更新 markdown 文件内容"""
    content = read_markdown_content(file_path)
    front_matter, main_content = extract_front_matter(content)
    
    # 优化文章内容
    optimized_content = optimize_content(main_content)
    if not optimized_content:
        print("无法优化文章内容")
        return

    print("\n内容已优化")

    # 生成新的文件内容
    new_content = f"""---
{yaml.dump(front_matter, allow_unicode=True, sort_keys=False)}---

{optimized_content}"""

    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\n已更新文件：{file_path}")

def main():
    if len(sys.argv) != 2:
        print("使用方法：python blog_optimizer.py <文章名称或all>")
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
