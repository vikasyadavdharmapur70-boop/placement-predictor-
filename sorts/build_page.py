"""
sort_programs.html banata hai:
- Har sort ka C program (code block me, syntax highlight ke saath)
- Niche uska output screenshot (base64 embed, taki file akeli chale)
- "Download PDF" button (browser print se)
"""

import base64
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

SORTS = [
    ("bubble_sort", "Bubble Sort", "Har pair ko compare karke bade ko aage bhejte hain. Sabse simple sort hai."),
    ("insertion_sort", "Insertion Sort", "Cards jaise element ko uthakar sahi jagah par daal dete hain."),
    ("quick_sort", "Quick Sort", "Pivot chunke uske chhote left, bade right me daalte hain. Sabse fast."),
    ("merge_sort", "Merge Sort", "Array ko 2 hisso me todte hain, sort karke wapas jodte hain."),
    ("heap_sort", "Heap Sort", "Max-heap banakar sabse bada element ek-ek karke nikalte hain."),
]


def highlight_c(code):
    """Simple C syntax highlighter (keywords, comments, strings, numbers)."""
    esc = html.escape(code)

    # Comments
    esc = re.sub(r"(//[^\n]*)", r"<span class='c'>\1</span>", esc)

    # Strings
    esc = re.sub(r'(&quot;.*?&quot;)', r"<span class='s'>\1</span>", esc)

    # Preprocessor
    esc = re.sub(r"(#include[^<\n]*&lt;[^&]*&gt;)", r"<span class='p'>\1</span>", esc)

    # Keywords
    kw = r"\b(int|void|char|float|double|for|while|if|else|return|include|struct|const)\b"
    esc = re.sub(kw, r"<span class='k'>\1</span>", esc)

    # Numbers
    esc = re.sub(r"\b(\d+)\b", r"<span class='n'>\1</span>", esc)

    # stdio.h
    esc = re.sub(r"&lt;(stdio\.h)&gt;", r"&lt;<span class='h'>stdio.h</span>&gt;", esc)

    # Functions (printf, scanf)
    esc = re.sub(r"\b(printf|scanf|main)\b", r"<span class='f'>\1</span>", esc)

    return esc


def build():
    sections = []

    for exe, title, desc in SORTS:
        # C code padho
        with open(os.path.join(HERE, f"{exe}.c")) as f:
            code = f.read()

        # Screenshot ko base64 me badlo ( taki html file akeli kaam kare)
        with open(os.path.join(HERE, f"{exe}_output.png"), "rb") as f:
            b64 = base64.b64encode(f.read()).decode()

        sections.append(
            f"""
<div class="program">
  <h2>{title}</h2>
  <p class="desc">{desc}</p>
  <pre class="code">{highlight_c(code)}</pre>
  <p class="shot-label">Output (VS Code Terminal Screenshot):</p>
  <img class="shot" src="data:image/png;base64,{b64}" alt="{title} output">
</div>
<hr>
"""
        )

    page = f"""<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="UTF-8">
<title>Sorting Programs in C</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{
    font-family: Georgia, 'Times New Roman', serif;
    max-width: 820px; margin: 0 auto; padding: 30px 20px;
    color: #1a1a1a; background: #fdfdfb; line-height: 1.55;
  }}
  h1 {{
    text-align: center; font-size: 26px;
    border-bottom: 3px solid #2c5f8a; padding-bottom: 12px;
  }}
  .subtitle {{ text-align: center; color: #555; margin-top: -6px; }}
  h2 {{
    color: #2c5f8a; font-size: 22px; margin-bottom: 4px;
    background: #eef3f7; padding: 8px 12px; border-left: 5px solid #2c5f8a;
  }}
  .desc {{ color: #444; font-style: italic; margin: 6px 0 14px; }}
  pre.code {{
    background: #1e1e1e; color: #d4d4d4;
    padding: 16px 18px; border-radius: 8px;
    font-family: Consolas, monospace; font-size: 13.5px;
    line-height: 1.5; overflow-x: auto; white-space: pre;
  }}
  .k {{ color: #569cd6; }}   /* keywords - blue */
  .s {{ color: #ce9178; }}   /* strings - orange */
  .c {{ color: #6a9955; }}   /* comments - green */
  .n {{ color: #b5cea8; }}   /* numbers - light green */
  .p {{ color: #c586c0; }}   /* preprocessor - purple */
  .h {{ color: #9cdcfe; }}   /* header file - light blue */
  .f {{ color: #dcdcaa; }}   /* functions - yellow */
  .shot-label {{ font-weight: bold; margin: 14px 0 6px; color: #333; }}
  img.shot {{
    width: 100%; max-width: 620px; display: block;
    border: 1px solid #bbb; border-radius: 6px; margin-bottom: 8px;
  }}
  hr {{ border: none; border-top: 2px dashed #ccc; margin: 30px 0; }}
  .btn-row {{ text-align: center; margin: 20px 0 30px; }}
  .btn {{
    background: #2c5f8a; color: white; border: none;
    padding: 14px 34px; font-size: 17px; border-radius: 8px;
    cursor: pointer; font-family: inherit;
  }}
  .btn:hover {{ background: #1d4361; }}
  .hint {{ text-align: center; color: #777; font-size: 14px; }}

  @media print {{
    .btn-row, .hint {{ display: none; }}
    body {{ background: white; }}
    pre.code {{ border-radius: 0; }}
  }}
</style>
</head>
<body>

<h1>Sorting Programs in C</h1>
<p class="subtitle">Quick Sort &bull; Merge Sort &bull; Heap Sort &bull; Insertion Sort &bull; Bubble Sort</p>

<div class="btn-row">
  <button class="btn" onclick="window.print()">&#128196; Download PDF</button>
</div>
<p class="hint">(Button dabane par print dialog khulega &rarr; "Save as PDF" select karo)</p>

{''.join(sections)}

<div class="btn-row">
  <button class="btn" onclick="window.print()">&#128196; Download PDF</button>
</div>

</body>
</html>"""

    out = os.path.join(HERE, "sort_programs.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print("saved:", out, f"({os.path.getsize(out)//1024} KB)")


if __name__ == "__main__":
    build()
