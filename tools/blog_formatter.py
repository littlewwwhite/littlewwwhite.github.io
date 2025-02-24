#!/usr/bin/env python3
import os
import sys
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

def get_content_analysis(content):
    """调用 DeepSeek API 分析内容"""
    if not DEEPSEEK_API_KEY:
        print("错误：未设置 DEEPSEEK_API_KEY 环境变量")
        sys.exit(1)

    system_prompt = """你是一个博客内容分析助手。你需要分析用户提供的博客内容，并返回以下信息：
1. 相关标签（2-4个）
2. 分类（1-2个）

请以JSON格式返回结果，包含以下字段：
{
    "tags": ["标签1", "标签2"],
    "categories": ["分类1", "分类2"]
}

示例格式：

---
categories:
- 云计算
- 数据库
date: '2025-02-21'
tags:
- AWS S3
- Qdrant
- MySQL
- 文件处理
title: 结合 AWS S3、Qdrant 和 MySQL 的文件处理与存储机制
---


注意：
- 标签应该具体且相关
- 分类应该是更广泛的主题领域
- 不要修改或生成新的标题和描述
"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"请分析以下博客内容：\n\n{content}"}
            ],
            temperature=0.7,
            stream=False
        )
        
        result = response.choices[0].message.content
        try:
            # 移除可能的markdown代码块标记
            result = result.replace('```json', '').replace('```', '').strip()
            return yaml.safe_load(result)
        except yaml.YAMLError as e:
            print(f"YAML解析错误：{str(e)}")
            return None
            
    except Exception as e:
        print(f"API 调用错误：{str(e)}")
        return None

def format_front_matter(file_path):
    """格式化 markdown 文件的 front matter"""
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取现有的 front matter
    front_matter = {}
    main_content = content
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                # 确保 front_matter 是字典类型
                yaml_content = yaml.safe_load(parts[1])
                if isinstance(yaml_content, dict):
                    front_matter = yaml_content
                else:
                    front_matter = {}
                main_content = parts[2].strip()
            except yaml.YAMLError:
                print(f"警告：front matter 解析失败，将创建新的 front matter")
                front_matter = {}
    
    # 获取文件夹名称中的日期（格式：YYMMDD）
    folder_name = file_path.parent.name
    if len(folder_name) == 6 and folder_name.isdigit():
        date = f"20{folder_name[:2]}-{folder_name[2:4]}-{folder_name[4:]}"
    else:
        date = datetime.now().strftime('%Y-%m-%d')
    
    # 获取AI分析结果
    analysis = get_content_analysis(main_content)
    if analysis and isinstance(analysis, dict):
        # 更新 front matter
        front_matter.update({
            "date": date,
            "categories": analysis.get("categories", []),
            "tags": analysis.get("tags", [])
        })
    else:
        # 如果AI分析失败，至少确保基本字段存在
        front_matter.update({
            "date": date,
            "categories": front_matter.get("categories", []),
            "tags": front_matter.get("tags", [])
        })
    
    # 如果没有标题，使用文件名作为标题
    if "title" not in front_matter:
        front_matter["title"] = file_path.stem.replace('-', ' ').title()
    
    # 生成新的文件内容
    new_content = f"""---
{yaml.dump(front_matter, allow_unicode=True, sort_keys=False)}---

{main_content}"""

    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\n已更新文件格式：{file_path}")
    print(f"分类: {', '.join(front_matter.get('categories', []))}")
    print(f"标签: {', '.join(front_matter.get('tags', []))}")

def process_folder(folder_name):
    """处理指定文件夹中的markdown文件"""
    folder_path = POSTS_DIR / folder_name
    if not folder_path.exists():
        print(f"错误：找不到文件夹 {folder_name}")
        return
    
    if not folder_path.is_dir():
        print(f"错误：{folder_name} 不是一个文件夹")
        return
    
    md_files = list(folder_path.glob("*.md"))
    if not md_files:
        print(f"在 {folder_name} 中没有找到markdown文件")
        return
    
    print(f"找到 {len(md_files)} 个markdown文件")
    for file_path in md_files:
        print(f"\n处理文件：{file_path.name}")
        format_front_matter(file_path)

def main():
    if len(sys.argv) != 2:
        print("使用方法：python blog_formatter.py <文件夹名称>")
        sys.exit(1)

    folder_name = sys.argv[1].strip()
    process_folder(folder_name)

if __name__ == "__main__":
    main() 