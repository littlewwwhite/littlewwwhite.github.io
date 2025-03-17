---
date: '2025-03-14'
categories:
- Python开发
- 工具使用
tags:
- uv
- Python包管理
- 虚拟环境
- 依赖管理
title: Uv 的使用方法示例
---

在 Python 项目中使用 `uv`（Astral 团队开发的高效包管理工具）有两种常见场景：**在已有项目中引入 `uv`** 和 **用 `uv` 新建一个项目**。下面我将通俗地解释这两种用法的步骤和方法，并用类比和例子说明。

---

### **一、在已有项目中使用 `uv`**

#### **场景**
你已经有一个 Python 项目，可能之前用的是 `pip`、`venv` 或 `Poetry`，依赖可能记录在 `requirements.txt` 或 `pyproject.toml` 中。现在想切换到 `uv`，享受它的高速和便利。

#### **步骤**
1. **安装 `uv`**：
   - 先确保 `uv` 已安装。可以用以下命令全局安装：
     ```bash
     pip install uv
     ```
   - 或用 Homebrew（macOS/Linux）：
     ```bash
     brew install uv
     ```

2. **检查现有依赖文件**：
   - 如果有 `requirements.txt`，可以直接用它导入 `uv`。
   - 如果有 `pyproject.toml`（比如用 Poetry 或 PEP 621 标准），`uv` 也能识别。
   - 如果啥都没有，就得手动整理依赖。

3. **初始化虚拟环境**：
   - 进入项目目录：
     ```bash
     cd /path/to/your/project
     ```
   - 用 `uv` 创建虚拟环境（默认在 `.venv` 文件夹）：
     ```bash
     uv venv
     ```
   - 激活虚拟环境：
     - Linux/macOS：
       ```bash
       source .venv/bin/activate
       ```
     - Windows：
       ```bash
       .venv\Scripts\activate
       ```

4. **导入现有依赖**：
   - **从 `requirements.txt` 导入**：
     ```bash
     uv pip install -r requirements.txt
     ```
     这会安装 `requirements.txt` 里的包，然后你可以生成 `uv.lock`：
     ```bash
     uv lock
     ```
   - **从 `pyproject.toml` 导入**：
     如果已有 `[project.dependencies]` 部分，直接运行：
     ```bash
     uv sync
     ```
     `uv` 会读取 `pyproject.toml`，安装依赖并生成 `uv.lock`。

5. **同步环境**：
   - 运行 `uv sync` 确保虚拟环境与依赖文件一致：
     ```bash
     uv sync
     ```
   - 这会安装缺失的包、移除多余的包，并锁定版本。

6. **提交到版本控制**：
   - 把 `uv.lock` 加到 Git，确保团队用相同版本：
     ```bash
     git add uv.lock
     git commit -m "Add uv.lock for consistent dependencies"
     ```

#### **类比**
就像你搬进一个旧房子，之前用的是老式水电系统（`pip` 或 `venv`）。现在你请了个新装修队（`uv`），他们根据旧房子的水电图纸（`requirements.txt` 或 `pyproject.toml`）重新布线，确保一切现代化（生成 `uv.lock`），还能跑得更快。

#### **例子**
假设你有个项目，目录如下：
```
my_project/
├── requirements.txt  # requests>=2.28.1, numpy>=1.26.0
└── main.py
```
- 安装 `uv` 并创建虚拟环境：
  ```bash
  uv venv
  source .venv/bin/activate
  ```
- 导入依赖：
  ```bash
  uv pip install -r requirements.txt
  uv lock  # 生成 uv.lock
  ```
- 以后用 `uv sync` 保持一致：
  ```bash
  uv sync
  ```

---

### **二、用 `uv` 新建项目**

#### **场景**
你从零开始一个新项目，想直接用 `uv` 管理依赖和虚拟环境。

#### **步骤**
1. **安装 `uv`**：
   - 同上，确保 `uv` 已安装。

2. **创建项目目录**：
   - 新建一个文件夹并进入：
     ```bash
     mkdir new_project
     cd new_project
     ```

3. **初始化虚拟环境**：
   - 创建并激活虚拟环境：
     ```bash
     uv venv
     source .venv/bin/activate  # Linux/macOS
     # 或 .venv\Scripts\activate  # Windows
     ```

4. **初始化 `pyproject.toml`**：
   - 用 `uv` 创建一个基本的 `pyproject.toml` 文件：
     ```bash
     uv init
     ```
   - 这会生成类似以下内容：
     ```toml
     [project]
     name = "new_project"
     version = "0.1.0"
     dependencies = []
     ```
   - 你也可以手动编辑这个文件，添加项目信息。

5. **添加依赖**：
   - 用 `uv add` 添加包，比如：
     ```bash
     uv add requests
     uv add numpy
     ```
   - 每次添加，`uv` 会更新 `pyproject.toml` 并生成/更新 `uv.lock`。

6. **同步环境**：
   - 运行 `uv sync` 安装所有依赖：
     ```bash
     uv sync
     ```
   - 这会根据 `pyproject.toml` 和 `uv.lock` 配置虚拟环境。

7. **开始开发**：
   - 创建你的代码文件（比如 `main.py`），然后用虚拟环境运行：
     ```bash
     uv run python main.py
     ```

8. **版本控制**：
   - 把 `pyproject.toml` 和 `uv.lock` 提交到 Git：
     ```bash
     git add pyproject.toml uv.lock
     git commit -m "Initialize project with uv"
     ```

#### **类比**
就像你买了一块空地，雇了个建筑队（`uv`）从头盖房子。你先画个蓝图（`pyproject.toml`），告诉他们要装什么家具（依赖），他们按图纸施工（`uv sync`），还留了份详细清单（`uv.lock`），保证以后盖出来的房子一模一样。

#### **例子**
新建项目流程：
- 创建目录并初始化：
  ```bash
  mkdir my_new_app
  cd my_new_app
  uv venv
  source .venv/bin/activate
  uv init
  ```
- 添加依赖：
  ```bash
  uv add requests
  ```
  `pyproject.toml` 变成：
  ```toml
  [project]
  name = "my_new_app"
  version = "0.1.0"
  dependencies = [
      "requests>=2.28.1"
  ]
  ```
- 同步：
  ```bash
  uv sync
  ```
  这会生成 `uv.lock` 并安装 `requests`。

---

### **两者的对比**

| **方面**           | **已有项目**                          | **新建项目**                          |
|--------------------|---------------------------------------|---------------------------------------|
| **起点**           | 有现有依赖文件或环境                  | 从零开始                              |
| **第一步**         | 检查现有文件，导入依赖                | 创建 `pyproject.toml` 和虚拟环境      |
| **依赖管理**       | 用 `uv pip install` 或 `uv sync` 转换 | 用 `uv add` 逐步添加                  |
| **目标**           | 迁移到 `uv`，保持一致性               | 直接用 `uv` 构建高效工作流            |

---

### **实用技巧**
- **运行脚本**：用 `uv run` 替代 `python`，自动用虚拟环境的解释器：
  ```bash
  uv run python main.py
  ```
- **更新依赖**：用 `uv lock` 重新解析依赖并更新 `uv.lock`：
  ```bash
  uv lock
  uv sync
  ```
- **指定 Python 版本**：创建虚拟环境时可以指定：
  ```bash
  uv venv --python 3.11
  ```

---

### **总结**
- **已有项目**：像给旧车换新引擎，先装 `uv`，导入旧依赖（`requirements.txt` 或 `pyproject.toml`），然后用 `uv sync` 校准环境。
- **新建项目**：像盖新房子，从 `uv init` 开始，用 `uv add` 搭框架，`uv sync` 装家具，步步为营。

不管哪种方式，`uv` 都能让你享受超快的包管理和一致的环境，关于速度之类的数据网上有很多，这里就不赘述了。