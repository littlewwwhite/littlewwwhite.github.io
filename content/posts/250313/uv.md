---
categories:
- 编程
- 工具
date: '2025-03-15'
tags:
- Python
- 项目管理
- uv
- 虚拟环境
title: uv 的崛起：能否替代 Poetry、pyenv 和 pipx？
---

本文介绍了新兴的 Python 项目管理工具 uv，探讨了其功能、使用方式以及与传统工具如 Poetry、pyenv 和 pipx 的对比。uv 以其轻量、快速和简洁的特点，逐渐成为 Python 开发者的新选择。
关于 python 的项目管理一直是个难题，之前一直使用的是 conda，但是 conda 太重了，而且不是全流程管理，所以一直想找一个轻量级的项目管理工具，然后发现了 uv，一款新的 python 项目管理工具，感觉还不错，所以分享一下。

### uv 的使用方式

#### 简介
uv 是一种新兴的 Python 项目管理工具，旨在简化依赖管理和虚拟环境设置，速度快且界面简洁。它被认为可能替代传统工具如 Poetry、pyenv 和 pipx，受到社区的广泛讨论和好评。以下是 uv 的具体使用方式，基于社区的实践和反馈。

#### 启动新项目
- 使用 `uv init --name myproject` 在新目录下初始化项目，自动生成 `pyproject.toml` 文件，方便快速开始开发。

#### 管理依赖
- 添加 PyPI 包：运行 `uv add package_name`，如 `uv add requests`。
- 添加 Git 仓库包：使用 `uv add -e git+https://github.com/user/project` 安装自定义包。

#### 管理虚拟环境
- 创建虚拟环境：执行 `uv venv`，生成项目专属的隔离环境。
- 激活虚拟环境：
  - Unix-like 系统：`source venv/bin/activate`
  - Windows 系统：`venv\Scripts\activate`

#### 运行脚本
- 在虚拟环境中运行脚本：使用 `uv run myscript.py`，确保依赖正确加载。

#### 锁定和更新依赖
- 生成锁文件：运行 `uv lock` 记录精确的依赖版本，确保可重复性。
- 更新依赖：执行 `uv update --all` 更新所有包到最新版本。

#### CI/CD 集成
- 在持续集成脚本中，使用 `uv init` 和 `uv venv` 设置环境，例如在测试或构建前快速准备。

#### 提示和最佳实践
- 从其他工具迁移时，比较并调整 `pyproject.toml` 文件。
- 指定 Python 版本：如 `uv venv --python python3.9`。
- 通过编辑 `pyproject.toml` 自定义默认选项或添加脚本。

---

实际应用，涵盖以下主要场景：

1. **启动新项目**：
   - 用户分享，使用 `uv init --name myproject` 可以在现有目录快速初始化项目，生成 `pyproject.toml`，无需额外配置。相比 Poetry，uv 不强制创建新目录，操作更灵活。

2. **管理依赖**：
   - 添加依赖是常见操作，例如 `uv add requests` 安装 PyPI 包，或 `uv add -e git+https://github.com/user/project` 安装 Git 仓库中的自定义包。社区提到，uv 的依赖添加速度快，且锁文件（lockfile）生成后可直接用于项目，确保一致性。

3. **虚拟环境管理**：
   - 创建虚拟环境使用 `uv venv`，激活方式因系统不同：
     - Unix-like 系统：`source venv/bin/activate`
     - Windows 系统：`venv\Scripts\activate`
   - 用户反馈，uv 的虚拟环境管理比 pyenv 更直观，适合团队协作。

4. **运行脚本**：
   - 在虚拟环境中运行脚本，命令为 `uv run myscript.py`，确保依赖正确加载。社区案例中，有人用此功能在开发中快速测试脚本。

5. **锁定和更新依赖**：
   - 生成锁文件：`uv lock` 记录精确依赖版本，适合需要可重复构建的项目。
   - 更新依赖：`uv update --all` 可一次性更新所有包，社区用户提到此功能在维护长期项目时非常实用。

6. **CI/CD 集成**：
   - 在 CI/CD 管道中，uv 被用于快速设置环境。例如，运行 `uv init` 和 `uv venv` 后，直接执行测试或构建脚本。用户分享，uv 在 GitHub Actions 或 GitLab CI 中表现良好，减少了设置时间。

#### 提示和最佳实践
基于社区讨论，以下是 uv 使用中的一些建议：
- **迁移工具**：从 Poetry 迁移时，比较 `pyproject.toml` 文件，调整依赖和设置。用户提到，uv 的文件格式与 Poetry 兼容性较高，迁移成本低。
- **多版本 Python**：通过 `uv venv --python python3.9` 指定 Python 版本，适合需要不同版本的项目。
- **自定义配置**：编辑 `pyproject.toml` 可设置默认选项或添加自定义脚本，例如定义运行命令，增强开发效率。

#### 对比与总结
以下表格总结 uv 的主要使用命令和适用场景：

| **功能**               | **命令**                              | **适用场景**                     |
|-----------------------|---------------------------------------|----------------------------------|
| 启动新项目            | `uv init --name myproject`            | 新项目初始化，快速设置结构       |
| 添加依赖              | `uv add package_name` 或 `-e Git URL` | 安装 PyPI 包或自定义 Git 包      |
| 创建虚拟环境          | `uv venv`                             | 隔离项目依赖，团队协作           |
| 激活虚拟环境          | `source venv/bin/activate` (Unix) 或 `venv\Scripts\activate` (Windows) | 开发和测试环境准备              |
| 运行脚本              | `uv run myscript.py`                  | 在虚拟环境中执行脚本            |
| 生成锁文件            | `uv lock`                             | 确保依赖可重复性，CI/CD 使用     |
| 更新依赖              | `uv update --all`                     | 维护项目，更新包到最新版本       |
| CI/CD 集成            | `uv init; uv venv`                    | 自动化构建和测试环境设置         |

uv 的使用方式体现了其设计初衷：简单、快速、实用。社区反馈显示，它特别适合快速原型开发、团队协作和 CI/CD 场景，但文档完善度和复杂工作流的说明仍有提升空间。


---

### 关键引文
- [uv after 0.5.0 - might be worth replacing Poetry/pyenv/pipx](https://www.reddit.com/r/Python/comments/1gqh4te/uv_after_050_might_be_worth_replacing/)
- [If you use uv, what are your use cases for uv?](https://www.reddit.com/r/Python/comments/1guf2fh/if_you_use_uv_what_are_your_use_cases_for_uvx/)