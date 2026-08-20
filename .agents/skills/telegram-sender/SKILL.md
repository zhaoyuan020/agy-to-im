---
name: telegram-sender
description: >-
  Send files, photos, images, generated charts, code documents, logs, or notifications directly to the user's Telegram chat.
  Activate and use this skill whenever the user asks to send, push, forward, upload, or deliver any file, picture, screenshot, document, report, or message to Telegram.
---

# Telegram Sender Skill

Use this skill to directly deliver files, photos, charts, reports, or text notifications to the user's Telegram.

## Helper Script Location

The helper script is located at:
- `python C:\Users\zhaoy\.gemini\config\skills\telegram-sender\scripts\send.py`
- or `python tg_send.py` (if present in the current workspace)

## Usage Instructions

When the user asks you to send a file, photo, or notification to Telegram, execute the script via terminal/command runner:

### 1. Send an Image or Photo
```bash
python C:\Users\zhaoy\.gemini\config\skills\telegram-sender\scripts\send.py --photo "path/to/image.png" --caption "可选的说明文字"
```

### 2. Send a Document, Code File, PDF, or Report
```bash
python C:\Users\zhaoy\.gemini\config\skills\telegram-sender\scripts\send.py --file "path/to/report.pdf" --caption "分析报告"
```

### 3. Send a Text Message / Notification
```bash
python C:\Users\zhaoy\.gemini\config\skills\telegram-sender\scripts\send.py --text "任务已执行完毕！"
```

## Workflow Example
1. Generate the file or image (e.g. save to `output.png` or `report.txt`).
2. Run the command: `python C:\Users\zhaoy\.gemini\config\skills\telegram-sender\scripts\send.py --photo output.png --caption "这是为您生成的图片"`
3. Confirm to the user that the file has been dispatched to their Telegram.
