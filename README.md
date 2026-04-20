# ✍️ SRT to Styled Captions (FFmpeg + Python)
[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md)

**Transform boring SRT subtitles into eye-catching, dynamic ASS captions and burn them directly into your videos — automatically.**

---

## 🎥 Preview
*(Add a Before/After image here just like your previous project)*

---

## Why This Tool?
Captions are essential for engagement, but default styles are often unreadable or ugly. This tool breathes life into your videos by converting basic `.srt` files into styled `.ass` (Advanced Substation Alpha) tracks with random animations, colors, and fonts, then burning them into your video.

---

## ✨ Features

- 🎨 **Randomized Styling** — Unique font, color, and size for every caption block
- 🎬 **Dynamic Animations** — Built-in fade-in and scale effects using ASS tags
- 📐 **Smart Layout** — Intelligent text wrapping and position clamping
- ⚡ **Batch Processing** — Automatically pairs `.srt` with `.mp4` and processes them in parallel
- 🐍 **Lightweight** — Uses Python's standard library and FFmpeg for maximum speed

---

## 🚀 Installation & Usage

### Installation
```bash
git clone [https://github.com/YourUsername/your-repo-name.git](https://github.com/YourUsername/your-repo-name.git)
cd your-repo-name

# Recommended: use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
