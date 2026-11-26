"""Builds the hand-designed SVGs (hero, tech stack, project cards, divider, footer) in dark + light.
Run: python scripts/build_static.py   → writes assets/*.svg. No network, no dependencies."""
import os
import textwrap
from theme import THEMES, SANS, MONO, esc, defs

ROOT = os.path.join(os.path.dirname(__file__), "..", "assets")

NAME = "Samit"
ROLE = "Android App Developer"
TYPED = [
    "Building Sami, a Hinglish assistant",
    "Kotlin · Compose · on-device speech",
    "BoloNyay: AI that explains rights",
    "ReelWish: reels on a daily limit",
]

PROJECTS = [
    dict(slug="sami", title="Sami", kind="Android · Voice assistant", repo="sami-assistant",
         desc="Voice-first assistant for Android. On-device wake word, Hinglish commands, an AI planner that turns speech into safe typed actions, screen control and UPI payment prep.",
         tags=["Kotlin", "Compose", "Vosk", "Groq", "Accessibility"]),
    dict(slug="bolonyay", title="BoloNyay", kind="AI · Legal rights (live)", repo="bolonyay",
         desc="Describe a real problem in English or Hindi, by typing or speaking, and get the relevant Articles of the Constitution of India, explained simply, with sources.",
         tags=["Python", "LangGraph", "RAG", "Chroma", "Streamlit"]),
    dict(slug="reelwish", title="ReelWish", kind="Android · Digital wellbeing", repo="ReelWish",
         desc="Counts the Instagram reels you watch, locks Instagram at your daily limit, and lets a group of friends see each other's counts, with cheat detection.",
         tags=["Kotlin", "Accessibility", "Device admin", "Android"]),
    dict(slug="portfolio", title="Portfolio", kind="Web · Personal site (live)", repo="My-portfolio",
         desc="My personal website: projects, skills and what I'm building next. Hand-written and hosted on GitHub Pages.",
         tags=["HTML", "CSS", "JavaScript", "GitHub Pages"]),
]

STACK = [
    ("Languages", ["Kotlin", "Python", "JavaScript", "HTML / CSS", "PowerShell"]),
    ("Android", ["Jetpack Compose", "Material 3", "Coroutines", "Accessibility services", "Vosk speech", "ML Kit", "LiteRT"]),
    ("AI & Data", ["LangChain", "LangGraph", "RAG · Chroma", "Hugging Face", "Groq API", "PyTorch", "Streamlit"]),
    ("Tools", ["Git", "GitHub", "Android Studio", "Gradle", "pytest"]),
]


def write(name: str, svg: str):
    os.makedirs(ROOT, exist_ok=True)
    with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)


# ---------------------------------------------------------------------------------------------
def hero(t: dict, theme: str) -> str:
    W, H, u = 1200, 400, f"h{theme[0]}"
    # Typing: each line gets an equal slot; its clip rect "types" in steps, holds, then erases.
    slot, cw, n = 4.5, 17.6, len(TYPED)
    total = slot * n
    lines = []
    for i, s in enumerate(TYPED):
        w = len(s) * cw + 4
        a, b = i * slot / total, (i + 1) * slot / total
        type_end = a + 1.6 / total
        erase_start = b - 0.5 / total
        kt = [0, a, type_end, erase_start, b, 1]
        kt = sorted(set(round(k, 4) for k in kt))
        vals = {0: 0, round(a, 4): 0, round(type_end, 4): w, round(erase_start, 4): w, round(b, 4): 0, 1: 0}
        if i == 0:
            vals[0] = 0
        widths = ";".join(f"{vals[k]:.1f}" for k in kt)
        cursor = ";".join(f"{70 + vals[k]:.1f}" for k in kt)
        vis = ";".join("1" if a <= k < b else "0" for k in kt)
        lines.append(f"""
  <clipPath id="{u}-c{i}"><rect x="70" y="282" height="48" width="0">
    <animate attributeName="width" dur="{total}s" repeatCount="indefinite" keyTimes="{';'.join(map(str, kt))}" values="{widths}"/>
  </rect></clipPath>
  <g clip-path="url(#{u}-c{i})"><text x="72" y="318" font-family="{MONO}" font-size="31" fill="{t['muted']}" textLength="{len(s) * cw:.0f}" lengthAdjust="spacingAndGlyphs">{esc(s)}</text></g>
  <rect y="290" width="14" height="36" rx="2" fill="{t['cyan']}" opacity="0">
    <animate attributeName="x" dur="{total}s" repeatCount="indefinite" keyTimes="{';'.join(map(str, kt))}" values="{cursor}"/>
    <animate attributeName="opacity" dur="{total}s" repeatCount="indefinite" keyTimes="{';'.join(map(str, kt))}" values="{vis}" calcMode="discrete"/>
  </rect>""")
    grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>' for x in range(0, W + 1, 40)) + \
           "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(0, H + 1, 40))
    ox, oy = 1030, 200
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{NAME}, {ROLE}">
{defs(t, u)}
<defs>
  <radialGradient id="{u}-orb" cx="0.4" cy="0.35" r="0.7">
    <stop offset="0" stop-color="{t['cyan']}" stop-opacity="0.95"/><stop offset="0.45" stop-color="{t['blue']}" stop-opacity="0.8"/><stop offset="1" stop-color="{t['violet']}" stop-opacity="0.15"/>
  </radialGradient>
  <radialGradient id="{u}-glow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{t['blue']}" stop-opacity="0.35"/><stop offset="1" stop-color="{t['blue']}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="{u}-fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t['bg']}" stop-opacity="1"/><stop offset="0.5" stop-color="{t['bg']}" stop-opacity="0.2"/><stop offset="1" stop-color="{t['bg']}" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="{u}-card"><rect width="{W}" height="{H}" rx="22"/></clipPath>
</defs>
<g clip-path="url(#{u}-card)">
  <rect width="{W}" height="{H}" fill="url(#{u}-bg)"/>
  <g stroke="{t['grid']}" stroke-width="1" opacity="0.7">{grid}</g>
  <rect width="{W * 0.62:.0f}" height="{H}" fill="url(#{u}-fade)"/>
  <rect x="0" y="-40" width="{W}" height="40" fill="url(#{u}-accent)" opacity="0.06">
    <animate attributeName="y" values="-40;{H};{H}" keyTimes="0;0.6;1" dur="7s" repeatCount="indefinite"/>
  </rect>
  <!-- orb -->
  <circle cx="{ox}" cy="{oy}" r="170" fill="url(#{u}-glow)"/>
  <circle cx="{ox}" cy="{oy}" r="112" fill="none" stroke="{t['border']}" stroke-width="1.2"/>
  <circle cx="{ox}" cy="{oy}" r="146" fill="none" stroke="{t['border']}" stroke-width="1" stroke-dasharray="3 9"/>
  <g>
    <animateTransform attributeName="transform" type="rotate" from="0 {ox} {oy}" to="360 {ox} {oy}" dur="16s" repeatCount="indefinite"/>
    <circle cx="{ox + 112}" cy="{oy}" r="5" fill="{t['cyan']}"/>
  </g>
  <g>
    <animateTransform attributeName="transform" type="rotate" from="360 {ox} {oy}" to="0 {ox} {oy}" dur="26s" repeatCount="indefinite"/>
    <circle cx="{ox}" cy="{oy - 146}" r="3.5" fill="{t['violet']}"/>
  </g>
  <circle cx="{ox}" cy="{oy}" r="62" fill="url(#{u}-orb)">
    <animate attributeName="r" values="58;66;58" dur="4.5s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{ox}" cy="{oy}" r="62" fill="none" stroke="{t['cyan']}" stroke-width="2" opacity="0">
    <animate attributeName="r" values="62;120" dur="4.5s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.6;0" dur="4.5s" repeatCount="indefinite"/>
  </circle>
  <!-- voice bars inside the orb -->
  {"".join(f'''<rect x="{ox - 26 + i * 11}" y="{oy - 4}" width="5" height="8" rx="2.5" fill="{t['panel']}" opacity="0.85">
    <animate attributeName="height" values="8;{h};8" dur="{1.1 + i * 0.13:.2f}s" repeatCount="indefinite"/>
    <animate attributeName="y" values="{oy - 4};{oy - h / 2};{oy - 4}" dur="{1.1 + i * 0.13:.2f}s" repeatCount="indefinite"/>
  </rect>''' for i, h in enumerate([18, 30, 40, 26, 14]))}
  <!-- text -->
  <text x="70" y="96" font-family="{MONO}" font-size="23" fill="{t['faint']}"><tspan fill="{t['cyan']}">~</tspan>/samit <tspan fill="{t['violet']}">$</tspan> whoami</text>
  <text x="64" y="198" font-family="{SANS}" font-size="112" font-weight="700" letter-spacing="-2" fill="url(#{u}-accent)">{NAME}</text>
  <text x="70" y="252" font-family="{SANS}" font-size="38" font-weight="500" fill="{t['text']}">{ROLE}</text>
  {''.join(lines)}
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="22" fill="none" stroke="{t['border']}"/>
</g>
</svg>"""


# ---------------------------------------------------------------------------------------------
def pill_w(s: str, fs: float) -> float:
    return len(s) * fs * 0.58 + 26


def tech(t: dict, theme: str) -> str:
    W, u, fs, ph = 1200, f"t{theme[0]}", 24, 50
    rows, y = [], 36
    colors = [t["violet"], t["blue"], t["cyan"], t["good"]]
    for ri, (label, items) in enumerate(STACK):
        rows.append(f'<text x="40" y="{y + 33}" font-family="{MONO}" font-size="19" fill="{t["faint"]}" letter-spacing="1">{esc(label.upper())}</text>')
        x0 = 230; x = x0
        for it in items:
            w = pill_w(it, fs) + 12
            if x + w > W - 36:
                x = x0; y += ph + 12
            rows.append(f'''<g><rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{ph}" rx="{ph // 2}" fill="{t['panel']}" stroke="{t['border']}"/>
<circle cx="{x + 22:.0f}" cy="{y + ph / 2}" r="6" fill="{colors[ri]}"/>
<text x="{x + 38:.0f}" y="{y + 33}" font-family="{SANS}" font-size="{fs}" fill="{t['text']}">{esc(it)}</text></g>''')
            x += w + 12
        y += ph + 30
    H = y + 6
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Tech stack">
{defs(t, u)}
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="22" fill="url(#{u}-bg)" stroke="{t['border']}"/>
{''.join(rows)}
</svg>"""


def card(t: dict, theme: str, p: dict) -> str:
    W, u = 1200, f"p{theme[0]}{p['slug']}"
    desc = textwrap.wrap(p["desc"], 78)[:3]
    ty = 150 + len(desc) * 36 + 8
    H = ty + 66
    tags, x = [], 40
    for tg in p["tags"]:
        w = pill_w(tg, 19) + 4
        tags.append(f'<rect x="{x:.0f}" y="{ty}" width="{w:.0f}" height="40" rx="20" fill="none" stroke="{t["border"]}"/>'
                    f'<text x="{x + 17:.0f}" y="{ty + 27}" font-family="{MONO}" font-size="19" fill="{t["muted"]}">{esc(tg)}</text>')
        x += w + 12
    lines = "".join(f'<text x="40" y="{150 + i * 36}" font-family="{SANS}" font-size="25" fill="{t["muted"]}">{esc(l)}</text>' for i, l in enumerate(desc))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(p['title'])}: {esc(p['desc'])}">
{defs(t, u)}
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="22" fill="{t['panel']}" stroke="{t['border']}"/>
<rect x="40" y="0" width="120" height="4" rx="2" fill="url(#{u}-accent)"/>
<text x="40" y="56" font-family="{MONO}" font-size="19" fill="{t['cyan']}" letter-spacing="1.5">{esc(p['kind'].upper())}</text>
<text x="40" y="104" font-family="{SANS}" font-size="44" font-weight="700" fill="{t['text']}">{esc(p['title'])}</text>
<text x="{W - 40}" y="56" text-anchor="end" font-family="{MONO}" font-size="20" fill="{t['faint']}">{esc(p['repo'])} ↗</text>
{lines}
{''.join(tags)}
</svg>"""


def divider(t: dict, theme: str) -> str:
    u = f"d{theme[0]}"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="24" viewBox="0 0 1200 24">
{defs(t, u)}
<defs><linearGradient id="{u}-l" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{t['violet']}" stop-opacity="0"/><stop offset="0.5" stop-color="{t['blue']}"/><stop offset="1" stop-color="{t['cyan']}" stop-opacity="0"/></linearGradient></defs>
<rect x="100" y="11.5" width="1000" height="1" fill="url(#{u}-l)"/>
<circle cx="600" cy="12" r="4" fill="{t['blue']}"><animate attributeName="cx" values="140;1060;140" dur="9s" repeatCount="indefinite"/></circle>
</svg>"""


def footer(t: dict, theme: str) -> str:
    u = f"f{theme[0]}"
    def wave(amp, off, op, dur):
        a = f"M0 60 Q 150 {60 - amp} 300 60 T 600 60 T 900 60 T 1200 60 T 1500 60 V 140 H 0 Z"
        return f'<path d="{a}" fill="url(#{u}-accent)" opacity="{op}"><animateTransform attributeName="transform" type="translate" values="0 {off};-300 {off};0 {off}" dur="{dur}s" repeatCount="indefinite"/></path>'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="140" viewBox="0 0 1200 140" role="img" aria-label="Thanks for visiting">
{defs(t, u)}
{wave(26, 18, 0.18, 12)}{wave(18, 32, 0.28, 9)}{wave(12, 46, 0.5, 7)}
<text x="600" y="122" text-anchor="middle" font-family="{MONO}" font-size="20" fill="#FFFFFF" opacity="0.92">thanks for stopping by · Samit</text>
</svg>"""


if __name__ == "__main__":
    for theme, t in THEMES.items():
        write(f"hero-{theme}.svg", hero(t, theme))
        write(f"tech-{theme}.svg", tech(t, theme))
        write(f"divider-{theme}.svg", divider(t, theme))
        write(f"footer-{theme}.svg", footer(t, theme))
        for p in PROJECTS:
            write(f"project-{p['slug']}-{theme}.svg", card(t, theme, p))
    print("static assets written to", os.path.normpath(ROOT))
