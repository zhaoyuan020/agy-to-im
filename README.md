# 🤖 antigravity-telegram-bridge

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](./LICENSE)
[![Platform: Windows/Linux](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)]()
[![CLI](https://img.shields.io/badge/backend-Antigravity%20%28agy%29-ff69b4.svg)](https://antigravity.google)

Chat with the [Antigravity CLI](https://antigravity.google) (`agy`) directly from Telegram.

Forked from `hah23255/kimi-to-im`, this version has been heavily customized to drive Google's `agy` CLI natively on **Windows and Linux**. It features 1-click startup scripts, configurable custom working directories for personal development, and automatic command menu registration.

**Self-hosted · Personal Assistant · Python · Cross-Platform**

[English](#english) · [中文](#中文)

---

## English

### What it is
A Telegram bridge daemon for the Google Antigravity CLI (`agy`). It allows you to chat with your local AI coding assistant remotely via Telegram, executing commands and modifying your actual projects seamlessly.

### Key New Features (Windows Adaptation)
* **Native Windows Support**: Removed Linux-specific dependencies (`bwrap`, `os.waitpid`, Unix signals) for flawless Windows execution.
* **1-Click Startup**: Included `start.bat` for automatic virtual environment creation, dependency installation, and daemon startup on Windows.
* **Custom Project Targeting**: Modified the state engine to allow `default_workdir` to bypass the isolated sandbox, enabling you to use the bot to edit your actual existing codebases.
* **Command Auto-Registration**: Includes `set_commands.py` to automatically register the bot's command menu with Telegram's UI.
* **Rate Limiting & Safety**: Built-in TurnQueue ratelimiting and queue management.

### Quickstart (Windows)
1. **Get a Telegram bot token** from [@BotFather](https://t.me/BotFather).
2. **Get your Telegram user ID** from [@userinfobot](https://t.me/userinfobot).
3. Clone this repository to your local machine.
4. Copy `config.example.json` to `config.json` and fill in your `bot_token` and `allowed_user_ids`. Set `default_workdir` to the absolute path of the project you want the AI to work on.
5. If you use a proxy to access Telegram API, edit `start.bat` to set `HTTP_PROXY` and `HTTPS_PROXY`.
6. Double click `start.bat` to run the bot.
7. (Optional) Run `uv run python set_commands.py` to register the quick menu commands in Telegram.

### Quickstart (Linux)
You can still use `./install.sh` and `systemctl --user start antigravity-telegram-bridge.service` as per the original repository for Linux deployments.

### Text Commands
* `/start` - Welcome message
* `/help` - Usage help
* `/status` / `/info` - Session summary
* `/settings` - Inline control panel (model, mode, reset)
* `/reset` - Start a fresh `agy` session
* `/files` - List inbox files

---

## 中文

### 简介
这是一个为 Google Antigravity CLI (`agy`) 打造的 Telegram 桥接守护进程。它允许你通过 Telegram 远程与本地的 AI 编程助手对话，直接管理和修改你电脑上的实际代码项目。

### 核心新特性（Windows 深度适配版）
* **原生 Windows 支持**：移除了原版中仅限 Linux 的依赖项（如 `bwrap` 沙盒、`os.waitpid` 僵尸进程回收、Unix 信号），在 Windows 环境下完美运行。
* **一键启动**：新增 `start.bat` 脚本，双击即可自动创建虚拟环境、安装依赖并启动机器人。
* **指定本地项目**：修改了底层状态机的安全沙盒校验规则。现在只需在 `config.json` 中配置 `default_workdir`，机器人就会直接进入你的真实项目目录去写代码，而不是被困在隔离的聊天沙盒中。
* **菜单自动注册**：新增 `set_commands.py` 脚本，可一键向 Telegram 官方注册底部快捷命令菜单。
* **流量与队列控制**：修复了原版遗漏的并发控制逻辑，完美支持用户队列限流。

### 快速开始 (Windows)
1. 在 Telegram 中找 [@BotFather](https://t.me/BotFather) 申请一个 **Bot Token**。
2. 找 [@userinfobot](https://t.me/userinfobot) 获取你自己的 **Telegram User ID**。
3. 将本项目克隆或下载到本地。
4. 将 `config.example.json` 复制一份并重命名为 `config.json`。填入你的 `bot_token` 和 `allowed_user_ids`。将 `default_workdir` 设为你想要 AI 帮你修改的本地项目的绝对路径。
5. **(国内用户注意)**：如果你需要通过代理访问 Telegram，请右键编辑 `start.bat`，在开头加上 `set HTTP_PROXY=http://127.0.0.1:端口号`。
6. 双击 `start.bat` 启动机器人！
7. (可选) 在终端运行 `uv run python set_commands.py`，即可在 Telegram 聊天界面左下角生成快捷命令菜单。

### 快速开始 (Linux)
本项目依然保留了原版的 Linux 兼容性。你可以继续使用 `./install.sh` 并通过 `systemd --user` 托管服务。

### 常用命令
* `/start` - 欢迎语
* `/help` - 帮助说明
* `/status` / `/info` - 查看当前项目和机器人运行状态
* `/settings` - 调出设置面板（可切换模型和工作模式）
* `/reset` - 清除当前的上下文记忆，重新开始
* `/files` - 列出当前上传的文件
