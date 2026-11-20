#!/usr/bin/env python3
"""Generates the SVGs in ../assets for the GitHub profile README.

Run:  python3 build/gen.py
Everything is self-contained: the VT323 font (SIL OFL) is embedded as base64, no external requests.
Edit PROJECTS below to change the cards.
"""
import base64
import html
import pathlib
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONT = base64.b64encode((ROOT / "build" / "vt323-latin.woff2").read_bytes()).decode()

# Same palette as the portfolio (src/app/effects.ts BASE_PALETTE).
CYAN, LILAC, PINK, HOT = "#6ac5fe", "#ad8cff", "#ff6ad5", "#ff1493"
NIGHT = "#0b0221"
NAVY_A, NAVY_B = "#000080", "#1084d0"  # Win95 title-bar gradient
SILVER, SHADOW, LIGHT = "#c0c0c0", "#808080", "#ffffff"

FONT_CSS = f"""
@font-face {{ font-family: 'VT323'; src: url(data:font/woff2;base64,{FONT}) format('woff2'); }}
text {{ font-family: 'VT323', 'Courier New', monospace; }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
"""

esc = lambda s: html.escape(s, quote=True)


def bevel(x, y, w, h, inset=False):
    """Win95 3D border: light top-left, dark bottom-right (swapped when inset)."""
    a, b = (SHADOW, LIGHT) if inset else (LIGHT, SHADOW)
    return (f'<path d="M{x} {y + h}V{y}H{x + w}" fill="none" stroke="{a}" stroke-width="2"/>'
            f'<path d="M{x} {y + h}H{x + w}V{y}" fill="none" stroke="{b}" stroke-width="2"/>')


def titlebar(x, y, w, title, h=26):
    bx = x + w - 4
    btns = ""
    for i, glyph in enumerate(["✕", "□", "_"]):
        X = bx - (i + 1) * 22 - (4 if i else 0)
        btns += (f'<rect x="{X}" y="{y + 4}" width="20" height="{h - 8}" fill="{SILVER}"/>' + bevel(X, y + 4, 20, h - 8)
                 + f'<text x="{X + 10}" y="{y + h - 8}" font-size="18" text-anchor="middle" fill="#000">{glyph}</text>')
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#tb)"/>'
            f'<text x="{x + 10}" y="{y + h - 7}" font-size="22" fill="#fff">{esc(title)}</text>' + btns)


def svg(w, h, body, extra_css="", defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<style>{FONT_CSS}{extra_css}</style>'
            f'<defs><linearGradient id="tb" x1="0" x2="1"><stop offset="0" stop-color="{NAVY_A}"/>'
            f'<stop offset="1" stop-color="{NAVY_B}"/></linearGradient>{defs}</defs>{body}</svg>')


# ---------------------------------------------------------------- header
def header():
    W, H, HORIZON = 1200, 400, 262
    # Floor lines fall from the horizon with ease-in, so their spacing grows like perspective.
    n, dur = 9, 6
    floor = "".join(
        f'<line class="fl" x1="0" x2="{W}" y1="{HORIZON}" y2="{HORIZON}" style="animation-delay:-{dur * i / n:.2f}s"/>'
        for i in range(n))
    vx = W / 2
    rays = "".join(
        f'<line x1="{vx}" y1="{HORIZON}" x2="{vx + k * 150}" y2="{H}" />' for k in range(-12, 13))
    sun_r = 120
    stripes = "".join(
        f'<rect class="st" x="{vx - sun_r}" y="{HORIZON - 70 + i * 16}" width="{sun_r * 2}" height="{3 + i * 1.3:.1f}" '
        f'style="animation-delay:-{i * 0.5}s"/>' for i in range(6))
    stars = "".join(
        f'<circle class="tw" cx="{(i * 397) % W}" cy="{(i * 151) % 190 + 8}" r="{1 + (i % 3) * 0.5}" '
        f'style="animation-delay:-{(i * 0.37) % 3:.2f}s"/>' for i in range(46))

    css = f"""
    .fl {{ stroke: {PINK}; stroke-width: 2; animation: fall {dur}s cubic-bezier(.55,0,1,.45) infinite; }}
    @keyframes fall {{ from {{ transform: translateY(0); opacity: 0; }} 15% {{ opacity: 1; }} to {{ transform: translateY({H - HORIZON}px); opacity: 1; }} }}
    .rays line {{ stroke: {PINK}; stroke-width: 1.5; opacity: .75; }}
    .st {{ fill: {NIGHT}; animation: rise 3s linear infinite; }}
    @keyframes rise {{ to {{ transform: translateY(-16px); }} }}
    .tw {{ fill: #fff; animation: tw 3s ease-in-out infinite; }}
    @keyframes tw {{ 50% {{ opacity: .15; }} }}
    .cur {{ animation: blink 1.06s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    .type {{ animation: type 2.4s steps(24) .4s both; }}
    @keyframes type {{ from {{ width: 0; }} }}
    .glow {{ filter: drop-shadow(0 0 6px {PINK}) drop-shadow(0 0 18px {HOT}); }}
    """
    defs = f"""
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{NIGHT}"/><stop offset=".55" stop-color="#2d0b55"/><stop offset="1" stop-color="#8a1f78"/>
    </linearGradient>
    <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffd319"/><stop offset=".55" stop-color="{PINK}"/><stop offset="1" stop-color="{HOT}"/>
    </linearGradient>
    <linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#fff"/><stop offset=".45" stop-color="{CYAN}"/><stop offset=".5" stop-color="{LILAC}"/><stop offset="1" stop-color="{PINK}"/>
    </linearGradient>
    <linearGradient id="floorfade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{NIGHT}"/><stop offset="1" stop-color="#1a0638"/>
    </linearGradient>
    <clipPath id="sunclip"><rect x="0" y="0" width="{W}" height="{HORIZON}"/></clipPath>
    <clipPath id="floorclip"><rect x="0" y="{HORIZON}" width="{W}" height="{H - HORIZON}"/></clipPath>
    <clipPath id="typeclip"><rect class="type" x="0" y="0" width="{W}" height="{H}"/></clipPath>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity=".22"/></pattern>
    <radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".6"/></radialGradient>
    """
    title_y = 150
    body = f"""
    <rect width="{W}" height="{H}" fill="url(#sky)"/>
    {stars}
    <g clip-path="url(#sunclip)">
      <circle cx="{vx}" cy="{HORIZON - 40}" r="{sun_r}" fill="url(#sun)"/>
      {stripes}
    </g>
    <rect y="{HORIZON}" width="{W}" height="{H - HORIZON}" fill="url(#floorfade)"/>
    <g clip-path="url(#floorclip)"><g class="rays">{rays}</g>{floor}</g>
    <line x1="0" x2="{W}" y1="{HORIZON}" y2="{HORIZON}" stroke="{CYAN}" stroke-width="2"/>

    <text x="{vx}" y="64" font-size="26" fill="{CYAN}" text-anchor="middle" letter-spacing="6">C:\\&gt; ZOUKKIS.EXE</text>
    <g class="glow">
      <text x="{vx + 4}" y="{title_y + 4}" font-size="118" fill="{HOT}" text-anchor="middle" opacity=".55" letter-spacing="4">ZOUKKIS</text>
      <text x="{vx}" y="{title_y}" font-size="118" fill="url(#chrome)" text-anchor="middle" letter-spacing="4">ZOUKKIS</text>
    </g>
    <rect x="{vx - 205}" y="{title_y + 22}" width="410" height="36" fill="{NIGHT}" opacity=".72"/>
    <g clip-path="url(#typeclip)">
      <text x="{vx}" y="{title_y + 48}" font-size="32" fill="#fff" text-anchor="middle">software engineering student<tspan class="cur" fill="{CYAN}">█</tspan></text>
    </g>

    <rect width="{W}" height="{H}" fill="url(#scan)" pointer-events="none"/>
    <rect width="{W}" height="{H}" fill="url(#vig)" pointer-events="none"/>
    """
    return svg(W, H, body, css, defs)


# ---------------------------------------------------------------- about window (terminal)
def about():
    W, H = 1200, 300
    lines = [
        ("> whoami", CYAN),
        ("  zoukkis — software engineering student.", "#e8e8ff"),
        ("> cat interests.txt", CYAN),
        ("  simulation & optimisation · cyber security · mesh networks (Reticulum)", "#e8e8ff"),
        ("  · mathematical modeling · procurement · interfaces that feel like 1995", "#e8e8ff"),
        ("> ls ~/events", CYAN),
        ("  junction-2026/   → built Kukkaro, an AI money coach for S-mobiili", PINK),
    ]
    rows = ""
    for i, (t, c) in enumerate(lines):
        rows += (f'<text class="ln" x="40" y="{82 + i * 28}" font-size="27" fill="{c}" xml:space="preserve" '
                 f'style="animation-delay:{0.25 + i * 0.32:.2f}s">{esc(t)}</text>')
    last = 82 + len(lines) * 28
    css = """
    .ln { opacity: 0; animation: show .01s linear forwards; }
    @keyframes show { to { opacity: 1; } }
    .cur { animation: blink 1.06s steps(1) infinite; }
    @keyframes blink { 50% { opacity: 0; } }
    """
    body = f"""
    <rect x="1" y="1" width="{W - 2}" height="{H - 2}" fill="{SILVER}"/>{bevel(1, 1, W - 2, H - 2)}
    {titlebar(5, 5, W - 10, "MS-DOS Prompt — C:\\USERS\\ZOUKKIS")}
    <rect x="12" y="38" width="{W - 24}" height="{H - 50}" fill="#05010f"/>{bevel(12, 38, W - 24, H - 50, inset=True)}
    {rows}
    <text class="ln cur" x="40" y="{last}" font-size="27" fill="{CYAN}" style="animation-delay:{0.25 + len(lines) * 0.32:.2f}s">&gt; █</text>
    """
    return svg(W, H, body, css)


# ---------------------------------------------------------------- project cards
PROJECTS = [
    dict(slug="traffic-twin", icon="🚦", file="TRAFFIC.EXE", title="Traffic Twin", status="LIVE",
         desc="What-if traffic for any town: user-equilibrium traffic on OpenStreetMap roads. Close a road and see where the traffic goes. Calibrated to Fintraffic counts.",
         tags=["JavaScript", "Leaflet", "Web Workers", "Python"]),
    dict(slug="fi-bess", icon="🔋", file="BESS.EXE", title="fi-bess", status="WIP",
         desc="How should a grid battery bid in Finland's day-ahead auction? Probabilistic price forecasts, MILP scheduling and day-by-day backtests.",
         tags=["Python", "Pyomo", "HiGHS", "pandas"]),
    dict(slug="youtube-listen-mcp", icon="🎧", file="LISTEN.EXE", title="youtube-listen-mcp", status="OPEN SOURCE",
         desc="MCP server that lets AI assistants like Claude listen to YouTube videos: captions, local Whisper transcription and screenshots, for just the time slot you ask for.",
         tags=["Python", "MCP", "Whisper"]),
    dict(slug="kukkaro", icon="👛", file="KUKKARO.EXE", title="Kukkaro", status="JUNCTION 2026",
         desc="AI money coach for S-mobiili, built at the Junction 2026 hackathon.",
         tags=["Python", "AI", "Hackathon"]),
    dict(slug="rns-scope", icon="📡", file="RNSSCOPE.EXE", title="rns-scope", status="OPEN SOURCE",
         desc="Real-time mesh topology and RF telemetry dashboard for the Reticulum Network Stack, fed by an RNode or a TCP interface.",
         tags=["Reticulum", "RF", "Dashboard"]),
    dict(slug="portfolio", icon="💾", file="PORTFOLIO.EXE", title="Retro OS portfolio", status="LIVE",
         desc="My portfolio as a Windows 95 / vaporwave desktop: boot screen, Bayer-dithered WebGL wallpaper, CRT effects and a pixel audio visualizer.",
         tags=["React", "TypeScript", "WebGL"]),
]
STATUS_COL = {"LIVE": "#00a86b", "WIP": "#c08000", "OPEN SOURCE": NAVY_A, "JUNCTION 2026": HOT}


def card(p):
    W, H = 580, 250
    lines = textwrap.wrap(p["desc"], 52)[:4]
    desc = "".join(f'<text x="28" y="{120 + i * 26}" font-size="25" fill="#111">{esc(l)}</text>' for i, l in enumerate(lines))
    tx, tags = 28, ""
    for t in p["tags"]:
        tw = 18 + len(t) * 9
        tags += (f'<rect x="{tx}" y="208" width="{tw:.0f}" height="26" fill="{SILVER}"/>' + bevel(tx, 208, round(tw), 26)
                 + f'<text x="{tx + tw / 2:.0f}" y="227" font-size="21" fill="#000" text-anchor="middle">{esc(t)}</text>')
        tx += tw + 8
    s = p["status"]
    sw = 20 + len(s) * 11
    css = """
    .wrap { animation: pop .5s cubic-bezier(.23,1,.32,1) both; }
    @keyframes pop { from { opacity: 0; transform: translateY(6px); } }
    """
    body = f"""
    <g>
    <rect x="1" y="1" width="{W - 2}" height="{H - 2}" fill="{SILVER}"/>{bevel(1, 1, W - 2, H - 2)}
    {titlebar(5, 5, W - 10, p["file"])}
    <rect x="12" y="38" width="{W - 24}" height="{H - 50}" fill="#fff"/>{bevel(12, 38, W - 24, H - 50, inset=True)}
    <text x="28" y="86" font-size="40">{p["icon"]}</text>
    <text x="78" y="84" font-size="38" fill="{NAVY_A}">{esc(p["title"])}</text>
    <rect x="{W - 28 - sw}" y="56" width="{sw}" height="28" fill="{STATUS_COL[s]}"/>
    <text x="{W - 28 - sw / 2}" y="77" font-size="22" fill="#fff" text-anchor="middle">{esc(s)}</text>
    <line x1="28" x2="{W - 28}" y1="96" y2="96" stroke="{PINK}" stroke-width="2" stroke-dasharray="4 4"/>
    {desc}
    {tags}
    </g>
    """
    return svg(W, H, body, css)


# ---------------------------------------------------------------- section titles & taskbar
def section(label):
    W, H = 1200, 56
    css = f"""
    .bar {{ animation: slide 4s linear infinite; }}
    @keyframes slide {{ to {{ transform: translateX(-40px); }} }}
    """
    defs = f"""<pattern id="hatch" width="40" height="56" patternUnits="userSpaceOnUse">
      <rect width="20" height="56" fill="{PINK}" opacity=".9"/><rect x="20" width="20" height="56" fill="{LILAC}" opacity=".9"/></pattern>
      <clipPath id="c"><rect width="{W}" height="{H}"/></clipPath>"""
    tw = 40 + len(label) * 17
    body = f"""
    <g clip-path="url(#c)"><rect class="bar" x="0" y="26" width="{W + 80}" height="4" fill="url(#hatch)"/></g>
    <rect x="0" y="8" width="{tw}" height="40" fill="{NIGHT}" stroke="{CYAN}" stroke-width="2"/>
    <text x="20" y="38" font-size="32" fill="{CYAN}">{esc(label)}</text>
    """
    return svg(W, H, body, css, defs)


def taskbar():
    W, H = 1200, 44
    css = """.cur { animation: blink 1.06s steps(1) infinite; } @keyframes blink { 50% { opacity: 0; } }"""
    items = ["🚦 Traffic Twin", "🔋 fi-bess", "🎧 listen-mcp", "📡 rns-scope"]
    x, tabs = 104, ""
    for it in items:
        w = 170
        tabs += (f'<rect x="{x}" y="6" width="{w}" height="32" fill="{SILVER}"/>' + bevel(x, 6, w, 32)
                 + f'<text x="{x + 10}" y="29" font-size="22" fill="#000">{esc(it)}</text>')
        x += w + 6
    body = f"""
    <rect width="{W}" height="{H}" fill="{SILVER}"/><line x1="0" x2="{W}" y1="1" y2="1" stroke="#fff" stroke-width="2"/>
    <rect x="6" y="6" width="88" height="32" fill="{SILVER}"/>{bevel(6, 6, 88, 32)}
    <text x="16" y="30" font-size="25" fill="#000">⊞ Start</text>
    {tabs}
    <rect x="{W - 160}" y="6" width="154" height="32" fill="{SILVER}"/>{bevel(W - 160, 6, 154, 32, inset=True)}
    <text x="{W - 150}" y="29" font-size="22" fill="#000">🔊 <tspan fill="{HOT}">♥</tspan> 1995<tspan class="cur">_</tspan></text>
    """
    return svg(W, H, body, css)


def main():
    ASSETS.mkdir(exist_ok=True)
    out = {"header.svg": header(), "about.svg": about(), "taskbar.svg": taskbar(),
           "section-projects.svg": section("PROJECTS.LNK"), "section-stack.svg": section("SYSTEM.INI"),
           "section-contact.svg": section("NETWORK NEIGHBORHOOD")}
    for p in PROJECTS:
        out[f"card-{p['slug']}.svg"] = card(p)
    for name, data in out.items():
        (ASSETS / name).write_text(data, encoding="utf-8")
    print("\n".join(f"{n}  {len(d) // 1024} KB" for n, d in out.items()))


if __name__ == "__main__":
    main()
