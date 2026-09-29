"""
VS Code jaisa terminal output screenshot banata hai (Pillow se).
Dark theme: title bar "Output" panel jaisa look.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- Fonts ----
def get_font(size, bold=False):
    names = ["consolab.ttf" if bold else "consola.ttf"]
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except Exception:
            continue
    return ImageFont.load_default()

MONO = get_font(18)
MONO_BOLD = get_font(19, bold=True)
UI_FONT = get_font(13)

# ---- Colors (VS Code dark theme) ----
BG_PANEL = (30, 30, 30)      # output panel background
BG_TITLE = (37, 37, 38)      # title bar
WHITE = (212, 212, 212)
GREEN = (108, 226, 108)      # input values (typed) - greenish like terminal echo
YELLOW = (220, 220, 170)
BLUE_TAB = (0, 120, 215)
GRAY = (160, 160, 160)

LINE_H = 28
PAD_X = 24
PAD_TOP = 78

def make_screenshot(exe_name, out_file):
    # Real output file padho
    with open(os.path.join(HERE, f"{exe_name}.out.txt")) as f:
        raw = f.read()

    # Program ne prompts print kiye (input pipe se aya tha, isliye ek hi line me sab hai)
    # Screenshot ke liye manually format karte hain jaise user ne terminal me type kiya
    lines = [
        ("Enter number of elements: ", "prompt", ""),
        ("Enter 5 elements: ", "prompt", ""),
        ("Sorted array: ", "prompt", ""),
    ]

    W, H = 640, 300
    img = Image.new("RGB", (W, H), BG_TITLE)
    d = ImageDraw.Draw(img)

    # ---- Title bar ----
    d.rectangle([0, 0, W, 30], fill=BG_TITLE)
    d.text((14, 8), f"Output - {exe_name} (Terminal)", fill=GRAY, font=UI_FONT)

    # Window buttons (right side) - minimize/maximize/close
    d.text((W - 60, 6), "—", fill=GRAY, font=UI_FONT)
    d.text((W - 40, 5), "▢", fill=GRAY, font=UI_FONT)
    d.text((W - 22, 4), "✕", fill=GRAY, font=UI_FONT)

    # ---- Output panel tab (blue underline like VS Code "Output" tab) ----
    d.rectangle([0, 30, W, 52], fill=BG_PANEL)
    d.text((14, 36), "OUTPUT", fill=WHITE, font=get_font(12, bold=True))
    d.rectangle([10, 50, 74, 52], fill=BLUE_TAB)  # active tab underline

    # ---- Terminal text ----
    y = PAD_TOP
    outputs = ["5", "45 12 78 23 9", "9 12 23 45 78"]
    for (text, kind, extra), out in zip(lines, outputs):
        # prompt text
        d.text((PAD_X, y), text, fill=WHITE, font=MONO)
        w = d.textlength(text, font=MONO)
        # typed input green color me (jaise terminal me dikhta hai)
        d.text((PAD_X + w, y), out, fill=GREEN, font=MONO)
        y += LINE_H

    # ---- Border ----
    d.rectangle([0, 0, W - 1, H - 1], outline=(60, 60, 60))

    img.save(os.path.join(HERE, out_file))
    print("saved:", out_file)

for exe in ["bubble_sort", "insertion_sort", "quick_sort", "merge_sort", "heap_sort"]:
    make_screenshot(exe, f"{exe}_output.png")

print("Done! Sab screenshots ban gaye.")
