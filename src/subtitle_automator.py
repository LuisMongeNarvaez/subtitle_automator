import subprocess
import random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

W, H = 1280, 720

# ============================
# 🔤 Fonts
# ============================
def get_system_fonts():
    try:
        result = subprocess.run(
            ["fc-list", ":family"],
            capture_output=True,
            text=True,
            check=True
        )

        fonts = []
        for line in result.stdout.splitlines():
            name = line.split(",")[0].strip()
            if name and not any(x in name.lower() for x in ["emoji","symbol","dingbat"]):
                fonts.append(name)

        if fonts:
            return fonts
    except Exception:
        pass

    return ["DejaVu Sans","Arial","Verdana","Roboto","Ubuntu"]

# ============================
# 🎨 Style Pool
# ============================
def create_style_pool(fonts, n=12):
    colors = [
        "00FFFFFF","00FFFF00","0000FFFF","0000FF00",
        "00FF00FF","00FFA500","00FF0000","00FF1493"
    ]

    pool = []
    for i in range(n):
        font = random.choice(fonts)
        fontsize = random.randint(40, 95)
        color = random.choice(colors)

        style = f"S{i},{font},{fontsize},&H{color},&H80000000,-1,5,30"
        pool.append((f"S{i}", style, color, fontsize))

    return pool

# ============================
# 📍 Position + Anchor
# ============================
def get_position(fontsize, mode):
    margin = int(fontsize * 1.3)

    if mode == "left":
        return margin + 40, random.randint(margin, H - margin), 4
    elif mode == "right":
        return W - margin - 40, random.randint(margin, H - margin), 6
    else:
        return W // 2, random.randint(margin, H - margin), 5

# ============================
# ✂️ Smart Wrap
# ============================
def smart_wrap(text, max_width):
    words = text.split()
    lines, line, width = [], "", 0

    for w in words:
        w_len = len(w) * (1.2 if w.isupper() else 1)

        if width + w_len <= max_width:
            line += (" " if line else "") + w
            width += w_len + 1
        else:
            lines.append(line)
            line = w
            width = w_len

    if line:
        lines.append(line)

    return lines

def get_max_width(mode, fontsize):
    if mode == "center":
        return max(18, 30 - fontsize // 4)
    else:
        return max(12, 22 - fontsize // 5)

# ============================
# 📏 Clamp Y
# ============================
def clamp_y(y, fontsize, lines):
    line_h = int(fontsize * 1.25)
    total_h = len(lines) * line_h

    top = total_h // 2
    bottom = H - total_h // 2

    return max(top, min(y, bottom))

# ============================
# 🔒 Hard Cap
# ============================
def hard_cap(lines, max_len=32):
    return [l[:max_len] for l in lines]

# ============================
# 🎞 Animation
# ============================
def animation_block(x, y, color, anchor):
    color_bgr = color[2:]
    return (
        f"{{\\an{anchor}\\pos({x},{y})"
        f"\\bord5\\shad4"
        f"\\1c&H{color_bgr}&\\3c&H000000&"
        f"\\fscx85\\fscy85"
        f"\\t(0,120,\\fscx100\\fscy100)"
        f"}}"
    )

# ============================
# 🧠 SAFE MERGE (FIXED)
# ============================
def merge_blocks(blocks, min_duration=0.7, max_gap=0.15, max_chars=60):
    merged = []

    def parse_time(t):
        h, m, s = t.replace(",", ".").split(":")
        return int(h)*3600 + int(m)*60 + float(s)

    current = None

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3 or "-->" not in lines[1]:
            continue

        start_s, end_s = [x.strip() for x in lines[1].split("-->")]
        start = parse_time(start_s)
        end = parse_time(end_s)
        text = " ".join(lines[2:]).strip()

        if not text:
            continue

        duration = end - start

        if current is None:
            current = [start, end, text]
            continue

        gap = start - current[1]

        short_text = len(text) <= 3
        short_duration = duration < min_duration
        small_gap = gap < max_gap
        not_too_long = len(current[2]) + len(text) < max_chars

        if (short_text or short_duration) and small_gap and not_too_long:
            current[1] = end
            current[2] += " " + text
        else:
            merged.append(current)
            current = [start, end, text]

    if current:
        merged.append(current)

    return merged

def format_time(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:02}:{m:02}:{s:06.3f}"

# ============================
# 🧠 SRT → ASS
# ============================
def srt_to_ass(srt_path, ass_path):
    fonts = get_system_fonts()
    styles = create_style_pool(fonts)

    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,BackColour,Bold,Alignment,MarginV
"""

    events = """
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""

    style_lines = [f"Style: {s[1]}" for s in styles]
    dialogues = []

    raw_blocks = Path(srt_path).read_text(
        encoding="utf-8", errors="ignore"
    ).split("\n\n")

    merged_blocks = merge_blocks(raw_blocks)

    for start, end, text in merged_blocks:
        start = format_time(start)
        end = format_time(end)

        style_name, _, color, fontsize = random.choice(styles)
        mode = random.choice(["center","left","right"])

        x, y, anchor = get_position(fontsize, mode)

        max_width = get_max_width(mode, fontsize)
        wrapped = smart_wrap(text, max_width)
        wrapped = hard_cap(wrapped)

        y = clamp_y(y, fontsize, wrapped)

        final_text = "\\N".join(wrapped)
        anim = animation_block(x, y, color, anchor)

        dialogues.append(
            f"Dialogue: 0,{start},{end},{style_name},,0,0,0,,{anim}{final_text}"
        )

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header)
        f.write("\n".join(style_lines))
        f.write(events)
        f.write("\n".join(dialogues))

    print(f"→ {ass_path.name}: {len(dialogues)} lines")

# ============================
# 🔥 Burn
# ============================
def burn(video, ass):
    out = video.with_name(f"{video.stem}_chaos.mp4")

    subprocess.run([
        "ffmpeg","-y",
        "-i", str(video),
        "-vf", f"ass={ass}",
        "-c:v","libx264",
        "-preset","veryfast",
        "-crf","23",
        "-c:a","copy",
        str(out)
    ], check=True)

# ============================
# 🚀 Process
# ============================
def process(video):
    srt = video.with_suffix(".srt")
    if not srt.exists():
        return

    ass = video.with_suffix(".ass")

    print(f"🧠 {video.name}")
    srt_to_ass(srt, ass)
    burn(video, ass)

# ============================
# 🧵 MAIN
# ============================
if __name__ == "__main__":
    videos = list(Path(".").glob("*.mp4"))

    with ThreadPoolExecutor() as ex:
        ex.map(process, videos)

    print("✅ Done")
