#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║     GitHub Profile README Auto-Generator                 ║
║     Username : RKPROGRAMMING10K                          ║
║     Schedule : Daily at 7:00 PM IST                      ║
║     Features : Live data · Animated SVGs · Time themes   ║
╚══════════════════════════════════════════════════════════╝
"""

import requests
import os
import math
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import Counter

# ──────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────

USERNAME    = "RKPROGRAMMING10K"
TOKEN       = os.environ.get("GITHUB_TOKEN", "")
API_BASE    = "https://api.github.com"

Path("assets").mkdir(exist_ok=True)
Path("scripts").mkdir(exist_ok=True)

HEADERS = {"Accept": "application/vnd.github.v3+json", "User-Agent": "ProfileBot"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

# IST = UTC + 5:30
IST   = timezone(timedelta(hours=5, minutes=30))
NOW   = datetime.now(IST)
HOUR  = NOW.hour
DATE  = NOW.strftime("%d %b %Y  %I:%M %p IST")

# ──────────────────────────────────────────────────────────
# TIME-BASED THEMES  (changes automatically)
# ──────────────────────────────────────────────────────────

def get_theme():
    if 5 <= HOUR < 12:          # 🌅 Morning  05:00–11:59
        return {
            "name": "morning",
            "greeting": "Good Morning",
            "emoji": "🌅",
            "bg1":  "#FF6B35", "bg2": "#FF9F1C", "bg3": "#FFCF77",
            "p1":   "#FFC166", "p2":  "#FFAA33",
            "txt1": "#FFFFFF",  "txt2": "#FFE8CC",
            "acc":  "#FF4500",  "glow": "#FF8C00",
            "dark": False,
        }
    elif 12 <= HOUR < 17:       # ☀️ Afternoon 12:00–16:59
        return {
            "name": "afternoon",
            "greeting": "Good Afternoon",
            "emoji": "☀️",
            "bg1":  "#003F8A", "bg2": "#0066CC", "bg3": "#3399FF",
            "p1":   "#66AAFF", "p2":  "#99CCFF",
            "txt1": "#FFFFFF",  "txt2": "#CCE5FF",
            "acc":  "#00AAFF",  "glow": "#0099FF",
            "dark": False,
        }
    elif 17 <= HOUR < 20:       # 🌇 Evening  17:00–19:59
        return {
            "name": "evening",
            "greeting": "Good Evening",
            "emoji": "🌇",
            "bg1":  "#1A0533", "bg2": "#6B21A8", "bg3": "#F97316",
            "p1":   "#CC88FF", "p2":  "#FF9966",
            "txt1": "#F5E6FF",  "txt2": "#DDB3FF",
            "acc":  "#C084FC",  "glow": "#A855F7",
            "dark": True,
        }
    else:                        # 🌙 Night    20:00–04:59
        return {
            "name": "night",
            "greeting": "Good Night",
            "emoji": "🌙",
            "bg1":  "#0D1117", "bg2": "#161B22", "bg3": "#1F2937",
            "p1":   "#3D6098", "p2":  "#2A4A7A",
            "txt1": "#E6EDF3",  "txt2": "#8B949E",
            "acc":  "#58A6FF",  "glow": "#388BFD",
            "dark": True,
        }

T    = get_theme()
DARK = T["dark"]

# ──────────────────────────────────────────────────────────
# GITHUB DATA FETCHER
# ──────────────────────────────────────────────────────────

def api(endpoint, params=None):
    try:
        r = requests.get(f"{API_BASE}{endpoint}", headers=HEADERS,
                         params=params, timeout=20)
        return r.json() if r.status_code == 200 else None
    except Exception as e:
        print(f"  ⚠ {endpoint}: {e}")
        return None

def get_all_repos():
    repos, page = [], 1
    while True:
        batch = api(f"/users/{USERNAME}/repos",
                    {"per_page": 100, "page": page, "type": "owner", "sort": "updated"})
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos

print("🔍  Fetching GitHub data for", USERNAME, "…")

USER  = api(f"/users/{USERNAME}") or {}
REPOS = get_all_repos()

STARS      = sum(r.get("stargazers_count", 0) for r in REPOS)
FORKS      = sum(r.get("forks_count", 0) for r in REPOS)
PUB_REPOS  = USER.get("public_repos", len(REPOS))
FOLLOWERS  = USER.get("followers", 0)
FOLLOWING  = USER.get("following", 0)
DISP_NAME  = USER.get("name") or USERNAME
BIO        = USER.get("bio", "") or ""
LOCATION   = USER.get("location", "") or "India"
BLOG       = USER.get("blog", "") or ""
AVATAR     = USER.get("avatar_url", "")

lang_acc = Counter()
for r in REPOS:
    if r.get("language"):
        lang_acc[r["language"]] += r.get("size", 100)

TOP_LANGS  = lang_acc.most_common(7)
LANG_TOTAL = sum(v for _, v in TOP_LANGS) or 1
TOP_REPOS  = sorted(REPOS, key=lambda r: r.get("stargazers_count", 0), reverse=True)[:6]

print(f"  ✓  Name: {DISP_NAME}  |  Repos: {PUB_REPOS}  |  Stars: {STARS}  |  Followers: {FOLLOWERS}")
print(f"  ✓  Top langs: {[l for l,_ in TOP_LANGS[:5]]}")

# ──────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────

LANG_COLORS = {
    "Python":"#3776AB","JavaScript":"#F7DF1E","TypeScript":"#3178C6",
    "Java":"#ED8B00","C":"#A8B9CC","C++":"#00599C","C#":"#239120",
    "Go":"#00ADD8","Rust":"#DEA584","PHP":"#777BB4","Ruby":"#CC342D",
    "Swift":"#FA7343","Kotlin":"#7F52FF","Dart":"#0175C2",
    "HTML":"#E34F26","CSS":"#1572B6","SCSS":"#CC6699","Shell":"#89E051",
    "Vue":"#4FC08D","R":"#276DC3","Lua":"#2C2D72","Perl":"#39457E",
    "Haskell":"#5D4F85","Scala":"#DC322F","Elixir":"#6E4A7E",
}

def lang_color(lang):  return LANG_COLORS.get(lang, "#6E7681")
def fmt(n):            return f"{n/1000:.1f}k" if n >= 1000 else str(n)

card_bg   = T["bg2"] if DARK else "#FFFFFF"
card_fg   = T["txt1"]
sub_fg    = T["txt2"]
line_col  = T["acc"] + "55"

# ──────────────────────────────────────────────────────────
# SVG 1 – HEADER  (900 × 300)
# ──────────────────────────────────────────────────────────

def make_header():
    W, H = 900, 300

    # ── Floating particles
    seed = random.Random(42)
    particles = []
    for i in range(24):
        cx  = seed.randint(10, W - 10)
        cy  = seed.randint(10, H - 10)
        r   = seed.uniform(1.5, 4.5)
        dur = round(seed.uniform(3, 8), 1)
        d   = round(seed.uniform(-dur, 0), 1)
        dy  = round(seed.uniform(10, 25), 1)
        col = T["p1"] if i % 2 == 0 else T["p2"]
        op  = round(seed.uniform(0.25, 0.65), 2)
        particles.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity="{op}">'
            f'<animate attributeName="cy" values="{cy};{cy-dy};{cy}" '
            f'dur="{dur}s" begin="{d}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="{op};{op*0.35};{op}" '
            f'dur="{dur}s" begin="{d}s" repeatCount="indefinite"/>'
            f'</circle>'
        )

    ptxt = "\n  ".join(particles)

    # ── Orbiting ring (right side decoration)
    orb_x, orb_y = 798, 148
    orb_rings = ""
    for ri, (rad, op, dur) in enumerate([(90,0.10,5),(70,0.08,4),(50,0.06,3)]):
        orb_rings += (
            f'<circle cx="{orb_x}" cy="{orb_y}" r="{rad}" '
            f'fill="none" stroke="{T["acc"]}" stroke-width="1.5" opacity="{op}">'
            f'<animate attributeName="r" values="{rad};{rad+8};{rad}" '
            f'dur="{dur}s" begin="-{ri*0.8}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="{op};{op*2};{op}" '
            f'dur="{dur}s" begin="-{ri*0.8}s" repeatCount="indefinite"/>'
            f'</circle>'
        )
    # Orbiting dot
    orb_rings += (
        f'<circle r="5" fill="{T["acc"]}" opacity="0.9">'
        f'<animateMotion dur="4s" repeatCount="indefinite">'
        f'<mpath href="#orbit"/>'
        f'</animateMotion>'
        f'</circle>'
        f'<circle r="3.5" fill="{T["p1"]}" opacity="0.7">'
        f'<animateMotion dur="6s" begin="-3s" repeatCount="indefinite">'
        f'<mpath href="#orbit2"/>'
        f'</animateMotion>'
        f'</circle>'
    )

    # ── Tech chip row
    langs_to_show = [l for l, _ in TOP_LANGS[:5]]
    if not langs_to_show:
        langs_to_show = ["Code", "GitHub", "Dev"]
    chips = []
    cx_pos = 50
    for i, lname in enumerate(langs_to_show):
        cw = len(lname) * 7.8 + 22
        col = lang_color(lname)
        delay = 0.9 + i * 0.13
        chips.append(
            f'<g opacity="0">'
            f'<rect x="{cx_pos}" y="202" width="{cw:.0f}" height="22" rx="11" '
            f'fill="{col}22" stroke="{col}" stroke-width="1"/>'
            f'<text x="{cx_pos + cw/2:.0f}" y="217" text-anchor="middle" '
            f'fill="{col}" font-size="10.5" font-family="monospace" font-weight="600">{lname}</text>'
            f'<animate attributeName="opacity" values="0;1" dur="0.4s" '
            f'begin="{delay:.2f}s" fill="freeze"/>'
            f'</g>'
        )
        cx_pos += cw + 8

    chips_svg = "\n  ".join(chips)

    # ── Bio text (truncate)
    bio_txt = BIO[:58] + ("…" if len(BIO) > 58 else "") if BIO else f"Developer · Open Source · @{USERNAME}"
    loc_txt = f"📍 {LOCATION}" if LOCATION else "📍 India"

    svg = f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Animated gradient background -->
    <linearGradient id="hdrBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"   stop-color="{T['bg1']}">
        <animate attributeName="stop-color" values="{T['bg1']};{T['bg2']};{T['bg1']}" dur="9s" repeatCount="indefinite"/>
      </stop>
      <stop offset="50%"  stop-color="{T['bg2']}">
        <animate attributeName="stop-color" values="{T['bg2']};{T['bg3']};{T['bg2']}" dur="9s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="{T['bg3']}">
        <animate attributeName="stop-color" values="{T['bg3']};{T['bg1']};{T['bg3']}" dur="9s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>

    <!-- Name gradient -->
    <linearGradient id="nameGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="{T['txt1']}"/>
      <stop offset="100%" stop-color="{T['acc']}"/>
    </linearGradient>

    <!-- Glow filter -->
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <!-- Orbit paths (for decorative dots) -->
    <path id="orbit"  d="M {orb_x-72},{orb_y} a 72,72 0 1,1 0.01,0"/>
    <path id="orbit2" d="M {orb_x+55},{orb_y} a 55,55 0 1,1 0.01,0"/>
  </defs>

  <!-- ── Background ── -->
  <rect width="{W}" height="{H}" rx="16" fill="url(#hdrBg)"/>

  <!-- ── Particles ── -->
  {ptxt}

  <!-- ── Right-side orbital decoration ── -->
  {orb_rings}

  <!-- ── Theme badge (top-left) ── -->
  <rect x="42" y="30" width="155" height="26" rx="13"
        fill="{T['acc']}25" stroke="{T['acc']}" stroke-width="1" opacity="0">
    <animate attributeName="opacity" values="0;1" dur="0.5s" begin="0.05s" fill="freeze"/>
  </rect>
  <text x="52" y="47" fill="{T['acc']}" font-size="13" font-family="monospace" font-weight="600" opacity="0">
    {T['emoji']}  {T['greeting']}
    <animate attributeName="opacity" values="0;1" dur="0.5s" begin="0.05s" fill="freeze"/>
  </text>

  <!-- ── Name ── -->
  <text x="50" y="118" fill="url(#nameGrad)"
        font-size="40" font-family="Arial Black, Arial, sans-serif"
        font-weight="900" filter="url(#glow)" opacity="0">
    {DISP_NAME}
    <animate attributeName="opacity" values="0;1" dur="0.7s" begin="0.35s" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate"
      values="0,18;0,0" dur="0.7s" begin="0.35s" fill="freeze" additive="sum"/>
  </text>

  <!-- ── Bio ── -->
  <text x="50" y="152" fill="{T['txt2']}"
        font-size="13.5" font-family="Arial, sans-serif" opacity="0">
    {bio_txt}
    <animate attributeName="opacity" values="0;1" dur="0.6s" begin="0.65s" fill="freeze"/>
  </text>

  <!-- ── Location ── -->
  <text x="50" y="176" fill="{T['txt2']}" font-size="12.5"
        font-family="Arial, sans-serif" opacity="0">
    {loc_txt}
    <animate attributeName="opacity" values="0;0.85" dur="0.5s" begin="0.8s" fill="freeze"/>
  </text>

  <!-- ── Tech chips ── -->
  {chips_svg}

  <!-- ── Quick stats row ── -->
  <g opacity="0">
    <text x="50"  y="252" fill="{T['txt2']}" font-size="12" font-family="monospace">📁 {fmt(PUB_REPOS)} Repos</text>
    <text x="185" y="252" fill="{T['txt2']}" font-size="12" font-family="monospace">⭐ {fmt(STARS)} Stars</text>
    <text x="315" y="252" fill="{T['txt2']}" font-size="12" font-family="monospace">👥 {fmt(FOLLOWERS)} Followers</text>
    <text x="470" y="252" fill="{T['txt2']}" font-size="12" font-family="monospace">🔀 {fmt(FORKS)} Forks</text>
    <animate attributeName="opacity" values="0;1" dur="0.6s" begin="1.1s" fill="freeze"/>
  </g>

  <!-- ── Divider line ── -->
  <line x1="50" y1="266" x2="660" y2="266" stroke="{T['acc']}" stroke-width="1" stroke-opacity="0.35">
    <animate attributeName="x2" values="50;660" dur="1.2s" begin="1.3s" fill="freeze" calcMode="spline" keySplines="0.4,0,0.2,1"/>
  </line>

  <!-- ── Updated timestamp ── -->
  <text x="{W-20}" y="{H-12}" text-anchor="end"
        fill="{T['txt2']}" font-size="10" font-family="monospace" opacity="0.5">
    🔄 {DATE}
  </text>
</svg>"""

    return svg


# ──────────────────────────────────────────────────────────
# SVG 2 – STATS CARDS  (900 × 130)
# ──────────────────────────────────────────────────────────

def make_stats():
    W, H = 900, 130

    bg_rect = T["bg2"] if DARK else "#F6F8FA"
    num_col = T["txt1"] if DARK else "#24292F"
    lbl_col = T["txt2"] if DARK else "#57606A"

    cards = [
        ("📁", "Repositories",  fmt(PUB_REPOS), T["acc"]),
        ("⭐", "Total Stars",   fmt(STARS),     "#E3B341"),
        ("👥", "Followers",     fmt(FOLLOWERS), "#3FB950"),
        ("🔀", "Total Forks",   fmt(FORKS),     "#F85149"),
    ]

    CW  = 195
    GAP = 20
    sx  = (W - (CW * 4 + GAP * 3)) // 2
    out = []

    for i, (icon, label, val, col) in enumerate(cards):
        x     = sx + i * (CW + GAP)
        delay = i * 0.15
        out.append(f"""
  <g opacity="0">
    <rect x="{x}" y="12" width="{CW}" height="106" rx="10"
          fill="{bg_rect}" stroke="{col}" stroke-width="1.5" stroke-opacity="0.45"/>
    <!-- Top accent strip -->
    <rect x="{x}" y="12" width="{CW}" height="5" rx="2.5" fill="{col}"/>
    <!-- Shine sweep -->
    <rect x="{x}" y="12" width="0" height="106" rx="10" fill="{col}" opacity="0.06">
      <animate attributeName="width" values="0;{CW};0" dur="2s"
               begin="{delay + 0.3}s" fill="freeze" calcMode="spline" keySplines="0.4,0,0.2,1"/>
    </rect>
    <text x="{x + CW//2}" y="52" text-anchor="middle" font-size="24">{icon}</text>
    <text x="{x + CW//2}" y="84" text-anchor="middle"
          fill="{num_col}" font-size="28" font-weight="800"
          font-family="Arial Black, Arial, sans-serif">{val}</text>
    <text x="{x + CW//2}" y="104" text-anchor="middle"
          fill="{lbl_col}" font-size="11.5" font-family="Arial, sans-serif">{label}</text>
    <animate attributeName="opacity" values="0;1" dur="0.45s" begin="{delay}s" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate"
      values="0,12;0,0" dur="0.45s" begin="{delay}s" fill="freeze" additive="sum"/>
  </g>""")

    cards_svg = "".join(out)

    return f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{W}" height="{H}" rx="12"
        fill="{'#0D1117' if DARK else '#FFFFFF'}"/>
  {cards_svg}
</svg>"""


# ──────────────────────────────────────────────────────────
# SVG 3 – LANGUAGE BARS  (900 × dynamic)
# ──────────────────────────────────────────────────────────

def make_languages():
    if not TOP_LANGS:
        return None

    BAR_H  = 26
    GAP    = 10
    LABEL_W= 140
    BAR_W  = 580
    PAD    = (900 - LABEL_W - BAR_W - 80) // 2 + 20

    W = 900
    H = len(TOP_LANGS) * (BAR_H + GAP) + 70

    dark_bg  = "#0D1117" if DARK else "#FFFFFF"
    dark_fg  = "#E6EDF3" if DARK else "#24292F"
    sub_col  = "#8B949E" if DARK else "#57606A"
    track_col= "#21262D" if DARK else "#EAECEF"

    rows = []
    for i, (lang, size) in enumerate(TOP_LANGS):
        pct   = size / LANG_TOTAL * 100
        bw    = int(pct / 100 * BAR_W)
        y     = 50 + i * (BAR_H + GAP)
        col   = lang_color(lang)
        delay = i * 0.1

        rows.append(f"""
  <!-- {lang} -->
  <text x="{PAD + LABEL_W - 8}" y="{y + 17}" text-anchor="end"
        fill="{sub_col}" font-size="12" font-family="monospace" font-weight="500">{lang}</text>
  <!-- Track -->
  <rect x="{PAD + LABEL_W}" y="{y}" width="{BAR_W}" height="{BAR_H}" rx="5" fill="{track_col}"/>
  <!-- Fill bar (animates in) -->
  <rect x="{PAD + LABEL_W}" y="{y}" width="0" height="{BAR_H}" rx="5" fill="{col}">
    <animate attributeName="width" values="0;{bw}" dur="1s" begin="{delay}s"
             fill="freeze" calcMode="spline" keySplines="0.4,0,0.2,1"/>
  </rect>
  <!-- Glow overlay on fill -->
  <rect x="{PAD + LABEL_W}" y="{y}" width="0" height="{BAR_H//2}" rx="5"
        fill="white" opacity="0.12">
    <animate attributeName="width" values="0;{bw}" dur="1s" begin="{delay}s"
             fill="freeze" calcMode="spline" keySplines="0.4,0,0.2,1"/>
  </rect>
  <!-- Percentage -->
  <text x="{PAD + LABEL_W + BAR_W + 10}" y="{y + 17}"
        fill="{sub_col}" font-size="11" font-family="monospace">{pct:.1f}%</text>
  <!-- Color dot before label -->
  <circle cx="{PAD + LABEL_W - 12}" cy="{y + BAR_H//2}" r="4" fill="{col}"/>""")

    rows_svg = "".join(rows)

    return f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{W}" height="{H}" rx="12" fill="{dark_bg}"/>
  <!-- Title -->
  <text x="{W//2}" y="28" text-anchor="middle"
        fill="{dark_fg}" font-size="16" font-weight="700"
        font-family="Arial, sans-serif">📊 Top Languages</text>
  {rows_svg}
</svg>"""


# ──────────────────────────────────────────────────────────
# SVG 4 – ANIMATED WAVE DIVIDER  (900 × 48)
# ──────────────────────────────────────────────────────────

def make_wave():
    acc = T["acc"]
    p1  = T["p1"]
    return f"""<svg width="900" height="48" viewBox="0 0 900 48" xmlns="http://www.w3.org/2000/svg">
  <!-- Wave 1 -->
  <path fill="none" stroke="{acc}" stroke-width="2" opacity="0.55"
        d="M0,24 Q112,6 225,24 T450,24 T675,24 T900,24">
    <animate attributeName="d"
      values="M0,24 Q112,6 225,24 T450,24 T675,24 T900,24;
              M0,24 Q112,42 225,24 T450,24 T675,24 T900,24;
              M0,24 Q112,6 225,24 T450,24 T675,24 T900,24"
      dur="3.5s" repeatCount="indefinite"/>
  </path>
  <!-- Wave 2 (offset phase) -->
  <path fill="none" stroke="{p1}" stroke-width="1.5" opacity="0.3"
        d="M0,24 Q112,42 225,24 T450,24 T675,24 T900,24">
    <animate attributeName="d"
      values="M0,24 Q112,42 225,24 T450,24 T675,24 T900,24;
              M0,24 Q112,6 225,24 T450,24 T675,24 T900,24;
              M0,24 Q112,42 225,24 T450,24 T675,24 T900,24"
      dur="3.5s" repeatCount="indefinite"/>
  </path>
  <!-- Travelling dot on wave -->
  <circle r="3.5" fill="{acc}" opacity="0.8">
    <animateMotion dur="4s" repeatCount="indefinite"
      path="M0,24 Q225,6 450,24 Q675,42 900,24"/>
  </circle>
</svg>"""


# ──────────────────────────────────────────────────────────
# SVG 5 – TYPING BANNER  (900 × 56)
# ──────────────────────────────────────────────────────────

def make_typing_banner():
    acc  = T["acc"]
    bg   = T["bg1"] if DARK else "#F0F6FF"
    fg   = T["txt1"] if DARK else "#1A2A4A"
    roles = [
        "Full Stack Developer",
        "Open Source Contributor",
        "Problem Solver",
        "Code Craftsman",
        "GitHub Explorer",
    ]
    # We use a CSS animation trick with multiple text elements
    role_elements = ""
    for i, role in enumerate(roles):
        total  = len(roles)
        dur    = total * 2.5
        begin  = i * 2.5
        role_elements += (
            f'<text x="450" y="36" text-anchor="middle" fill="{acc}" '
            f'font-size="17" font-family="monospace" font-weight="600" opacity="0">'
            f'{role}'
            f'<animate attributeName="opacity" '
            f'values="0;0;1;1;0;0" '
            f'keyTimes="0;{begin/dur:.3f};{(begin+0.2)/dur:.3f};{(begin+2.0)/dur:.3f};{(begin+2.4)/dur:.3f};1" '
            f'dur="{dur}s" repeatCount="indefinite"/>'
            f'</text>'
        )

    return f"""<svg width="900" height="56" viewBox="0 0 900 56" xmlns="http://www.w3.org/2000/svg">
  <rect width="900" height="56" rx="10" fill="{bg}" opacity="0.6"/>
  <text x="450" y="22" text-anchor="middle" fill="{fg}"
        font-size="11" font-family="monospace" opacity="0.6">I am a …</text>
  {role_elements}
  <!-- Blinking cursor -->
  <rect x="0" y="22" width="2" height="20" fill="{acc}" rx="1">
    <animate attributeName="opacity" values="1;1;0;0" dur="1s" repeatCount="indefinite"/>
    <animateMotion dur="12.5s" repeatCount="indefinite"
      path="M 320,0 L 580,0"/>
  </rect>
</svg>"""


# ──────────────────────────────────────────────────────────
# WRITE ALL SVG FILES
# ──────────────────────────────────────────────────────────

print("\n🎨  Generating SVG assets…")

assets = {
    "assets/header.svg":        make_header(),
    "assets/stats.svg":         make_stats(),
    "assets/wave.svg":          make_wave(),
    "assets/typing_banner.svg": make_typing_banner(),
}

langs_svg = make_languages()
if langs_svg:
    assets["assets/languages.svg"] = langs_svg

for path, content in assets.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓  {path}")

# ──────────────────────────────────────────────────────────
# GENERATE README.md
# ──────────────────────────────────────────────────────────

print("\n📝  Building README.md…")

streak_theme  = "dark" if DARK else "default"
streak_bg     = "0D1117" if DARK else "FFFFFF"
stats_theme   = "github_dark" if DARK else "default"
acc_hex       = T["acc"].lstrip("#")
name_url_safe = USERNAME

# Top repos table
repo_rows = []
for r in TOP_REPOS:
    rname = r.get("name", "")
    url   = r.get("html_url", f"https://github.com/{USERNAME}/{rname}")
    stars = r.get("stargazers_count", 0)
    forks = r.get("forks_count", 0)
    lang  = r.get("language", "—")
    desc  = (r.get("description") or "")[:60]
    if len(r.get("description", "") or "") > 60:
        desc += "…"
    repo_rows.append(f"| [**{rname}**]({url}) | {desc} | ⭐ {stars} | 🔀 {forks} | `{lang}` |")

repos_table = (
    "| Repository | Description | Stars | Forks | Language |\n"
    "|------------|-------------|-------|-------|----------|\n"
    + "\n".join(repo_rows)
) if repo_rows else "_No repositories yet — watch this space!_"

# Language shield badges
lang_badges = "  ".join(
    f"![{lang}](https://img.shields.io/badge/-{lang.replace(' ','+').replace('#','sharp').replace('+','plus')}-"
    f"{lang_color(lang).lstrip('#')}?style=flat-square&logoColor=white)"
    for lang, _ in TOP_LANGS[:6]
)

# Bio block
bio_line  = BIO if BIO else f"Software developer passionate about clean code and open source."
blog_line = f"[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-{acc_hex}?style=for-the-badge&logo=firefox-browser&logoColor=white)]({BLOG})" if BLOG else ""

readme_content = f"""<!-- ╔═══════════════════════════════════════════════════╗ -->
<!-- ║  Auto-generated by GitHub Actions                  ║ -->
<!-- ║  Theme : {T['name']:<12}  Updated : {DATE:<22}  ║ -->
<!-- ╚═══════════════════════════════════════════════════╝ -->

<div align="center">

<img src="./assets/header.svg" width="100%" alt="Profile header — {T['name']} theme"/>

</div>

<img src="./assets/wave.svg" width="100%" alt="Animated wave"/>

---

<div align="center">
<img src="./assets/typing_banner.svg" width="80%" alt="Typing roles banner"/>
</div>

---

<div align="center">
<img src="./assets/stats.svg" width="100%" alt="GitHub stats"/>
</div>

---

## 🧑‍💻 About Me

```yaml
───────────────────────────────────────────
  name       : {DISP_NAME}
  github     : @{USERNAME}
  location   : {LOCATION or "India"}
  bio        : "{bio_line[:80]}"
  stats:
    repositories : {PUB_REPOS}
    total_stars  : {STARS}
    followers    : {FOLLOWERS}
    following    : {FOLLOWING}
    total_forks  : {FORKS}
  current_theme  : {T['name']}   {T['emoji']}
  last_updated   : {DATE}
───────────────────────────────────────────
```

---

## 🛠️ Tech Stack

<div align="center">

{lang_badges}

</div>

---

## 📊 Language Distribution

<div align="center">
<img src="./assets/languages.svg" width="100%" alt="Language bar chart"/>
</div>

---

## 🔥 Top Repositories

{repos_table}

---

## 📈 GitHub Activity

<div align="center">

[![GitHub Streak](https://streak-stats.demolab.com/?user={name_url_safe}&theme={streak_theme}&hide_border=true&background={streak_bg}&ring={acc_hex}&fire={acc_hex}&currStreakLabel={acc_hex})](https://github.com/{USERNAME})

</div>

<div align="center">

[![GitHub Stats](https://github-readme-stats.vercel.app/api?username={name_url_safe}&show_icons=true&count_private=true&hide_border=true&theme={stats_theme}&title_color={acc_hex}&icon_color={acc_hex})](https://github.com/{USERNAME})&nbsp;&nbsp;[![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username={name_url_safe}&layout=compact&hide_border=true&theme={stats_theme}&title_color={acc_hex})](https://github.com/{USERNAME})

</div>

---

## 🌐 Connect with Me

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-@{USERNAME}-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/{USERNAME})
{blog_line}
[![Profile Views](https://komarev.com/ghpvc/?username={name_url_safe}&color={acc_hex}&style=for-the-badge&label=Profile+Views)](https://github.com/{USERNAME})

</div>

---

<img src="./assets/wave.svg" width="100%" alt="Animated wave"/>

<div align="center">

<sub>
🤖 This README is <b>fully automated</b> — rebuilt every day at <b>7:00 PM IST</b> via GitHub Actions.<br>
⏱ <b>Last updated:</b> {DATE} &nbsp;|&nbsp; 🎨 <b>Active theme:</b> {T['name'].title()} {T['emoji']}<br>
🌅 <i>Theme changes automatically: Morning · Afternoon · Evening · Night</i>
</sub>

</div>
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("  ✓  README.md")
print(f"\n✅  All done!  Theme: {T['name']} {T['emoji']}  |  Updated: {DATE}\n")
