"""Builds the animated SVG tiles for the profile README.

Run from the repo root: python scripts/build.py
Writes assets/<tile>-dark.svg and assets/<tile>-light.svg.

GitHub strips JS and CSS from READMEs, but CSS inside an SVG served as an
image still animates. Design rules follow Apple's system (awesome-design-md):
600-weight display type with tight tracking, one accent family, tiles that
alternate dark and light canvases, a single shadow under product imagery.
Motion durations follow the transitions.dev token scale. Every tile honours
prefers-reduced-motion.
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

# motion tokens (transitions.dev scale)
EASE = "cubic-bezier(.22,1,.36,1)"  # --ease-smooth-out
REVEAL = ".5s"  # --duration-very-slow: text reveal
STAGGER = .04  # --duration-stagger
MICRO = .08  # --duration-micro: few large items

DARK_TEXT = dict(fg="#f5f5f7", fg2="#a1a1a6", fg3="#6e6e73", line="#ffffff1a", chip="#ffffff12", chipline="#ffffff24",
                 frame="#2a2a2c", g1="#2997ff", g2="#7d7aff", g3="#bf5af2", glow=.42, dots=.08)
LIGHT_TEXT = dict(fg="#1d1d1f", fg2="#6e6e73", fg3="#86868b", line="#0000000f", chip="#ffffff", chipline="#00000014",
                  frame="#e8e8ed", g1="#0066cc", g2="#5e5ce6", g3="#af52de", glow=.22, dots=.07)

SURFACES = {
    "black": dict(bg="#000000", **DARK_TEXT),
    "graphite": dict(bg="#161617", **DARK_TEXT),
    "parchment": dict(bg="#f5f5f7", **LIGHT_TEXT),
}

# tile order in the README alternates canvases; the colour change is the divider
LAYOUT = {
    "light": {"hero": "black", "stats": "parchment", "pawse": "black", "bowl": "parchment", "timeline": "black", "stack": "parchment"},
    "dark": {"hero": "black", "stats": "graphite", "pawse": "black", "bowl": "graphite", "timeline": "black", "stack": "graphite"},
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def jpeg_b64(name, width):
    img = Image.open(SRC / name).convert("RGB")
    h = round(img.height * width / img.width)
    img = img.resize((width, h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=76, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def base_css(s):
    return f"""
    text {{ font-family: {FONT}; }}
    .mono {{ font-family: {MONO}; }}
    .fg {{ fill: {s['fg']}; }} .fg2 {{ fill: {s['fg2']}; }} .fg3 {{ fill: {s['fg3']}; }}
    .rise {{ transform-box: fill-box; animation: rise {REVEAL} {EASE} both; }}
    .fade {{ transform-box: fill-box; animation: reveal {REVEAL} ease-in-out both; }}
    .draw {{ animation: draw 1.2s {EASE} both; }}
    .drift-a {{ animation: drift-a 16s ease-in-out infinite alternate; }}
    .drift-b {{ animation: drift-b 11s ease-in-out infinite alternate; }}
    .drift-c {{ animation: drift-c 8s ease-in-out infinite alternate; }}
    @keyframes rise {{ from {{ transform: translateY(105%); filter: blur(3px); }} to {{ transform: none; filter: blur(0); }} }}
    @keyframes reveal {{ from {{ opacity: 0; transform: translateY(12px); filter: blur(3px); }} to {{ opacity: 1; transform: none; filter: blur(0); }} }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    @keyframes drift-a {{ from {{ transform: translate(0, 0); }} to {{ transform: translate(-12px, 6px); }} }}
    @keyframes drift-b {{ from {{ transform: translate(0, 0); }} to {{ transform: translate(18px, -10px); }} }}
    @keyframes drift-c {{ from {{ transform: translate(0, 0); }} to {{ transform: translate(-6px, -8px); }} }}
    """


REDUCED = """
    @media (prefers-reduced-motion: reduce) {
      * { animation: none !important; }
      .draw { stroke-dashoffset: 0 !important; }
      .loop { display: none; }
    }
"""


def defs(s, w):
    return f"""
    <linearGradient id="grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{s['g1']}"/><stop offset=".55" stop-color="{s['g2']}"/><stop offset="1" stop-color="{s['g3']}"/>
    </linearGradient>
    <linearGradient id="gline" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="0">
      <stop offset="0" stop-color="{s['g1']}"/><stop offset=".55" stop-color="{s['g2']}"/><stop offset="1" stop-color="{s['g3']}"/>
    </linearGradient>
    <radialGradient id="orb1"><stop offset="0" stop-color="{s['g1']}" stop-opacity="{s['glow']}"/><stop offset="1" stop-color="{s['g1']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="orb2"><stop offset="0" stop-color="{s['g3']}" stop-opacity="{s['glow']}"/><stop offset="1" stop-color="{s['g3']}" stop-opacity="0"/></radialGradient>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{s['fg']}" fill-opacity="{s['dots']}"/></pattern>
    <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="15"/></filter>"""


def svg(w, h, label, css, body, s, radius=18, tile=True):
    clip = f'<clipPath id="tile"><rect width="{w}" height="{h}" rx="{radius}"/></clipPath>' if tile else ""
    open_g = '<g clip-path="url(#tile)">' if tile else "<g>"
    bg = f'<rect width="{w}" height="{h}" fill="{s["bg"]}"/>' if tile else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">
  <style>{base_css(s)}{css}{REDUCED}</style>
  <defs>{defs(s, w)}{clip}</defs>
  {open_g}
    {bg}
{body}
  </g>
</svg>
"""


def pill(x, y, text, s, size=13, accent=False):
    w = len(text) * size * .62 + 26
    h = size + 16
    stroke = "url(#gline)" if accent else s["chipline"]
    return (
        f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{s["chip"]}" stroke="{stroke}"/>'
        f'<text x="{x + w / 2:.0f}" y="{y + h / 2 + size * .36:.1f}" text-anchor="middle" font-size="{size}" class="mono fg">{esc(text)}</text>',
        w,
    )


def delay(d):
    return f'style="animation-delay:{d:.2f}s"'


# ---------- hero ----------

def hero(s):
    W, H = 1000, 520
    lines = [("I turn manual ops work", False), ("into automated pipelines.", True)]
    head = []
    for i, (txt, grad) in enumerate(lines):
        y = 214 + i * 72
        paint = 'fill="url(#grad)" class="rise"' if grad else 'class="fg rise"'
        head.append(
            f'<clipPath id="l{i}"><rect x="0" y="{y - 62}" width="{W}" height="82"/></clipPath>'
            f'<g clip-path="url(#l{i})"><text x="64" y="{y}" font-size="62" font-weight="600" letter-spacing="-1.4" {paint} {delay(.1 + i * MICRO)}>{txt}</text></g>'
        )
    # a light sheen travels across the gradient line every few seconds
    sheen = f"""
    <clipPath id="sheenclip"><text x="64" y="286" font-size="62" font-weight="600" letter-spacing="-1.4">into automated pipelines.</text></clipPath>
    <g clip-path="url(#sheenclip)" class="loop"><rect x="-200" y="200" width="140" height="110" fill="#ffffff" opacity=".35" style="animation: sheen 7s {EASE} 1.2s infinite both"/></g>"""

    nodes = ["inbound", "queue", "llm", "action", "done"]
    x0, x1, py = 64, 936, 436
    step = (x1 - x0) / (len(nodes) - 1)
    chips = []
    for i, n in enumerate(nodes):
        cx = x0 + i * step
        w = len(n) * 13 * .62 + 26
        x = min(max(cx - w / 2, x0), x1 - w)
        p, _ = pill(x, py - 14, n, s, accent=(n == "done"))
        chips.append(f'<g class="fade" {delay(.55 + i * STAGGER)}>{p}</g>')

    body = f"""
    <g class="drift-a"><rect x="-40" y="-40" width="{W + 80}" height="{H + 80}" fill="url(#dots)"/></g>
    <g class="drift-b"><ellipse cx="830" cy="110" rx="380" ry="260" fill="url(#orb1)"/></g>
    <g class="drift-c"><ellipse cx="620" cy="460" rx="320" ry="190" fill="url(#orb2)"/></g>

    <g class="fade">
      <text x="64" y="94" font-size="21" font-weight="600" class="fg" letter-spacing="-.2">Pradumya Gaurav</text>
      <text x="64" y="122" font-size="15" class="fg2" letter-spacing="-.2">Backend engineer · Node.js, queues, LLMs · Bengaluru</text>
    </g>
    {''.join(head)}
    {sheen}
    <text x="64" y="352" font-size="19" class="fg2 fade" letter-spacing="-.3" {delay(.3)}>Production systems where the busywork runs itself, and people only see what needs a human.</text>

    <path d="M{x0} {py}H{x1}" stroke="url(#gline)" stroke-width="1.5" stroke-dasharray="{x1 - x0}" stroke-dashoffset="{x1 - x0}" class="draw" {delay(.45)}/>
    <g class="loop"><circle cx="{x0}" cy="{py}" r="4" fill="{s['g1']}" style="animation: pulse 4.2s {EASE} 1.6s infinite both"/></g>
    {''.join(chips)}
    """
    css = f"""
    @keyframes pulse {{ 0% {{ transform: translateX(0); opacity: 0; }} 6% {{ opacity: 1; }} 70% {{ transform: translateX({x1 - x0}px); opacity: 1; }} 76%, 100% {{ transform: translateX({x1 - x0}px); opacity: 0; }} }}
    @keyframes sheen {{ 0% {{ transform: skewX(-20deg) translateX(0); }} 30%, 100% {{ transform: skewX(-20deg) translateX(1100px); }} }}
    """
    return svg(W, H, "Pradumya Gaurav. Backend engineer. I turn manual ops work into automated pipelines.", css, body, s)


# ---------- stats (odometer roll) ----------

ADV = {"d": .6, "%": .86, "+": .62, "K": .66, "→": 1.05, " ": .26}


def odometer(x, y, value, size, uid, d0, s):
    out, css, cx = [], [], x
    lh = size * 1.1
    fill = f'fill="url(#ng{uid})"'
    out.append(
        f'<linearGradient id="ng{uid}" gradientUnits="userSpaceOnUse" x1="{x}" y1="0" x2="{x + size * len(value) * .62:.0f}" y2="0">'
        f'<stop offset="0" stop-color="{s["g1"]}"/><stop offset=".55" stop-color="{s["g2"]}"/><stop offset="1" stop-color="{s["g3"]}"/></linearGradient>'
    )
    for i, ch in enumerate(value):
        adv = size * ADV.get("d" if ch.isdigit() else ch, .6)
        mid = cx + adv / 2
        if ch.isdigit():
            target = int(ch)
            seq = list(range(10)) + list(range(target + 1))
            steps = len(seq) - 1
            name = f"r{uid}_{i}"
            css.append(
                f"@keyframes {name} {{ from {{ transform: translateY(0); filter: blur(2px); }} 85% {{ filter: blur(0); }} to {{ transform: translateY(-{steps * lh:.1f}px); filter: blur(0); }} }}"
            )
            col = "".join(
                f'<text x="{mid:.1f}" y="{y + k * lh:.1f}" text-anchor="middle" font-size="{size}" font-weight="600" letter-spacing="-1" {fill}>{dgt}</text>'
                for k, dgt in enumerate(seq)
            )
            out.append(
                f'<g clip-path="url(#clip{uid})"><g style="animation:{name} {1.0 + i * STAGGER * 2:.2f}s {EASE} {d0:.2f}s both; transform: translateY(-{steps * lh:.1f}px)">{col}</g></g>'
            )
        elif ch != " ":
            out.append(
                f'<text x="{mid:.1f}" y="{y}" text-anchor="middle" font-size="{size}" font-weight="600" {fill} class="fade" {delay(d0 + .3)}>{esc(ch)}</text>'
            )
        cx += adv
    clip = f'<clipPath id="clip{uid}"><rect x="{x - 10}" y="{y - size}" width="{cx - x + 20:.0f}" height="{size * 1.28:.0f}"/></clipPath>'
    return clip + "".join(out), "\n".join(css)


def stats(s):
    W, H = 1000, 280
    items = [
        ("86%", "of reference checks now start", "with no human involved", "Reference-check automation"),
        ("116→14", "manual ops tasks a day,", "turnaround down 31%", "Same system, before vs after"),
        ("11K+", "WhatsApp messages in 10 weeks,", "~90% of replies auto-routed", "Meta Cloud API, built in-house"),
    ]
    gap = 16
    tw = (W - gap * 2) / 3
    body, css = [], []
    for i, (val, c1, c2, label) in enumerate(items):
        x = i * (tw + gap)
        d = .1 + i * MICRO
        num, kf = odometer(x + 32, 160, val, 64, i, d, s)
        css.append(kf)
        body.append(f"""
    <rect x="{x:.1f}" y="0" width="{tw:.1f}" height="{H}" rx="18" fill="{s['bg']}"/>
    <text x="{x + 32:.1f}" y="60" font-size="14" font-weight="600" letter-spacing="-.2" class="fg2 fade" {delay(d)}>{esc(label)}</text>
    {num}
    <text x="{x + 32:.1f}" y="214" font-size="17" letter-spacing="-.35" class="fg fade" {delay(d + .35)}>{esc(c1)}</text>
    <text x="{x + 32:.1f}" y="239" font-size="17" letter-spacing="-.35" class="fg2 fade" {delay(d + .35 + STAGGER)}>{esc(c2)}</text>""")
    return svg(W, H, "86% of reference checks start with no human. Manual ops tasks fell from 116 to 14 a day, turnaround down 31%. 11K+ WhatsApp messages in 10 weeks, about 90% of replies auto-routed.",
               "\n".join(css), "".join(body), s, tile=False)


# ---------- project tiles ----------

def browser(x, y, w, img, s):
    bar = 28
    ih = round(w * 800 / 1280)
    dots = "".join(f'<circle cx="{x + 18 + k * 14}" cy="{y + bar / 2}" r="4.5" fill="{c}"/>' for k, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]))
    return f"""
      <rect x="{x + 3}" y="{y + 10}" width="{w}" height="{ih + bar}" rx="12" fill="#000" opacity=".3" filter="url(#soft)"/>
      <clipPath id="b{x}{y}"><rect x="{x}" y="{y}" width="{w}" height="{ih + bar}" rx="12"/></clipPath>
      <g clip-path="url(#b{x}{y})">
        <rect x="{x}" y="{y}" width="{w}" height="{bar}" fill="{s['frame']}"/>{dots}
        <image href="{img}" x="{x}" y="{y + bar}" width="{w}" height="{ih}" preserveAspectRatio="xMidYMin slice"/>
      </g>
      <rect x="{x}" y="{y}" width="{w}" height="{ih + bar}" rx="12" fill="none" stroke="{s['chipline']}"/>"""


def phone(x, y, w, img):
    h = round(w * 2.05)
    return f"""
      <rect x="{x + 3}" y="{y + 10}" width="{w}" height="{h}" rx="28" fill="#000" opacity=".35" filter="url(#soft)"/>
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" fill="#1d1d1f"/>
      <clipPath id="p{x}"><rect x="{x + 6}" y="{y + 6}" width="{w - 12}" height="{h - 12}" rx="22"/></clipPath>
      <image href="{img}" x="{x + 6}" y="{y + 6}" width="{w - 12}" height="{h - 12}" preserveAspectRatio="xMidYMin slice" clip-path="url(#p{x})"/>"""


def text_block(x, eyebrow, title, lines, tags, live, s):
    out = [
        f'<text x="{x}" y="92" font-size="14" font-weight="600" letter-spacing="-.2" fill="{s["g1"]}" class="fade">{esc(eyebrow)}</text>',
        f'<clipPath id="tt"><rect x="{x}" y="98" width="430" height="64"/></clipPath>',
        f'<g clip-path="url(#tt)"><text x="{x}" y="148" font-size="48" font-weight="600" letter-spacing="-1.2" class="fg rise" {delay(MICRO)}>{esc(title)}</text></g>',
    ]
    for i, ln in enumerate(lines):
        out.append(f'<text x="{x}" y="{200 + i * 25}" font-size="17" letter-spacing="-.35" class="fg2 fade" {delay(.2 + i * STAGGER)}>{esc(ln)}</text>')
    ty = 200 + len(lines) * 25 + 20
    cx = x
    for i, tag in enumerate(tags):
        if cx + len(tag) * 12 * .62 + 26 > x + 380:
            cx, ty = x, ty + 36
        p, w = pill(cx, ty, tag, s, size=12)
        out.append(f'<g class="fade" {delay(.35 + i * STAGGER)}>{p}</g>')
        cx += w + 8
    out.append(f'<text x="{x}" y="{ty + 74}" font-size="17" letter-spacing="-.35" fill="{s["g1"]}" class="fade" {delay(.5)}>{esc(live)} ›</text>')
    return "".join(out)


def project_pawse(s):
    W, H = 1000, 480
    shot = jpeg_b64("pawse.png", 1040)
    events = [("play · 00:14:32", 560, 392, "c"), ("synced · 2 viewers", 820, 78, "b"), ("seek → 01:02:10", 900, 322, "a")]
    chips = []
    for i, (label, x, y, layer) in enumerate(events):
        p, _ = pill(x - 60, y, label, s, size=12, accent=label.startswith("synced"))
        chips.append(f'<g class="drift-{layer}"><g class="fade" {delay(.6 + i * MICRO)}>{p}</g></g>')
    body = f"""
    {text_block(56, "Personal product", "Pawse", ["Watch movies together from two places,", "in sync. Play, pause and seek travel over", "a WebSocket relay; your own movie file", "goes peer to peer over WebRTC."], ["WebSocket", "WebRTC", "React", "Node.js", "Chrome MV3"], "pawsetv.vercel.app", s)}
    <g class="drift-c"><g class="fade" {delay(.25)}>{browser(470, 104, 500, shot, s)}</g></g>
    {''.join(chips)}
    """
    return svg(W, H, "Pawse: watch movies together from two places, in sync. WebSocket relay and WebRTC peer-to-peer file transfer.", "", body, s)


def project_bowl(s):
    W, H = 1000, 480
    desk = jpeg_b64("bns-desktop.png", 960)
    mob = jpeg_b64("bns-mobile.png", 260)
    body = f"""
    {text_block(56, "Freelance client", "Bowl n Sticks", ["QR menu and admin panel for a cafe.", "Owners edit dishes, photos and order", "themselves; Row Level Security decides", "who can write. 83 tests on the actions."], ["Next.js 16", "Supabase", "Postgres RLS", "dnd-kit"], "bowl-n-sticks.vercel.app", s)}
    <g class="drift-a"><g class="fade" {delay(.25)}>{browser(470, 92, 480, desk, s)}</g></g>
    <g class="drift-c"><g class="fade" {delay(.25 + MICRO)}>{phone(832, 200, 128, mob)}</g></g>
    """
    return svg(W, H, "Bowl n Sticks: QR menu and admin panel for a cafe. Next.js, Supabase, Postgres Row Level Security.", "", body, s)


# ---------- timeline ----------

def timeline(s):
    W, H = 1000, 300
    stops = [
        ("2025", "GetMax Solutions", ["Built getmaxhealthcare.com end to end", "and internal tools for US healthcare ops."]),
        ("2026", "SpringWorks · SDE-1", ["Backend automation: queues, LLM routing,", "WhatsApp Cloud API. 148 merged PRs."]),
        ("Now", "Open to remote", ["Shipping side projects in public and", "contributing to open source."]),
    ]
    x0, x1, ly = 64, 936, 128
    col = (x1 - x0) / len(stops)
    body = [
        '<text x="64" y="72" font-size="14" font-weight="600" letter-spacing="-.2" class="fg2 fade">Experience</text>',
        f'<path d="M{x0} {ly}H{x1}" stroke="{s["line"]}" stroke-width="1.5"/>',
        f'<path d="M{x0} {ly}H{x1}" stroke="url(#gline)" stroke-width="1.5" stroke-dasharray="{x1 - x0}" stroke-dashoffset="{x1 - x0}" class="draw" {delay(.1)}/>',
    ]
    for i, (year, org, lines) in enumerate(stops):
        x = x0 + i * col
        d = .2 + i * MICRO * 2
        now = year == "Now"
        ring = s["g3"] if now else s["g1"]
        body.append(f'<g class="fade" {delay(d)}>')
        body.append(f'<circle cx="{x + 6}" cy="{ly}" r="6" fill="{s["bg"]}" stroke="{ring}" stroke-width="2"/>')
        if now:
            body.append(f'<circle cx="{x + 6}" cy="{ly}" r="6" fill="none" stroke="{ring}" class="loop" style="transform-box: fill-box; transform-origin: center; animation: ping 2.4s ease-out 1.2s infinite"/>')
        body.append(f'<text x="{x}" y="{ly + 52}" font-size="32" font-weight="600" letter-spacing="-.8" class="fg">{year}</text>')
        body.append(f'<text x="{x}" y="{ly + 84}" font-size="17" font-weight="600" letter-spacing="-.35" class="fg">{esc(org)}</text>')
        for k, ln in enumerate(lines):
            body.append(f'<text x="{x}" y="{ly + 112 + k * 23}" font-size="15" letter-spacing="-.25" class="fg2">{esc(ln)}</text>')
        body.append("</g>")
    css = "@keyframes ping { from { transform: scale(1); opacity: .9; } to { transform: scale(2.6); opacity: 0; } }"
    return svg(W, H, "Experience: 2025 GetMax Solutions, built getmaxhealthcare.com. 2026 SpringWorks, SDE-1, backend automation, 148 merged PRs. Now open to remote.", css, "".join(body), s)


# ---------- stack marquee (two speeds = parallax) ----------

def stack(s):
    W, H = 1000, 168
    rows = [
        ["Node.js", "TypeScript", "BullMQ", "Redis", "MySQL", "PostgreSQL", "AWS Bedrock", "SES", "Webhooks"],
        ["React", "Next.js", "Supabase", "WebSockets", "WebRTC", "Express", "MongoDB", "Tailwind", "Vitest"],
    ]
    body, css = [], []
    for r, words in enumerate(rows):
        size = 40 if r == 0 else 24
        y = 76 if r == 0 else 128
        sep = "   ·   "
        line = sep.join(words) + sep
        est = len(line) * size * (.455 if r == 0 else .44)
        name = f"m{r}"
        dur = 50 if r == 0 else 32
        frm, to = ("0", f"-{est:.0f}px") if r == 0 else (f"-{est:.0f}px", "0")
        css.append(f"@keyframes {name} {{ from {{ transform: translateX({frm}); }} to {{ transform: translateX({to}); }} }}")
        cls = "fg" if r == 0 else "fg3"
        weight = 600 if r == 0 else 400
        copies = "".join(
            f'<text x="{k * est:.0f}" y="{y}" font-size="{size}" font-weight="{weight}" class="{cls}" textLength="{est:.0f}" lengthAdjust="spacing" xml:space="preserve">{esc(line)}</text>'
            for k in range(3)
        )
        body.append(f'<g style="animation:{name} {dur}s linear infinite">{copies}</g>')
    mask = f"""
    <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".1" stop-color="#fff"/><stop offset=".9" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <mask id="fadeedge"><rect width="{W}" height="{H}" fill="url(#edge)"/></mask>"""
    inner = f'<defs>{mask}</defs><g mask="url(#fadeedge)">{"".join(body)}</g>'
    return svg(W, H, "Stack: Node.js, TypeScript, BullMQ, Redis, MySQL, PostgreSQL, AWS Bedrock, SES, React, Next.js, Supabase, WebSockets, WebRTC.", "\n".join(css), inner, s)


TILES = {"hero": hero, "stats": stats, "pawse": project_pawse, "bowl": project_bowl, "timeline": timeline, "stack": stack}

if __name__ == "__main__":
    for theme, layout in LAYOUT.items():
        for name, fn in TILES.items():
            path = OUT / f"{name}-{theme}.svg"
            path.write_text(fn(SURFACES[layout[name]]), encoding="utf-8")
            print(f"{path.relative_to(ROOT)}  {path.stat().st_size // 1024} KB")
