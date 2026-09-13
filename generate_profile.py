#!/usr/bin/env python3
"""Generate the BIOCOMPUTE//MUSA GitHub profile artwork.

The profile behaves like a living neural interface: midnight navy, binary cyan,
electric blue, ice highlights, scan lines, neural traces, and asymmetric
instrument layouts. Fonts are embedded for consistent rendering on GitHub.
"""

import base64
from html import escape
from pathlib import Path


HERE = Path(__file__).parent
FONTS = HERE / "fonts"

# --------------------------------------------------------------- BRAND / COPY
NAME = "MUSA//004"
EYEBROW = "BIO-COMPUTE LAB / HUMAN NODE 004"
TAGLINE = "I TEACH APPS TO THINK"
DESC = "Agents that act. RAG that remembers. Mobile experiences that feel alive."
STATUS = "SPECIMEN AWAKE"

STATS = [
    ("10+", "APPS RELEASED"),
    ("10K+", "HUMANS REACHED"),
    ("5+", "MODELS TRAINED"),
    ("03", "YEARS EXPLORING"),
]

THEMES = {
    "dark": {
        "bg": "#050A10", "surface": "#0A121C", "display": "#EAFBFF",
        "primary": "#BCD7E2", "secondary": "#6D8A99", "border": "#214256",
        "grid": "#0E2532", "cyan": "#66F7FF", "violet": "#29A9FF",
        "pink": "#8B7CFF", "lime": "#D5F7FF",
    },
    "light": {
        "bg": "#F2F8FA", "surface": "#E8F2F6", "display": "#07121B",
        "primary": "#294A59", "secondary": "#668491", "border": "#A9C6D2",
        "grid": "#D5E7ED", "cyan": "#007F8C", "violet": "#006ECB",
        "pink": "#6653D4", "lime": "#1298AB",
    },
}

SM = "'Space Mono', monospace"
SG = "'Space Grotesk', sans-serif"
DOTO = "'Doto', 'Space Mono', monospace"


def _b64(filename):
    return base64.b64encode((FONTS / filename).read_bytes()).decode()


def font_faces():
    faces = [
        ("Doto", "100 900", "Doto-var.woff2"),
        ("Space Grotesk", "400", "SpaceGrotesk-400.woff2"),
        ("Space Grotesk", "500", "SpaceGrotesk-500.woff2"),
        ("Space Mono", "400", "SpaceMono-400.woff2"),
    ]
    return "\n".join(
        f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};"
        f"src:url(data:font/woff2;base64,{_b64(filename)}) format('woff2');}}"
        for family, weight, filename in faces
    )


def defs(c, prefix="n"):
    return f"""
<defs>
  <style>{font_faces()}</style>
  <linearGradient id="{prefix}-signal" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{c['cyan']}"/>
    <stop offset="0.52" stop-color="{c['violet']}"/>
    <stop offset="1" stop-color="{c['pink']}"/>
  </linearGradient>
  <radialGradient id="{prefix}-aura">
    <stop offset="0" stop-color="{c['violet']}" stop-opacity=".16"/>
    <stop offset="1" stop-color="{c['violet']}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="{prefix}-grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="{c['grid']}" stroke-width="1"/>
    <circle cx="1" cy="1" r="1" fill="{c['border']}"/>
  </pattern>
  <pattern id="{prefix}-scan" width="8" height="8" patternUnits="userSpaceOnUse">
    <path d="M0 7.5H8" stroke="{c['grid']}" stroke-width="1"/>
  </pattern>
  <filter id="{prefix}-glow" x="-80%" y="-80%" width="260%" height="260%">
    <feGaussianBlur stdDeviation="4" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>"""


def frame(width, height, c):
    return (
        f'<path d="M18 58V18H72 M{width-90} 18h72v40 M18 {height-58}v40h54 '
        f'M{width-90} {height-18}h72v-40" fill="none" stroke="{c["border"]}" stroke-width="1.3"/>'
        f'<path d="M82 18h6m8 0h18m8 0h3 M{width-126} {height-18}h-6m-8 0h-18m-8 0h-3" '
        f'stroke="{c["cyan"]}" stroke-width="2"/>'
    )


def neural_map(c):
    nodes = [
        (742, 86, 6, "cyan"), (843, 68, 4, "pink"),
        (912, 124, 7, "violet"), (792, 158, 10, "violet"),
        (885, 202, 5, "cyan"), (736, 230, 4, "pink"),
        (944, 246, 4, "pink"), (826, 274, 7, "cyan"),
    ]
    edges = [(0, 1), (0, 3), (1, 2), (1, 3), (2, 4), (3, 4),
             (3, 5), (3, 7), (4, 6), (4, 7), (5, 7), (6, 7)]
    out = [
        '<circle cx="835" cy="174" r="170" fill="url(#hero-aura)"/>',
        f'<path d="M724 131C742 72 801 48 858 62C921 77 954 126 946 184C938 245 888 282 827 280C765 278 715 235 716 178C716 160 719 145 724 131Z" fill="none" stroke="{c["border"]}" stroke-width="1.2"/>',
        f'<path d="M744 142C757 96 804 76 851 87C897 98 927 136 919 181C912 226 874 253 828 251C783 249 745 218 740 178C738 164 740 152 744 142Z" fill="none" stroke="{c["violet"]}" stroke-opacity=".45" stroke-dasharray="4 9">'
        '<animate attributeName="stroke-dashoffset" values="26;0" dur="3s" repeatCount="indefinite"/></path>',
        f'<path d="M766 149C776 119 809 103 841 111C876 120 897 147 891 180C885 214 856 233 823 226C791 219 766 193 763 167C762 160 763 154 766 149Z" fill="none" stroke="{c["cyan"]}" stroke-opacity=".55"/>',
        f'<path d="M694 174H970 M835 48V288" stroke="{c["border"]}" stroke-width=".8" stroke-dasharray="3 8"/>',
        f'<rect x="704" y="76" width="260" height="2" fill="{c["cyan"]}" opacity=".5">'
        '<animate attributeName="y" values="76;270;76" dur="4.4s" repeatCount="indefinite"/></rect>',
        f'<text x="712" y="68" font-family="{SM}" font-size="8" letter-spacing="1.4" fill="{c["secondary"]}">CORTEX SCAN / 004</text>',
        f'<text x="958" y="284" text-anchor="end" font-family="{SM}" font-size="8" letter-spacing="1.2" fill="{c["secondary"]}">08 SYNAPSES / LIVE</text>',
    ]
    for a, b in edges:
        x1, y1, _, _ = nodes[a]
        x2, y2, _, _ = nodes[b]
        out.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{c["border"]}" stroke-width="1.3"/>')
    out.append(
        '<path d="M742 86L792 158L885 202L826 274" fill="none" stroke="url(#hero-signal)" '
        'stroke-width="2" stroke-dasharray="8 10" filter="url(#hero-glow)">'
        '<animate attributeName="stroke-dashoffset" values="36;0" dur="1.6s" repeatCount="indefinite"/></path>'
    )
    for index, (x, y, radius, color) in enumerate(nodes):
        out.append(
            f'<circle cx="{x}" cy="{y}" r="{radius + 5}" fill="{c[color]}" opacity=".08">'
            f'<animate attributeName="r" values="{radius+3};{radius+10};{radius+3}" dur="{2.0+index*.18:.2f}s" repeatCount="indefinite"/></circle>'
        )
        out.append(
            f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{c[color]}" filter="url(#hero-glow)">'
            f'<animate attributeName="opacity" values="1;.35;1" dur="{1.4+index*.16:.2f}s" repeatCount="indefinite"/></circle>'
        )
    out.append(
        f'<text x="835" y="177" text-anchor="middle" font-family="{SM}" font-size="9" '
        f'letter-spacing="1.6" fill="{c["display"]}">LIVE CORTEX 004</text>'
    )
    return "\n".join(out)


def render(c):
    width, height = 1000, 390
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        defs(c, "hero"),
        f'<rect width="{width}" height="{height}" fill="{c["bg"]}"/>',
        '<rect width="1000" height="390" fill="url(#hero-grid)" opacity=".8"/>',
        '<rect width="1000" height="390" fill="url(#hero-scan)" opacity=".28"/>',
        frame(width, height, c), neural_map(c),
        f'<text x="54" y="49" font-family="{SM}" font-size="11" letter-spacing="2.4" fill="{c["secondary"]}">{escape(EYEBROW)}</text>',
        f'<circle cx="784" cy="44" r="4" fill="{c["lime"]}" filter="url(#hero-glow)"><animate attributeName="opacity" values="1;.25;1" dur="1.3s" repeatCount="indefinite"/></circle>',
        f'<text x="798" y="49" font-family="{SM}" font-size="11" letter-spacing="1.5" fill="{c["secondary"]}">{escape(STATUS)}</text>',
        f'<text x="50" y="135" font-family="{DOTO}" font-size="76" font-weight="700" letter-spacing="1" fill="url(#hero-signal)">{escape(NAME)}</text>',
        f'<text x="54" y="176" font-family="{SM}" font-size="15" letter-spacing="3" fill="{c["display"]}">{escape(TAGLINE)}</text>',
        f'<text x="54" y="207" font-family="{SG}" font-size="16" fill="{c["primary"]}">{escape(DESC)}</text>',
        f'<text x="54" y="238" font-family="{SM}" font-size="10" letter-spacing="1.5" fill="{c["secondary"]}">UNSTABLE BY DESIGN / USEFUL ON PURPOSE</text>',
        '<line x1="54" y1="276" x2="946" y2="276" stroke="url(#hero-signal)" stroke-width="1.5"/>',
    ]
    cell_width = 892 / len(STATS)
    for index, (value, label) in enumerate(STATS):
        x = 54 + index * cell_width
        if index:
            parts.append(f'<line x1="{x:.1f}" y1="300" x2="{x:.1f}" y2="352" stroke="{c["border"]}"/>')
        tx = x + (18 if index else 0)
        color = ["cyan", "violet", "pink", "lime"][index]
        parts.extend([
            f'<text x="{tx:.1f}" y="327" font-family="{SM}" font-size="27" fill="{c[color]}">{escape(value)}</text>',
            f'<text x="{tx:.1f}" y="348" font-family="{SM}" font-size="10" letter-spacing="1.5" fill="{c["secondary"]}">{escape(label)}</text>',
        ])
    parts.extend([
        '</svg>',
    ])
    return "\n".join(parts)


def render_status(c):
    bars = []
    for i, bar_height in enumerate([10, 28, 16, 38, 22, 44, 18, 32, 12]):
        bars.append(
            f'<rect x="{842+i*12}" y="{67-bar_height}" width="5" height="{bar_height}" fill="{c[["cyan", "violet", "pink"][i%3]]}" opacity="{.42 + i*.055:.2f}">'
            f'<animate attributeName="height" values="{bar_height};{max(7, 48-bar_height)};{bar_height}" dur="{1.0+i*.11:.2f}s" repeatCount="indefinite"/></rect>'
        )
    return "\n".join([
        '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="92" viewBox="0 0 1000 92">', defs(c, "status"),
        f'<path d="M1 1H978L999 22V91H22L1 70Z" fill="{c["surface"]}" stroke="{c["border"]}"/>',
        f'<path d="M1 1H214" stroke="{c["cyan"]}" stroke-width="4"/><path d="M214 1H350" stroke="{c["violet"]}" stroke-width="4"/><path d="M350 1H999" stroke="{c["border"]}" stroke-width="4"/>',
        f'<rect x="22" y="26" width="9" height="9" fill="{c["cyan"]}" filter="url(#status-glow)"><animate attributeName="opacity" values="1;.18;1" dur="1.2s" repeatCount="indefinite"/></rect>',
        f'<text x="44" y="31" font-family="{SM}" font-size="8" letter-spacing="1.7" fill="{c["secondary"]}">BIOCOMPUTE BUS</text>',
        f'<text x="44" y="54" font-family="{SM}" font-size="13" letter-spacing="1.3" fill="{c["display"]}">NODE 004 / AWAKE</text>',
        f'<text x="44" y="72" font-family="{SM}" font-size="8" letter-spacing="1.2" fill="{c["violet"]}">HUMAN-IN-THE-LOOP</text>',
        f'<line x1="224" y1="16" x2="224" y2="76" stroke="{c["border"]}"/>',
        f'<text x="250" y="27" font-family="{SM}" font-size="8" letter-spacing="1.6" fill="{c["secondary"]}">ACTIVE PROCESSES</text>',
        f'<rect x="250" y="39" width="5" height="5" fill="{c["cyan"]}"/><text x="264" y="46" font-family="{SM}" font-size="10" fill="{c["display"]}">AGENT LOOP</text>',
        f'<rect x="368" y="39" width="5" height="5" fill="{c["violet"]}"/><text x="382" y="46" font-family="{SM}" font-size="10" fill="{c["display"]}">RAG MEMORY</text>',
        f'<rect x="492" y="39" width="5" height="5" fill="{c["pink"]}"/><text x="506" y="46" font-family="{SM}" font-size="10" fill="{c["display"]}">MOBILE CORE</text>',
        f'<path d="M250 66h54l9-11 12 22 12-17 11 6h62l7-6 9 6h72l9-18 10 29 12-20 10 9h92" fill="none" stroke="{c["border"]}" stroke-width="1.2"/>',
        '<path d="M250 66h54l9-11 12 22 12-17 11 6h62l7-6 9 6h72l9-18 10 29 12-20 10 9h92" fill="none" stroke="url(#status-signal)" stroke-width="2" stroke-dasharray="50 490"><animate attributeName="stroke-dashoffset" values="0;-540" dur="2.8s" repeatCount="indefinite"/></path>',
        f'<line x1="760" y1="16" x2="760" y2="76" stroke="{c["border"]}"/>',
        f'<text x="785" y="28" font-family="{SM}" font-size="8" letter-spacing="1.4" fill="{c["secondary"]}">SIGNAL DENSITY</text>',
        *bars,
        f'<text x="972" y="81" text-anchor="end" font-family="{SM}" font-size="8" letter-spacing="1.2" fill="{c["secondary"]}">98.4% / LIVE</text>',
        '</svg>',
    ])


def render_divider(c):
    path = "M18 17 H170 L194 7 L218 27 L246 11 L270 22 L292 17 H982"
    return "\n".join([
        '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="34" viewBox="0 0 1000 34">', defs(c, "divider"),
        f'<path d="{path}" fill="none" stroke="{c["border"]}" stroke-width="1.3"/>',
        f'<path d="{path}" fill="none" stroke="url(#divider-signal)" stroke-width="2" stroke-dasharray="90 900" filter="url(#divider-glow)"><animate attributeName="stroke-dashoffset" values="0;-1000" dur="3.2s" repeatCount="indefinite"/></path>',
        f'<circle cx="18" cy="17" r="3" fill="{c["cyan"]}"/><circle cx="982" cy="17" r="3" fill="{c["pink"]}"/>', '</svg>',
    ])


def render_stack(c):
    modules = [
        ("01", "INTELLIGENCE", "LLMs  ·  AGENTS  ·  RAG  ·  FINE-TUNING", "cyan"),
        ("02", "MODEL LAB", "OLLAMA  ·  RUNPOD  ·  OPENAI  ·  HUGGING FACE", "violet"),
        ("03", "MOBILE SHELL", "FLUTTER  ·  REACT NATIVE  ·  EXPO  ·  DART", "pink"),
        ("04", "BACKBONE", "NODE.JS  ·  EXPRESS  ·  REST  ·  DOCKER", "lime"),
        ("05", "MEMORY", "POSTGRES  ·  PGVECTOR  ·  MONGODB  ·  FIREBASE", "cyan"),
        ("06", "LANGUAGE", "TYPESCRIPT  ·  PYTHON  ·  JAVASCRIPT", "violet"),
    ]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="322" viewBox="0 0 1000 322">', defs(c, "stack"),
        f'<path d="M1 1H970L999 30V321H30L1 292Z" fill="{c["surface"]}" stroke="{c["border"]}"/>',
        '<path d="M1 1H970L999 30V321H30L1 292Z" fill="url(#stack-grid)" opacity=".45"/>',
        f'<text x="32" y="38" font-family="{DOTO}" font-size="22" font-weight="650" letter-spacing="2" fill="{c["display"]}">SPECIMEN INVENTORY</text>',
        f'<text x="968" y="36" text-anchor="end" font-family="{SM}" font-size="9" letter-spacing="1.4" fill="{c["secondary"]}">06 MODULES / BIOCOMPUTE LAB</text>',
        '<line x1="32" y1="55" x2="968" y2="55" stroke="url(#stack-signal)" stroke-width="1"/>',
    ]
    for i, (number, label, tech, color) in enumerate(modules):
        x = 32 + (i % 2) * 476
        y = 76 + (i // 2) * 76
        parts.extend([
            f'<path d="M{x} {y+9}L{x+9} {y}H{x+450}V{y+49}L{x+441} {y+58}H{x}Z" fill="{c["bg"]}" stroke="{c["border"]}"/>',
            f'<circle cx="{x+22}" cy="{y+29}" r="7" fill="{c[color]}" opacity=".18"><animate attributeName="r" values="7;12;7" dur="{1.7+i*.2:.2f}s" repeatCount="indefinite"/></circle>',
            f'<circle cx="{x+22}" cy="{y+29}" r="3" fill="{c[color]}"/>',
            f'<text x="{x+42}" y="{y+22}" font-family="{SM}" font-size="9" letter-spacing="1.5" fill="{c[color]}">{number} / {label}</text>',
            f'<text x="{x+42}" y="{y+42}" font-family="{SM}" font-size="10.5" fill="{c["primary"]}">{escape(tech)}</text>',
        ])
    parts.extend([
        f'<text x="32" y="302" font-family="{SM}" font-size="9" letter-spacing="1.4" fill="{c["secondary"]}">STACK CHANGES. CURIOSITY DOESN\'T.</text>',
        f'<text x="968" y="302" text-anchor="end" font-family="{SM}" font-size="9" letter-spacing="1.4" fill="{c["secondary"]}">READY FOR NEXT EXPERIMENT / 004</text>', '</svg>',
    ])
    return "\n".join(parts)


def render_achievements(c):
    cards = [
        ("10+", "APPS RELEASED", "FROM IDEA → STORE", "cyan"),
        ("10K+", "HUMANS REACHED", "REAL USERS / REAL CHAOS", "violet"),
        ("5+", "MODELS TRAINED", "CUSTOM WEIGHTS / REAL TASKS", "pink"),
        ("03", "YEARS EXPLORING", "STILL ASKING WHY", "lime"),
    ]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="250" viewBox="0 0 1000 250">', defs(c, "impact"),
        f'<path d="M1 1H978L999 22V249H22L1 228Z" fill="{c["surface"]}" stroke="{c["border"]}"/>',
        f'<text x="32" y="38" font-family="{DOTO}" font-size="22" font-weight="650" letter-spacing="2" fill="{c["display"]}">FIELD RESULTS</text>',
        f'<text x="968" y="36" text-anchor="end" font-family="{SM}" font-size="9" letter-spacing="1.4" fill="{c["secondary"]}">REAL PRODUCTS &gt; PRETTY DEMOS</text>',
        '<line x1="32" y1="55" x2="968" y2="55" stroke="url(#impact-signal)"/>',
    ]
    for i, (value, label, sub, color) in enumerate(cards):
        x = 32 + i * 236
        parts.extend([
            f'<path d="M{x} 87L{x+10} 77H{x+220}V187L{x+210} 197H{x}Z" fill="{c["bg"]}" stroke="{c["border"]}"/>',
            f'<path d="M{x+16} 93h24" stroke="{c[color]}" stroke-width="3"/>',
            f'<text x="{x+16}" y="139" font-family="{DOTO}" font-size="34" font-weight="700" fill="{c[color]}">{value}</text>',
            f'<text x="{x+16}" y="165" font-family="{SM}" font-size="10" letter-spacing="1.2" fill="{c["display"]}">{label}</text>',
            f'<text x="{x+16}" y="184" font-family="{SM}" font-size="8" letter-spacing="1" fill="{c["secondary"]}">{escape(sub)}</text>',
        ])
    parts.extend([
        f'<path d="M32 224H188l16-10 18 18 20-12 18 4h708" fill="none" stroke="{c["border"]}"/>',
        '<path d="M32 224H188l16-10 18 18 20-12 18 4h708" fill="none" stroke="url(#impact-signal)" stroke-width="2" stroke-dasharray="70 900"><animate attributeName="stroke-dashoffset" values="0;-970" dur="3s" repeatCount="indefinite"/></path>',
        '</svg>',
    ])
    return "\n".join(parts)


def main():
    for theme, colors in THEMES.items():
        hero = render(colors)
        status = render_status(colors)
        divider = render_divider(colors)
        stack = render_stack(colors)
        results = render_achievements(colors)

        # Keep the legacy paths current, but publish the V2 artwork under new
        # cache-proof paths. GitHub's image proxy can retain SVG bytes even when
        # a query string changes, while a new filename forces a fresh request.
        outputs = {
            f"{theme}.svg": hero,
            f"status-{theme}.svg": status,
            f"divider-{theme}.svg": divider,
            f"stack-{theme}.svg": stack,
            f"achievements-{theme}.svg": results,
            f"bio004-hero-{theme}.svg": hero,
            f"bio004-hero-clean-{theme}.svg": hero,
            f"bio004-status-{theme}.svg": status,
            f"bio004-divider-{theme}.svg": divider,
            f"bio004-stack-{theme}.svg": stack,
            f"bio004-results-{theme}.svg": results,
            f"cipher-hero-{theme}.svg": hero,
            f"cipher-status-{theme}.svg": status,
            f"cipher-divider-{theme}.svg": divider,
            f"cipher-stack-{theme}.svg": stack,
            f"cipher-results-{theme}.svg": results,
        }
        for filename, artwork in outputs.items():
            (HERE / filename).write_text(artwork, encoding="utf-8")
        print(f"wrote {theme} BIOCOMPUTE//MUSA set")


if __name__ == "__main__":
    main()
