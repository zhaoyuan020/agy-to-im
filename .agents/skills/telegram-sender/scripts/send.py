#!/usr/bin/env python3
"""
Telegram sender script for Antigravity AI Agent.
Enables the agent to push text, photos, and files directly to the user's Telegram.
"""
from __future__ import annotations

import argparse
import mimetypes
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure UTF-8 output on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import requests

DEFAULT_TELEGRAM_API_BASE = "https://api.telegram.org"
DEFAULT_TELEGRAM_BOT_TOKEN = "8609427657:AAHa-oHP3KaYu-UoDF6wpugtEkBqvLYmRRU"
DEFAULT_TELEGRAM_CHAT_ID = "8168057505"
DEFAULT_PROXY = "http://127.0.0.1:7890"
MAX_TELEGRAM_TEXT_LENGTH = 4096


def get_token() -> str:
    return (os.environ.get("TELEGRAM_BOT_TOKEN") or DEFAULT_TELEGRAM_BOT_TOKEN).strip()


def get_chat_id(override: Optional[str] = None) -> str:
    return (override or os.environ.get("TELEGRAM_CHAT_ID") or DEFAULT_TELEGRAM_CHAT_ID).strip()


def build_session() -> requests.Session:
    session = requests.Session()
    session.trust_env = False
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY") or DEFAULT_PROXY
    if proxy:
        session.proxies.update({"http": proxy, "https": proxy})
    session.headers.update({"Connection": "close"})
    return session


def _build_url(method: str) -> str:
    token = get_token()
    if not token:
        raise RuntimeError("未配置 TELEGRAM_BOT_TOKEN，无法发送 Telegram 消息。")
    return f"{DEFAULT_TELEGRAM_API_BASE.rstrip('/')}/bot{token}/{method}"


def _chunk_text(content: str, limit: int = MAX_TELEGRAM_TEXT_LENGTH) -> List[str]:
    if len(content) <= limit:
        return [content]
    chunks: List[str] = []
    remaining = content
    while remaining:
        if len(remaining) <= limit:
            chunks.append(remaining)
            break
        split_at = remaining.rfind("\n", 0, limit)
        if split_at <= 0:
            split_at = limit
        chunks.append(remaining[:split_at])
        remaining = remaining[split_at:].lstrip("\n")
    return chunks


def send_text(content: str, chat_id: Optional[str] = None) -> bool:
    """发送纯文本或 Markdown 消息。"""
    target_chat_id = get_chat_id(chat_id)
    session = build_session()
    url = _build_url("sendMessage")
    for chunk in _chunk_text(content):
        payload: Dict[str, Any] = {
            "chat_id": target_chat_id,
            "text": chunk,
            "disable_web_page_preview": True,
        }
        resp = session.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("ok"):
            raise RuntimeError(f"Telegram 返回错误: {data}")
    return True


def send_photo(photo_path: str | Path, caption: str = "", chat_id: Optional[str] = None) -> bool:
    """发送单张图片 (JPG, PNG, WebP, GIF 等)。"""
    p = Path(photo_path).resolve()
    if not p.exists():
        raise FileNotFoundError(f"图片文件不存在: {p}")
    target_chat_id = get_chat_id(chat_id)
    session = build_session()
    url = _build_url("sendPhoto")
    
    mime_type, _ = mimetypes.guess_type(str(p))
    if not mime_type:
        mime_type = "image/jpeg"
        
    with open(p, "rb") as f:
        files = {"photo": (p.name, f, mime_type)}
        data = {"chat_id": target_chat_id}
        if caption:
            data["caption"] = caption[:1024]
        resp = session.post(url, data=data, files=files, timeout=60)
        resp.raise_for_status()
        res_data = resp.json()
        if not res_data.get("ok"):
            raise RuntimeError(f"Telegram 返回错误: {res_data}")
    return True


def send_document(file_path: str | Path, caption: str = "", chat_id: Optional[str] = None) -> bool:
    """发送任意文档或文件 (PDF, ZIP, CSV, TXT, PY, etc.)。"""
    p = Path(file_path).resolve()
    if not p.exists():
        raise FileNotFoundError(f"文件不存在: {p}")
    target_chat_id = get_chat_id(chat_id)
    session = build_session()
    url = _build_url("sendDocument")
    
    mime_type, _ = mimetypes.guess_type(str(p))
    if not mime_type:
        mime_type = "application/octet-stream"
        
    with open(p, "rb") as f:
        files = {"document": (p.name, f, mime_type)}
        data = {"chat_id": target_chat_id}
        if caption:
            data["caption"] = caption[:1024]
        resp = session.post(url, data=data, files=files, timeout=90)
        resp.raise_for_status()
        res_data = resp.json()
        if not res_data.get("ok"):
            raise RuntimeError(f"Telegram 返回错误: {res_data}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Send text, photo, or document to Telegram.")
    parser.add_argument("--text", "-t", type=str, help="Plain text message to send")
    parser.add_argument("--photo", "-p", type=str, help="Path to image/photo file to send")
    parser.add_argument("--file", "-f", "--doc", type=str, help="Path to document/file to send")
    parser.add_argument("--caption", "-c", type=str, default="", help="Caption for photo or file")
    parser.add_argument("--chat-id", type=str, default=None, help="Target Telegram Chat ID")

    args = parser.parse_args()

    if not args.text and not args.photo and not args.file:
        parser.print_help()
        return 1

    try:
        if args.photo:
            print(f"正在发送图片: {args.photo} ...")
            send_photo(args.photo, caption=args.caption, chat_id=args.chat_id)
            print("[SUCCESS] 图片发送成功！")
        elif args.file:
            print(f"正在发送文件: {args.file} ...")
            send_document(args.file, caption=args.caption, chat_id=args.chat_id)
            print("[SUCCESS] 文件发送成功！")
        elif args.text:
            print("正在发送文本消息...")
            send_text(args.text, chat_id=args.chat_id)
            print("[SUCCESS] 消息发送成功！")
        return 0
    except Exception as exc:
        print(f"[ERROR] 发送失败: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
