"""
Build a neofetch-style info card SVG (Andrew6rant style) to sit beside or below
the ASCII portrait: colored key/value rows for education, tech stack, and
highlights.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 540, 520
PAD = 20
TITLEBAR_H = 30
KEY_X = PAD
VAL_X = PAD + 98
LINE_H = 20.5

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
KEY = "#ffa657"      # orange keys
SECTION = "#58a6ff"  # blue section headers
GREEN = "#3fb950"
ACCENT = "#22d3ee"

HOST = os.environ.get("GH_PROFILE_USER", "Venky9959-code")

ROWS = [
    ("host",),
    ("kv", "Name",      "Banavathu Venkateswararao (Venky)"),
    ("kv", "Role",      "Full-Stack Dev · CSE Student · AI Enthusiast"),
    ("kv", "College",   "VR Siddhartha Engineering College (VRSEC)"),
    ("kv", "Degree",    "B.Tech in Computer Science (2023 - 2027)"),
    ("kv", "Location",  "Vijayawada, Andhra Pradesh, India"),
    ("gap",),
    ("sec", "Tech Stack"),
    ("kv", "Frontend",  "React.js · JavaScript · HTML5 · CSS3 · Tailwind"),
    ("kv", "Backend",   "Node.js · Express.js · REST APIs · Auth/OTP"),
    ("kv", "Database",  "MySQL · SQL · Schema Design · CRUD"),
    ("kv", "AI / ML",   "CNN · Prophet · Scikit-Learn · Computer Vision"),
    ("kv", "Languages", "Python · JavaScript · C · C++"),
    ("kv", "Tools",     "Git · GitHub · VS Code · npm · Vite"),
    ("gap",),
    ("sec", "Key Projects"),
    ("bul", "Epidemiological Forecasting (React · Prophet · MySQL · PWA)"),
    ("bul", "Smart Waste Segregation with CNN (Deep Learning & CV)"),
    ("bul", "SkillsBoostHub Platform (MERN-style · Razorpay · Nodemailer)"),
    ("gap",),
    ("sec", "Connect"),
    ("kv", "LinkedIn",  "linkedin.com/in/venky-banavathu-2377082a3"),
    ("kv", "Email",     "venky995982@gmail.com"),
]


def esc(s):
    return html.escape(s)


def rise(inner, i):
    """fade + slight upward slide, staggered by row index; freezes visible."""
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.15 + i * 0.05
    return (f'<g opacity="0" transform="translate(0,5)">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" '
            f'begin="{delay:.2f}s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>')


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>'
    f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">{HOST}@github: ~$ neofetch --profile</text>')

y = TITLEBAR_H + 24
for i, r in enumerate(ROWS):
    kind = r[0]
    if kind == "host":
        content = (f'<text x="{KEY_X}" y="{y}" fill="{MUTED}" font-size="12.5">'
                   f'<tspan fill="{ACCENT}">{HOST}</tspan>@<tspan fill="{MUTED}">github</tspan></text>'
                   f'<line x1="{KEY_X}" y1="{y+4}" x2="{W-PAD}" y2="{y+4}" stroke="{FRAME}"/>')
        parts.append(rise(content, i))
        y += LINE_H - 2
    elif kind == "kv":
        k, v = r[1], r[2]
        content = (f'<text x="{KEY_X}" y="{y}" fill="{KEY}" font-size="12">{esc(k)}</text>'
                   f'<text x="{VAL_X}" y="{y}" fill="{INK}" font-size="12">{esc(v)}</text>')
        parts.append(rise(content, i))
        y += LINE_H
    elif kind == "sec":
        title = r[1]
        content = (f'<text x="{KEY_X}" y="{y}" fill="{SECTION}" font-size="11" letter-spacing="1">'
                   f'-- {esc(title.upper())} --</text>')
        parts.append(rise(content, i))
        y += LINE_H - 4
    elif kind == "bul":
        text = r[1]
        content = (f'<circle cx="{KEY_X+4}" cy="{y-3.5}" r="2" fill="{GREEN}"/>'
                   f'<text x="{KEY_X+14}" y="{y}" fill="{INK}" font-size="11.5">{esc(text)}</text>')
        parts.append(rise(content, i))
        y += LINE_H
    elif kind == "gap":
        y += 6

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes")
