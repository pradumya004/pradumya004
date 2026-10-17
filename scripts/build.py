"""Builds the animated SVG tiles for the profile README.

Run from the repo root: python scripts/build.py
Writes assets/<tile>-dark.svg and assets/<tile>-light.svg.

GitHub strips JS and CSS from READMEs, but CSS inside an SVG served as an
image still animates. Every tile honours prefers-reduced-motion.
"""

import base64
import io
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "src"
OUT = ROOT / "assets"

FONT = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI Variable Display', 'Segoe UI', Inter, Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, monospace"
EASE = "cubic-bezier(.16,1,.3,1)"

THEMES = {
    "dark": dict(
        bg="#000000", fg="#f5f5f7", fg2="#a1a1a6", fg3="#6e6e73",
        line="#ffffff1f", chip="#1d1d1f", chipline="#ffffff26",
        g1="#34d399", g2="#2997ff", g3="#a78bfa", glow=0.55, frame="#1d1d1f",
    ),
    "light": dict(
        bg="#fbfbfd", fg="#1d1d1f", fg2="#6e6e73", fg3="#86868b",
        line="#0000001a", chip="#ffffff", chipline="#00000017",
        g1="#059669", g2="#0071e3", g3="#7c3aed", glow=0.28, frame="#e8e8ed",
    ),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def jpeg_b64(name, width, crop=None):
    img = Image.open(SRC / name).convert("RGB")
    if crop:
        img = img.crop(crop)
    h = round(img.height * width / img.width)
    img = img.resize((width, h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=74, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def base_css(t):
    return f"""
    text {{ font-family: {FONT}; }}
    .mono {{ font-family: {MONO}; }}
    .fg {{ fill: {t['fg']}; }} .fg2 {{ fill: {t['fg2']}; }} .fg3 {{ fill: {t['fg3']}; }}
    .rise {{ transform-box: fill-box; animation: rise 1.1s {EASE} both; }}
    .fade {{ animation: fade 1.2s ease-out both; }}
    .draw {{ animation: draw 1.6s {EASE} both; }}
    .drift-a {{ animation: drift-a 16s ease-in-out infinite alternate; }}
    .drift-b {{ animation: drift-b 11s ease-in-out infinite alternate; }}
    .drift-c {{ animation: drift-c 7s ease-in-out infinite alternate; }}
    @keyframes rise {{ from {{ transform: translateY(110%); }} to {{ transform: translateY(0); }} }}
    @keyframes fade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    @keyframes drift-a {{ from {{ transform: translate(0, 0); }} to {{ transform: translate(-14px, 8px); }} }}
    @keyframes drift-b {{ from {{ transform: translate(0, 0); }} to {{ transform: translate(22px, -14px); }} }}
    @keyframes drift-c {{ from {{ transform: translate(0, 0); }} to {{ transform: translate(-8px, -10px); }} }}
    """


REDUCED = """
    @media (prefers-reduced-motion: reduce) {
      * { animation: none !important; }
      .draw { stroke-dashoffset: 0 !important; }
      .loop { display: none; }
    }
"""


def svg(w, h, label, css, body, t, radius=28):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">
  <style>{base_css(t)}{css}{REDUCED}</style>
  <defs>
    <linearGradient id="grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['g1']}"/><stop offset=".5" stop-color="{t['g2']}"/><stop offset="1" stop-color="{t['g3']}"/>
    </linearGradient>
    <linearGradient id="gline" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="0">
      <stop offset="0" stop-color="{t['g1']}"/><stop offset=".5" stop-color="{t['g2']}"/><stop offset="1" stop-color="{t['g3']}"/>
    </linearGradient>
    <radialGradient id="orb1"><stop offset="0" stop-color="{t['g2']}" stop-opacity="{t['glow']}"/><stop offset="1" stop-color="{t['g2']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="orb2"><stop offset="0" stop-color="{t['g3']}" stop-opacity="{t['glow']}"/><stop offset="1" stop-color="{t['g3']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="orb3"><stop offset="0" stop-color="{t['g1']}" stop-opacity="{t['glow'] * .8}"/><stop offset="1" stop-color="{t['g1']}" stop-opacity="0"/></radialGradient>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{t['fg']}" fill-opacity=".09"/></pattern>
    <clipPath id="tile"><rect width="{w}" height="{h}" rx="{radius}"/></clipPath>
  </defs>
  <g clip-path="url(#tile)">
    <rect width="{w}" height="{h}" fill="{t['bg']}"/>
{body}
  </g>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{radius}" fill="none" stroke="{t['line']}"/>
</svg>
"""


def pill(x, y, text, t, size=13, mono=True, accent=False):
    w = len(text) * size * (0.62 if mono else 0.56) + 26
    h = size + 16
    stroke = "url(#grad)" if accent else t["chipline"]
    cls = "mono" if mono else ""
    return (
        f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{t["chip"]}" stroke="{stroke}"/>'
        f'<text x="{x + w / 2:.0f}" y="{y + h / 2 + size * .36:.1f}" text-anchor="middle" font-size="{size}" class="{cls} fg">{esc(text)}</text>',
        w,
    )


# ---------- hero ----------

def hero(t):
    W, H = 1000, 540
    lines = [("I turn manual ops work", False), ("into automated pipelines.", True)]
    head = []
    for i, (txt, grad) in enumerate(lines):
        y = 214 + i * 74
        paint = 'fill="url(#grad)" class="rise"' if grad else 'class="fg rise"'
        head.append(
            f'<clipPath id="l{i}"><rect x="0" y="{y - 64}" width="{W}" height="84"/></clipPath>'
            f'<g clip-path="url(#l{i})"><text x="64" y="{y}" font-size="64" font-weight="700" letter-spacing="-2.2" {paint} '
            f'style="animation-delay:{.25 + i * .14:.2f}s">{txt}</text></g>'
        )

    nodes = ["inbound", "queue", "llm", "action", "done"]
    x0, x1, py = 64, 936, 448
    step = (x1 - x0) / (len(nodes) - 1)
    chips = []
    for i, n in enumerate(nodes):
        cx = x0 + i * step
        w = len(n) * 13 * .62 + 26
        x = min(max(cx - w / 2, x0), x1 - w)
        p, _ = pill(round(x), py - 14, n, t, accent=(n == "done"))
        chips.append(f'<g class="fade" style="animation-delay:{1.0 + i * .12:.2f}s">{p}</g>')

    body = f"""
    <g class="drift-a"><rect x="-40" y="-40" width="{W + 80}" height="{H + 80}" fill="url(#dots)"/></g>
    <g class="drift-b"><ellipse cx="820" cy="120" rx="360" ry="260" fill="url(#orb1)"/></g>
    <g class="drift-c"><ellipse cx="640" cy="420" rx="300" ry="200" fill="url(#orb2)"/><ellipse cx="140" cy="500" rx="260" ry="160" fill="url(#orb3)"/></g>

    <g class="fade" style="animation-delay:.05s">
      <text x="64" y="96" font-size="22" font-weight="600" class="fg" letter-spacing="-.3">Pradumya Gaurav</text>
      <text x="64" y="124" font-size="16" class="fg2">Backend engineer · Node.js, queues, LLMs · Bengaluru</text>
    </g>
    {''.join(head)}
    <text x="64" y="370" font-size="19" class="fg2 fade" style="animation-delay:.7s">Production systems where the busywork runs itself, and people only see what needs a human.</text>

    <path d="M{x0} {py}H{x1}" stroke="url(#gline)" stroke-width="1.5" stroke-dasharray="{x1 - x0}" stroke-dashoffset="{x1 - x0}" class="draw" style="animation-delay:.9s"/>
    <g class="loop"><circle cx="{x0}" cy="{py}" r="4" fill="url(#grad)" style="animation: pulse 4.2s {EASE} 2.2s infinite both"/></g>
    {''.join(chips)}
    """
    css = f"""
    @keyframes pulse {{ 0% {{ transform: translateX(0); opacity: 0; }} 6% {{ opacity: 1; }} 70% {{ transform: translateX({x1 - x0}px); opacity: 1; }} 76%, 100% {{ transform: translateX({x1 - x0}px); opacity: 0; }} }}
    """
    return svg(W, H, "Pradumya Gaurav. Backend engineer. I turn manual ops work into automated pipelines.", css, body, t)


# ---------- stats (odometer roll, number-flow style) ----------

ADV = {"d": .6, "%": .86, "+": .62, "K": .66, "→": 1.05, " ": .26}


def odometer(x, y, value, size, uid, delay, t):
    out, css, cx = [], [], x
    lh = size * 1.1
    fill = f'fill="url(#ng{uid})"'
    out.append(
        f'<linearGradient id="ng{uid}" gradientUnits="userSpaceOnUse" x1="{x}" y1="0" x2="{x + size * len(value) * .62:.0f}" y2="0">'
        f'<stop offset="0" stop-color="{t["g1"]}"/><stop offset=".55" stop-color="{t["g2"]}"/><stop offset="1" stop-color="{t["g3"]}"/></linearGradient>'
    )
    for i, ch in enumerate(value):
        adv = size * ADV.get("d" if ch.isdigit() else ch, .6)
        mid = cx + adv / 2
        if ch.isdigit():
            target = int(ch)
            seq = list(range(10)) + list(range(target + 1))
            steps = len(seq) - 1
            name = f"r{uid}_{i}"
            css.append(f"@keyframes {name} {{ from {{ transform: translateY(0); }} to {{ transform: translateY(-{steps * lh:.1f}px); }} }}")
            col = "".join(
                f'<text x="{mid:.1f}" y="{y + k * lh:.1f}" text-anchor="middle" font-size="{size}" font-weight="700" {fill}>{d}</text>'
                for k, d in enumerate(seq)
            )
            out.append(
                f'<g clip-path="url(#clip{uid})"><g style="animation:{name} {1.5 + i * .12:.2f}s {EASE} {delay:.2f}s both; transform: translateY(-{steps * lh:.1f}px)">{col}</g></g>'
            )
        elif ch != " ":
            out.append(
                f'<text x="{mid:.1f}" y="{y}" text-anchor="middle" font-size="{size}" font-weight="700" {fill} class="fade" style="animation-delay:{delay + .5:.2f}s">{esc(ch)}</text>'
            )
        cx += adv
    clip = f'<clipPath id="clip{uid}"><rect x="{x - 10}" y="{y - size}" width="{cx - x + 20:.0f}" height="{size * 1.28:.0f}"/></clipPath>'
    return clip + "".join(out), "\n".join(css)


def stats(t):
    W, H = 1000, 300
    items = [
        ("86%", "of reference checks now start", "with no human involved", "Reference-check automation"),
        ("116→14", "manual ops tasks a day,", "turnaround down 31%", "Same system, before vs after"),
        ("11K+", "WhatsApp messages in 10 weeks,", "~90% of replies auto-routed", "Meta Cloud API, built in-house"),
    ]
    gap, pad = 16, 0
    tw = (W - gap * 2) / 3
    body, css = [], []
    for i, (val, c1, c2, label) in enumerate(items):
        x = i * (tw + gap)
        d = .2 + i * .15
        num, kf = odometer(x + 36, 168, val.replace("→", "→"), 66, i, d, t)
        css.append(kf)
        body.append(f"""
    <clipPath id="st{i}"><rect x="{x:.1f}" y="0" width="{tw:.1f}" height="{H}" rx="28"/></clipPath>
    <g clip-path="url(#st{i})">
      <rect x="{x:.1f}" y="0" width="{tw:.1f}" height="{H}" fill="{t['bg']}"/>
      <g class="drift-{'abc'[i]}"><ellipse cx="{x + tw * .8:.0f}" cy="40" rx="190" ry="120" fill="url(#orb{i + 1})" opacity=".7"/></g>
      <text x="{x + 36:.1f}" y="64" font-size="14" font-weight="600" class="fg2 fade" style="animation-delay:{d:.2f}s">{esc(label)}</text>
      {num}
      <text x="{x + 36:.1f}" y="226" font-size="17" class="fg fade" style="animation-delay:{d + .6:.2f}s">{esc(c1)}</text>
      <text x="{x + 36:.1f}" y="250" font-size="17" class="fg2 fade" style="animation-delay:{d + .7:.2f}s">{esc(c2)}</text>
    </g>
    <rect x="{x + .5:.1f}" y=".5" width="{tw - 1:.1f}" height="{H - 1}" rx="28" fill="none" stroke="{t['line']}"/>""")
    # no outer tile: three bento tiles
    out = svg(W, H, "86% of reference checks start with no human. Manual ops tasks fell from 116 to 14 a day, turnaround down 31%. 11K+ WhatsApp messages in 10 weeks, about 90% of replies auto-routed.",
              "\n".join(css), "".join(body), t, radius=0)
    return out.replace(f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>', "").replace(
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="0" fill="none" stroke="{t["line"]}"/>', "")


# ---------- project tiles ----------

def browser(x, y, w, img, t, h=None):
    bar = 30
    ratio = 800 / 1280
    ih = h or round(w * ratio)
    dots = "".join(f'<circle cx="{x + 18 + k * 14}" cy="{y + bar / 2}" r="4.5" fill="{c}"/>' for k, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]))
    return f"""
      <rect x="{x + 6}" y="{y + 18}" width="{w}" height="{ih + bar}" rx="14" fill="#000" opacity=".22" filter="url(#soft)"/>
      <clipPath id="b{x}{y}"><rect x="{x}" y="{y}" width="{w}" height="{ih + bar}" rx="14"/></clipPath>
      <g clip-path="url(#b{x}{y})">
        <rect x="{x}" y="{y}" width="{w}" height="{bar}" fill="{t['frame']}"/>{dots}
        <image href="{img}" x="{x}" y="{y + bar}" width="{w}" height="{ih}" preserveAspectRatio="xMidYMin slice"/>
      </g>
      <rect x="{x}" y="{y}" width="{w}" height="{ih + bar}" rx="14" fill="none" stroke="{t['chipline']}"/>"""


def phone(x, y, w, img, t):
    h = round(w * 2.05)
    return f"""
      <rect x="{x + 6}" y="{y + 16}" width="{w}" height="{h}" rx="30" fill="#000" opacity=".28" filter="url(#soft)"/>
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="30" fill="#111"/>
      <clipPath id="p{x}"><rect x="{x + 7}" y="{y + 7}" width="{w - 14}" height="{h - 14}" rx="24"/></clipPath>
      <image href="{img}" x="{x + 7}" y="{y + 7}" width="{w - 14}" height="{h - 14}" preserveAspectRatio="xMidYMin slice" clip-path="url(#p{x})"/>"""


SOFT = '<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter>'


def text_block(x, eyebrow, title, lines, tags, live, t):
    out = [
        f'<text x="{x}" y="92" font-size="14" font-weight="600" class="fg2 fade">{esc(eyebrow)}</text>',
        f'<clipPath id="tt"><rect x="{x}" y="96" width="420" height="68"/></clipPath>',
        f'<g clip-path="url(#tt)"><text x="{x}" y="150" font-size="52" font-weight="700" letter-spacing="-1.8" class="fg rise" style="animation-delay:.1s">{esc(title)}</text></g>',
    ]
    for i, ln in enumerate(lines):
        out.append(f'<text x="{x}" y="{204 + i * 27}" font-size="18" class="fg2 fade" style="animation-delay:{.35 + i * .06:.2f}s">{esc(ln)}</text>')
    ty = 204 + len(lines) * 27 + 22
    cx = x
    for i, tag in enumerate(tags):
        if cx + len(tag) * 12 * .62 + 26 > x + 380:
            cx, ty = x, ty + 38
        p, w = pill(cx, ty, tag, t, size=12)
        out.append(f'<g class="fade" style="animation-delay:{.6 + i * .06:.2f}s">{p}</g>')
        cx += w + 8
    out.append(f'<text x="{x}" y="{ty + 78}" font-size="17" font-weight="600" fill="url(#grad)" class="fade" style="animation-delay:.9s">{esc(live)}</text>')
    return "".join(out)


def project_pawse(t):
    W, H = 1000, 500
    shot = jpeg_b64("pawse.png", 1040)
    events = [("play · 00:14:32", 560, 400, "c", .0), ("synced · 2 viewers", 820, 84, "b", .3), ("seek → 01:02:10", 900, 330, "a", .6)]
    chips = []
    for label, x, y, layer, d in events:
        p, w = pill(x - 60, y, label, t, size=12, accent=label.startswith("synced"))
        chips.append(f'<g class="drift-{layer}"><g class="fade" style="animation-delay:{1.1 + d:.2f}s">{p}</g></g>')
    body = f"""
    <defs>{SOFT}</defs>
    <g class="drift-a"><rect x="-40" y="-40" width="{W + 80}" height="{H + 80}" fill="url(#dots)"/></g>
    <g class="drift-b"><ellipse cx="760" cy="260" rx="330" ry="240" fill="url(#orb2)"/></g>
    {text_block(56, "Personal product · live", "Pawse", ["Watch movies together from two places,", "in sync. Play, pause and seek travel over", "a WebSocket relay; your own movie file", "goes peer to peer over WebRTC."], ["WebSocket", "WebRTC", "React", "Node.js", "Chrome MV3"], "pawsetv.vercel.app ↗", t)}
    <g class="drift-c"><g class="fade" style="animation-delay:.4s">{browser(470, 110, 500, shot, t)}</g></g>
    {''.join(chips)}
    """
    return svg(W, H, "Pawse: watch movies together from two places, in sync. WebSocket relay and WebRTC peer-to-peer file transfer.", "", body, t)


def project_bowl(t):
    W, H = 1000, 500
    desk = jpeg_b64("bns-desktop.png", 960)
    mob = jpeg_b64("bns-mobile.png", 260)
    body = f"""
    <defs>{SOFT}</defs>
    <g class="drift-a"><rect x="-40" y="-40" width="{W + 80}" height="{H + 80}" fill="url(#dots)"/></g>
    <g class="drift-b"><ellipse cx="780" cy="240" rx="330" ry="240" fill="url(#orb3)"/></g>
    {text_block(56, "Freelance client · live", "Bowl n Sticks", ["QR menu and admin panel for a cafe.", "Owners edit dishes, photos and order", "themselves; Row Level Security decides", "who can write. 83 tests on the actions."], ["Next.js 16", "Supabase", "Postgres RLS", "dnd-kit"], "bowl-n-sticks.vercel.app ↗", t)}
    <g class="drift-a"><g class="fade" style="animation-delay:.4s">{browser(470, 96, 480, desk, t)}</g></g>
    <g class="drift-c"><g class="fade" style="animation-delay:.7s">{phone(830, 210, 130, mob, t)}</g></g>
    """
    return svg(W, H, "Bowl n Sticks: QR menu and admin panel for a cafe. Next.js, Supabase, Postgres Row Level Security.", "", body, t)


# ---------- stack marquee (two speeds = parallax) ----------

def stack(t):
    W, H = 1000, 176
    rows = [
        ["Node.js", "TypeScript", "BullMQ", "Redis", "MySQL", "PostgreSQL", "AWS Bedrock", "SES", "Webhooks"],
        ["React", "Next.js", "Supabase", "WebSockets", "WebRTC", "Express", "MongoDB", "Tailwind", "Vitest"],
    ]
    body, css = [], []
    for r, words in enumerate(rows):
        size = 40 if r == 0 else 26
        y = 78 if r == 0 else 136
        sep = "   ·   "
        line = sep.join(words) + sep
        est = len(line) * size * (.52 if r == 0 else .5)
        name = f"m{r}"
        dur = 46 if r == 0 else 30
        direction = "-" if r == 0 else ""
        css.append(f"@keyframes {name} {{ from {{ transform: translateX({'0' if r == 0 else f'-{est:.0f}px'}); }} to {{ transform: translateX({f'-{est:.0f}px' if r == 0 else '0'}); }} }}")
        cls = "fg" if r == 0 else "fg3"
        weight = 700 if r == 0 else 500
        copies = "".join(
            f'<text x="{k * est:.0f}" y="{y}" font-size="{size}" font-weight="{weight}" class="{cls}" textLength="{est:.0f}" lengthAdjust="spacing" xml:space="preserve">{esc(line)}</text>'
            for k in range(3)
        )
        body.append(f'<g style="animation:{name} {dur}s linear infinite">{copies}</g>')
    mask = f"""
    <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".1" stop-color="#fff"/><stop offset=".9" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <mask id="fade"><rect width="{W}" height="{H}" fill="url(#edge)"/></mask>"""
    inner = f'<defs>{mask}</defs><g mask="url(#fade)">{"".join(body)}</g>'
    return svg(W, H, "Stack: Node.js, TypeScript, BullMQ, Redis, MySQL, PostgreSQL, AWS Bedrock, SES, React, Next.js, Supabase, WebSockets, WebRTC.", "\n".join(css), inner, t)


TILES = {"hero": hero, "stats": stats, "pawse": project_pawse, "bowl": project_bowl, "stack": stack}

if __name__ == "__main__":
    for name, fn in TILES.items():
        for theme, t in THEMES.items():
            path = OUT / f"{name}-{theme}.svg"
            path.write_text(fn(t), encoding="utf-8")
            print(f"{path.relative_to(ROOT)}  {path.stat().st_size // 1024} KB")
