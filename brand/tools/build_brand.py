"""Build every CASSANDRA brand asset in VectorCraft from exact geometry.

Usage (from the repository root):
    python brand/tools/build_brand.py

Needs VectorCraft 0.10 or later (vectorcraft-cli on the default install path, or the
VECTORCRAFT_CLI environment variable). Writes only inside brand/: svg/, pdf/, eps/,
png/, web/, guide/ and source/. Re-running overwrites the same files, so the output is a
pure function of the numbers in this file and the engine version.

Geometry is defined in units of the mark's outer diameter D (mark) or of the mark height
H (lockups); see brand/README.md and docs/implementations/2026-10-14-cassandra-brand-identity.md.
"""
import json
import math
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vcdriver import VC  # noqa: E402
from wcag import contrast  # noqa: E402

BRAND = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = {k: os.path.join(BRAND, k) for k in ("svg", "pdf", "eps", "png", "web", "guide", "source")}

# Palette "Bronze and night" (owner decision 2026-10-14).
NIGHT, BRONZE, GOLD, IVORY = "#121C2E", "#8A672B", "#D2A65A", "#F4EFE6"
BLACK, WHITE = "#000000", "#FFFFFF"
# Palette "Red-figure", for the CASSANDRA and CASSANDRA-Chorus project materials (owner, 2026-10-14).
KILN, TERRACOTTA, CLAY = "#1A1411", "#B2462A", "#F3EBDD"
# The mark (full and small) in the Red-figure palette, for the CASSANDRA and CASSANDRA-Chorus
# README headers and other project material. Only the mark: the lockups say COLLECTIVE and
# stay in the organisation's palette.
PROJECT_MARK_VARIANTS = {
    "red-figure-on-light": dict(c=KILN, dash=TERRACOTTA),
    "red-figure-on-dark": dict(c=CLAY, dash=TERRACOTTA),
}

# Colour variants: C = the ring, dash = the forecast, text = wordmark, desc = descriptor.
VARIANTS = {
    "on-light": dict(c=NIGHT, dash=BRONZE, text=NIGHT, desc=BRONZE, ground=IVORY),
    "on-dark": dict(c=IVORY, dash=GOLD, text=IVORY, desc=GOLD, ground=NIGHT),
    "black": dict(c=BLACK, dash=BLACK, text=BLACK, desc=BLACK, ground=WHITE),
    "white": dict(c=WHITE, dash=WHITE, text=WHITE, desc=WHITE, ground=BLACK),
}

# Mark geometry, radii as fractions of D (outer radius is 0.5 D), angles in degrees
# measured clockwise on screen from the rightward horizontal (y axis points down).
FULL = dict(r_in=0.32, gap=50, dash_out=0.455, dash_in=0.365,
            dashes=[(-37, -21), (-8, 8), (21, 37)])
SMALL = dict(r_in=0.30, gap=52, dash_out=0.475, dash_in=0.325, dashes=[(-17, 17)])

WORDMARK = dict(text="CASSANDRA", font="Source Serif 4", style="Regular", tracking=160)
DESCRIPTOR = dict(text="COLLECTIVE", font="Inter", style="Medium", tracking=350)
SANS = "Inter"

# Lockup proportions, fractions of the mark height H.
HORIZONTAL = dict(gap=0.30, word_h=0.30, desc_h=0.095, line_gap=0.11)
STACKED = dict(gap=0.24, word_h=0.20, desc_h=0.068, line_gap=0.085)
COMPACT = dict(gap=0.30, word_h=0.34)  # horizontal without the descriptor, for small sizes
CLEAR_SPACE = 0.25  # of H, on every side

# Owner decision 2026-10-14 (candidate B of three).
TAGLINE = "Language models for everyday hardware."

# Social preview cards of the project repositories (owner decision 2026-10-14: one card per
# repository; Ephesus keeps its own). The card line is the short form of each repository's
# description, broken by hand into lines that fit the text column.
CARD_PALETTES = {
    "bronze-night": dict(ground=NIGHT, c=IVORY, dash=GOLD, kicker=GOLD, text=IVORY),
    "red-figure": dict(ground=KILN, c=CLAY, dash=TERRACOTTA, kicker=TERRACOTTA, text=CLAY),
}
PROJECT_CARDS = {
    "cassandra": dict(palette="red-figure", name=["CASSANDRA"],
                      line=["Language-model research", "on consumer hardware."]),
    "chorus": dict(palette="red-figure", name=["CASSANDRA", "CHORUS"],
                   line=["One MoE language model trained", "across volunteer machines."]),
    "dervish": dict(palette="bronze-night", name=["DERVISH"],
                    line=["A Muon-variant optimizer with", "a provably bounded spectrum."]),
}
KICKER = dict(text="CASSANDRA COLLECTIVE", font="Inter", style="Medium", tracking=350)

# The Ephesus card (owner decisions 2026-10-15): card A, the Collective's project-card layout
# drawn entirely in Ephesus's own identity (docs/design/UI-DESIGN.md in Ephesus): its section 2
# tokens, its pixel column and wordmark (vendored in ephesus_artwork.json), and IBM Plex Mono.
EPH_INK900, EPH_INK700, EPH_MARBLE100 = "#221A14", "#4A3B2C", "#F4EDE0"
EPH_TERRACOTTA = "#C4552D"
EPH_TOKENS = {EPH_INK900, EPH_INK700, EPH_MARBLE100, EPH_TERRACOTTA, "#E8A987", "#E7DCC6", "#D3C4A5"}
EPH_MONO, EPH_MONO_MEDIUM = "IBM Plex Mono", "IBM Plex Mono Medium"  # install_ephesus_fonts.py
EPHESUS_CARD = dict(
    kicker="A CASSANDRA COLLECTIVE PROJECT",
    headline="An agentic harness you govern and measure",
    line=["Every agent works behind your gates;", "the harness is scored by its own bench."],
    footer=["pre-alpha · MIT · ephesushq.com", "github.com/Cassandra-Collective/Ephesus"],
    aria="Ephesus, an agentic harness you govern and measure",
)
# Integer layout. The column (64-unit master at 6x, frame box left out) is centred on (290, 320)
# like the other project cards' mark; the text column starts at x 520 and is the wordmark's
# 533 px wide.
EPH_LAYOUT = dict(column_t=(98, 116), scale=6, text_x=520, text_w=533, kicker_base=150, word_top=172,
                  rule_gap=26, rule_h=6, head_gap=44, line_gap=40, line_step=30, footer_gap=52,
                  footer_step=28, kicker_size=16, kicker_tracking=120, text_size=21, footer_size=18)
# kicker_h 19 sets the kicker at about 26 px, WCAG "large text" (24 px and up), where 3:1 is enough
# for terracotta on kiln black (3.30:1); build_project_cards checks this.
CARD = dict(mark_d=300, mark_cx=290, text_x=520, text_w=650, kicker_h=19, name_h=62, name_lead=1.45,
            line_size=32, line_lead=1.4, gap_kicker=30, gap_name=40)


# ---------------------------------------------------------------- geometry
def _pt(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def sector(cx, cy, R, r, a0, a1):
    """SVG path data of an annular sector between radii r < R from angle a0 to a1."""
    large = 1 if (a1 - a0) % 360 > 180 else 0
    x0, y0 = _pt(cx, cy, R, a0)
    x1, y1 = _pt(cx, cy, R, a1)
    x2, y2 = _pt(cx, cy, r, a1)
    x3, y3 = _pt(cx, cy, r, a0)
    return (f"M {x0:.4f} {y0:.4f} A {R:.4f} {R:.4f} 0 {large} 1 {x1:.4f} {y1:.4f} "
            f"L {x2:.4f} {y2:.4f} A {r:.4f} {r:.4f} 0 {large} 0 {x3:.4f} {y3:.4f} Z")


# ---------------------------------------------------------------- drawing helpers
def path(vc, d, fill):
    return vc.tool("draw_path", d=d, fill=fill, stroke="none")["id"]


def rect(vc, x, y, w, h, fill, radius=None, stroke=None, weight=1):
    args = dict(shape="rectangle", x=x, y=y, width=w, height=h, fill=fill, stroke=stroke or "none")
    if radius:
        args["radius"] = radius
    if stroke:
        args["strokeWidth"] = weight
    return vc.tool("draw_shape", **args)["id"]


def bounds(vc, oid):
    n = vc.cmd("document.node", id=oid, summary=True)
    return n.get("bounds") or n["summary"]["bounds"]


def set_box(vc, oid, x, y, w, h):
    vc.cmd("select.set", ids=[oid])
    vc.cmd("object.setBounds", x=x, y=y, width=w, height=h, reference=0)


def group(vc, ids):
    vc.cmd("select.set", ids=ids)
    return vc.cmd("object.group")["id"]


def delete(vc, ids):
    vc.cmd("select.set", ids=ids)
    vc.cmd("edit.clear")


def draw_mark(vc, cx, cy, D, v, geo=FULL):
    """Draw the mark centred on the ring centre (cx, cy) with outer diameter D. Returns ids."""
    ids = [path(vc, sector(cx, cy, 0.5 * D, geo["r_in"] * D, geo["gap"], 360 - geo["gap"]), v["c"])]
    for a0, a1 in geo["dashes"]:
        ids.append(path(vc, sector(cx, cy, geo["dash_out"] * D, geo["dash_in"] * D, a0, a1), v["dash"]))
    return ids


def outlined(vc, spec, size, colour, tracking):
    """Set one line of type, convert it to outlines. Returns (group id, bounds)."""
    t = vc.tool("add_text", x=0, y=0, text=spec["text"], font=spec["font"], size=size, color=colour)["id"]
    vc.cmd("text.setStyle", id=t, style=spec["style"], tracking=tracking)
    vc.cmd("select.set", ids=[t])
    gid = vc.cmd("type.createOutlines")["ids"][0]
    return gid, bounds(vc, gid)


def text_line(vc, spec, letter_h, colour, x, y):
    """Outlined line whose letter height (cap height plus round overshoot) is letter_h,
    top-left at (x, y). Tracking is the spec's, in thousandths of an em. Returns (id, w, h)."""
    gid, b = outlined(vc, spec, 100, colour, spec["tracking"])
    s = letter_h / b["height"]
    set_box(vc, gid, x, y, b["width"] * s, letter_h)
    return gid, b["width"] * s, letter_h


def free_text(vc, text, size, colour, font=SANS, style="Regular"):
    return outlined(vc, dict(text=text, font=font, style=style), size, colour, 0)


# ---------------------------------------------------------------- lockups
def horizontal(vc, x, y, H, v):
    """Mark + wordmark over descriptor. Top-left (x, y), mark height H. Returns (ids, w, h)."""
    p = HORIZONTAL
    ids = draw_mark(vc, x + H / 2, y + H / 2, H, v)
    tx = x + H + p["gap"] * H
    block = (p["word_h"] + p["line_gap"] + p["desc_h"]) * H
    top = y + H / 2 - block / 2
    w_id, w_w, _ = text_line(vc, WORDMARK, p["word_h"] * H, v["text"], tx, top)
    d_id, _, _ = text_line(vc, DESCRIPTOR, p["desc_h"] * H, v["desc"], tx, top + (p["word_h"] + p["line_gap"]) * H)
    return ids + [w_id, d_id], tx + w_w - x, H


def compact(vc, x, y, H, v):
    """Mark + wordmark only, wordmark centred on the mark's centre line. Returns (ids, w, h)."""
    p = COMPACT
    ids = draw_mark(vc, x + H / 2, y + H / 2, H, v)
    tx = x + H + p["gap"] * H
    w_id, w_w, _ = text_line(vc, WORDMARK, p["word_h"] * H, v["text"], tx, y + H / 2 - p["word_h"] * H / 2)
    return ids + [w_id], tx + w_w - x, H


def stacked(vc, x, y, H, v):
    """Mark over wordmark over descriptor, centred on one axis. Returns (ids, w, h)."""
    p = STACKED
    w_id, w_w, _ = text_line(vc, WORDMARK, p["word_h"] * H, v["text"], 0, 0)
    d_id, d_w, _ = text_line(vc, DESCRIPTOR, p["desc_h"] * H, v["desc"], 0, 0)
    W = max(H, w_w)
    ids = draw_mark(vc, x + W / 2, y + H / 2, H, v)
    wy = y + H + p["gap"] * H
    set_box(vc, w_id, x + (W - w_w) / 2, wy, w_w, p["word_h"] * H)
    dy = wy + (p["word_h"] + p["line_gap"]) * H
    set_box(vc, d_id, x + (W - d_w) / 2, dy, d_w, p["desc_h"] * H)
    return ids + [w_id, d_id], W, dy + p["desc_h"] * H - y


# ---------------------------------------------------------------- documents and export
def new_doc(vc, name, w, h, title, description):
    vc.cmd("file.new", width=w, height=h, units="Pixels", name=name)
    vc.cmd("file.info", title=title, author="Cassandra Collective", description=description,
           keywords=["CASSANDRA", "Cassandra Collective", "logo"])


def fit_artboard(vc, w, h):
    vc.cmd("artboard.setProps", index=0, x=0, y=0, width=round(w, 3), height=round(h, 3))


def export(vc, stem, vector=True, pdf_eps=True, png=(), web=False, source=True):
    """Write svg/pdf/eps/png (or web/) files for the active document, save its gzip-compressed
    .vectorcraft source unless source=False, and close it."""
    out = []
    if vector:
        out.append(vc.tool("export", path=os.path.join(DIRS["web" if web else "svg"], stem + ".svg"))["path"])
    if pdf_eps:
        out.append(vc.cmd("document.export", path=os.path.join(DIRS["pdf"], stem + ".pdf"), preserveEditing=False)["path"])
        out.append(vc.cmd("document.export", path=os.path.join(DIRS["eps"], stem + ".eps"))["path"])
    for suffix, scale in png:
        out.append(vc.tool("export", path=os.path.join(DIRS["web" if web else "png"], f"{stem}{suffix}.png"),
                           scale=scale)["path"])
    if source:
        vc.cmd("document.save", path=os.path.join(DIRS["source"], stem + ".vectorcraft"), compress=True)
    vc.cmd("file.close")
    return out


def build_marks(vc, variants=None):
    for vname, v in (variants or VARIANTS).items():
        new_doc(vc, f"mark-{vname}", 512, 512, "CASSANDRA mark", f"The Forecast mark, {vname} colours.")
        draw_mark(vc, 256, 256, 512, v)
        export(vc, f"cassandra-mark-{vname}", png=[(f"-{px}", px / 512) for px in (64, 128, 256, 512, 1024)])
        new_doc(vc, f"mark-small-{vname}", 64, 64, "CASSANDRA mark, small",
                f"The Forecast mark redrawn for 24 px and below, {vname} colours.")
        draw_mark(vc, 32, 32, 64, v, SMALL)
        export(vc, f"cassandra-mark-small-{vname}", pdf_eps=False, png=[(f"-{px}", px / 64) for px in (16, 24, 32)])


def build_lockups(vc):
    for vname, v in VARIANTS.items():
        new_doc(vc, f"horizontal-{vname}", 2000, 400, "CASSANDRA Collective, horizontal lockup",
                f"Primary horizontal lockup, {vname} colours.")
        _, w, h = horizontal(vc, 0, 0, 200, v)
        fit_artboard(vc, w, h)
        export(vc, f"cassandra-horizontal-{vname}", png=[("", 1), ("@2x", 2), ("@4x", 4)])
        new_doc(vc, f"compact-{vname}", 2000, 400, "CASSANDRA, compact horizontal lockup",
                f"Horizontal lockup without the descriptor, for small sizes, {vname} colours.")
        _, w, h = compact(vc, 0, 0, 200, v)
        fit_artboard(vc, w, h)
        export(vc, f"cassandra-compact-{vname}", png=[("", 1), ("@2x", 2), ("@4x", 4)])
        new_doc(vc, f"stacked-{vname}", 1000, 1000, "CASSANDRA Collective, stacked lockup",
                f"Stacked lockup, {vname} colours.")
        _, w, h = stacked(vc, 0, 0, 240, v)
        fit_artboard(vc, w, h)
        export(vc, f"cassandra-stacked-{vname}", png=[("", 1), ("@2x", 2), ("@4x", 4)])


def build_web(vc):
    v = VARIANTS["on-dark"]
    # Favicon: night tile, small mark at every size, so the tab icon keeps one shape.
    new_doc(vc, "favicon", 64, 64, "CASSANDRA favicon", "Small mark on a night tile, for 16 to 48 px.")
    rect(vc, 0, 0, 64, 64, NIGHT, radius=12)
    draw_mark(vc, 32, 32, 52, v, SMALL)
    export(vc, "favicon", pdf_eps=False, web=True, png=[("-16", 0.25), ("-32", 0.5), ("-48", 0.75)])
    # App icon: full mark on a square night tile; platforms round the corners themselves.
    new_doc(vc, "app-icon", 512, 512, "CASSANDRA app icon", "Full mark on a night tile, for 48 px and up.")
    rect(vc, 0, 0, 512, 512, NIGHT)
    draw_mark(vc, 256, 256, 320, v)
    export(vc, "app-icon", pdf_eps=False, web=True,
           png=[("-180", 180 / 512), ("-192", 192 / 512), ("-512", 1)])
    # Organisation avatar.
    new_doc(vc, "avatar", 1024, 1024, "Cassandra Collective avatar", "Organisation avatar: full mark on night.")
    rect(vc, 0, 0, 1024, 1024, NIGHT)
    draw_mark(vc, 512, 512, 600, v)
    export(vc, "avatar", pdf_eps=False, web=True, png=[("-500", 500 / 1024), ("-1024", 1)])
    # Social card with the tagline (GitHub's recommended 1280 x 640).
    new_doc(vc, "social-card", 1280, 640, "Cassandra Collective social card", TAGLINE)
    rect(vc, 0, 0, 1280, 640, NIGHT)
    ids, w, h = horizontal(vc, 0, 0, 150, v)
    g = group(vc, ids)
    set_box(vc, g, (1280 - w) / 2, 205, w, h)
    t, b = free_text(vc, TAGLINE, 40, IVORY)
    set_box(vc, t, (1280 - b["width"]) / 2, 425, b["width"], b["height"])
    export(vc, "social-card", pdf_eps=False, web=True, png=[("", 1)])


def build_project_cards(vc):
    """One 1280 x 640 social card per project repository: the mark on the left; on the right
    a gold kicker, the project name in the wordmark's type, and the card line in Inter, the
    whole text block centred vertically on the card. Raises if a line overflows the column."""
    c = CARD
    for key, spec in PROJECT_CARDS.items():
        pal = CARD_PALETTES[spec["palette"]]
        v = dict(c=pal["c"], dash=pal["dash"])
        new_doc(vc, f"social-card-{key}", 1280, 640, f"{' '.join(spec['name'])} social card",
                " ".join(spec["line"]))
        rect(vc, 0, 0, 1280, 640, pal["ground"])
        draw_mark(vc, c["mark_cx"], 320, c["mark_d"], v)
        name_step = c["name_h"] * c["name_lead"]
        line_step = c["line_size"] * c["line_lead"]
        lines = [free_text(vc, t, c["line_size"], pal["text"]) for t in spec["line"]]
        line_h = max(b["height"] for _, b in lines)
        block = (c["kicker_h"] + c["gap_kicker"] + c["name_h"] + name_step * (len(spec["name"]) - 1)
                 + c["gap_name"] + line_h + line_step * (len(lines) - 1))
        y = 320 - block / 2
        k, kw, _ = text_line(vc, KICKER, c["kicker_h"], pal["kicker"], c["text_x"], y)
        probe, pb = outlined(vc, KICKER, 100, pal["kicker"], KICKER["tracking"])
        kicker_size = 100 * c["kicker_h"] / pb["height"]
        delete(vc, [probe])
        if contrast(pal["kicker"], pal["ground"]) < 4.5 and kicker_size < 24:
            raise ValueError(f"card {key}: kicker at {kicker_size:.1f} px needs 4.5:1, has "
                             f"{contrast(pal['kicker'], pal['ground']):.2f}:1")
        print(f"  card {key}: {spec['palette']}, kicker {kicker_size:.1f} px, "
              f"kicker contrast {contrast(pal['kicker'], pal['ground']):.2f}:1")
        y += c["kicker_h"] + c["gap_kicker"]
        widths = [kw]
        for i, word in enumerate(spec["name"]):
            _, w, _ = text_line(vc, dict(WORDMARK, text=word), c["name_h"], pal["text"], c["text_x"], y + i * name_step)
            widths.append(w)
        y += c["name_h"] + name_step * (len(spec["name"]) - 1) + c["gap_name"]
        for i, (gid, b) in enumerate(lines):
            set_box(vc, gid, c["text_x"], y + i * line_step, b["width"], b["height"])
            widths.append(b["width"])
        if max(widths) > c["text_w"]:
            raise ValueError(f"card {key}: a line is {max(widths):.0f} px wide, the column is {c['text_w']} px")
        export(vc, f"social-card-{key}", pdf_eps=False, web=True, png=[("", 1)])


def require_fonts(vc, families):
    for family in families:
        try:
            vc.cmd("text.fontList", family=family)
        except RuntimeError:
            raise SystemExit(f"VectorCraft has no font family '{family}'. Install it first:\n"
                             "  python brand/tools/install_ephesus_fonts.py <path to an Ephesus checkout>")


def live_text(vc, s, x, baseline, size, font, fill, tracking=0):
    """Point type with its baseline at (x, baseline). Returns (id, bounds)."""
    t = vc.tool("add_text", x=x, y=baseline, text=s, font=font, size=size, color=fill)["id"]
    if tracking:
        vc.cmd("text.setStyle", id=t, tracking=tracking)
    return t, bounds(vc, t)


def ephesus_svg(svg):
    """Normalise VectorCraft's live-text SVG to Ephesus's file rules, then check them."""
    mono = "&apos;IBM Plex Mono&apos;,&apos;DejaVu Sans Mono&apos;,monospace"
    svg = svg.replace('font-family="&apos;IBM Plex Mono Medium&apos;"', f'font-family="{mono}" font-weight="500"')
    svg = svg.replace('font-family="&apos;IBM Plex Mono&apos;"', f'font-family="{mono}"')
    svg = re.sub(r"#([0-9a-fA-F]{6})", lambda m: "#" + m.group(1).upper(), svg)
    svg = re.sub(r'(<svg\b[^>]*?viewBox="0 0 1280 640")',
                 r'\1 shape-rendering="crispEdges" role="img" aria-label="' + EPHESUS_CARD["aria"] + '"',
                 svg, count=1)
    colours = set(re.findall(r"#[0-9A-F]{6}", svg))
    fractional = re.findall(r'(?:\b(?:x|y|width|height)="-?\d*\.\d+")|(?:\bd="[^"]*\d\.\d)|(?:matrix\([^)]*\d\.\d)', svg)
    families = set(re.findall(r'font-family="([^"]*)"', svg))
    problems = []
    if not colours <= EPH_TOKENS:
        problems.append(f"colours outside the tokens: {sorted(colours - EPH_TOKENS)}")
    if fractional:
        problems.append(f"fractional coordinates: {fractional[:3]}")
    if families != {mono}:
        problems.append(f"unexpected font families: {families}")
    if 'shape-rendering="crispEdges"' not in svg:
        problems.append("crispEdges missing on the root")
    if problems:
        raise ValueError("Ephesus card SVG breaks Ephesus's rules: " + "; ".join(problems))
    return svg


def build_ephesus_card(vc, ephesus_out=None):
    """Card A for Ephesus (see the constants above). Writes web/social-card-ephesus.{svg,png}
    and its source with outlined text; with ephesus_out (an Ephesus checkout) also writes that
    repository's docs/brand/ephesus-social-card.svg, site/public/img/social-card.svg and
    site/public/img/social-card.png, with live text normalised by ephesus_svg()."""
    require_fonts(vc, (EPH_MONO, EPH_MONO_MEDIUM))
    art = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ephesus_artwork.json"),
                         encoding="utf-8"))
    c, p = EPH_LAYOUT, EPHESUS_CARD
    new_doc(vc, "social-card-ephesus", 1280, 640, "Ephesus", p["aria"])
    rect(vc, 0, 0, 1280, 640, EPH_INK900)
    rect(vc, 8, 8, 1264, 624, EPH_MARBLE100)
    tx, ty = c["column_t"]
    for x, y, w, h, fill in art["column"]["rects"][2:]:      # the first two are the frame box
        rect(vc, tx + x * c["scale"], ty + y * c["scale"], w * c["scale"], h * c["scale"], fill)
    ox, oy = art["wordmark"]["origin"]
    for x, y, w, h, fill in art["wordmark"]["rects"]:
        rect(vc, x - ox + c["text_x"], y - oy + c["word_top"], w, h, fill)
    rule_y = c["word_top"] + 91 + c["rule_gap"]
    rect(vc, c["text_x"], rule_y, c["text_w"], c["rule_h"], EPH_TERRACOTTA)
    x0, head = c["text_x"], rule_y + c["rule_h"] + c["head_gap"]
    lines = [(p["kicker"], c["kicker_base"], c["kicker_size"], EPH_MONO_MEDIUM, EPH_INK700, c["kicker_tracking"]),
             (p["headline"], head, c["text_size"], EPH_MONO_MEDIUM, EPH_INK900, 0)]
    lines += [(s, head + c["line_gap"] + i * c["line_step"], c["text_size"], EPH_MONO, EPH_INK900, 0)
              for i, s in enumerate(p["line"])]
    foot = head + c["line_gap"] + c["line_step"] * (len(p["line"]) - 1) + c["footer_gap"]
    lines += [(s, foot + i * c["footer_step"], c["footer_size"], EPH_MONO, EPH_INK700, 0)
              for i, s in enumerate(p["footer"])]
    ids = []
    for s, base, size, font, fill, track in lines:
        t, b = live_text(vc, s, x0, base, size, font, fill, track)
        if b["x"] + b["width"] > x0 + c["text_w"]:
            raise ValueError(f"Ephesus card: '{s}' ends at {b['x'] + b['width']:.0f}, past {x0 + c['text_w']}")
        print(f"  ephesus card: {b['width']:6.1f} px  {s}")
        ids.append(t)
    if ephesus_out:
        tmp = os.path.join(BRAND, ".ephesus-card")
        os.makedirs(tmp, exist_ok=True)
        try:
            vc.tool("export", path=os.path.join(tmp, "card.svg"))
            vc.tool("export", path=os.path.join(tmp, "card.png"))
            svg = ephesus_svg(open(os.path.join(tmp, "card.svg"), encoding="utf-8").read())
            for rel in (("docs", "brand", "ephesus-social-card.svg"), ("site", "public", "img", "social-card.svg")):
                with open(os.path.join(ephesus_out, *rel), "w", encoding="utf-8", newline="\n") as f:
                    f.write(svg)
            shutil.copyfile(os.path.join(tmp, "card.png"), os.path.join(ephesus_out, "site", "public", "img", "social-card.png"))
            print(f"  ephesus card: wrote 3 files into {ephesus_out}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    vc.cmd("select.set", ids=ids)
    vc.cmd("type.createOutlines")
    export(vc, "social-card-ephesus", pdf_eps=False, web=True, png=[("", 1)])


def build_guide(vc):
    # Palette with names, hex codes and contrast ratios.
    swatches = [("Night", NIGHT, "Base: ring, wordmark, dark grounds",
                 f"{contrast(NIGHT, IVORY):.2f}:1 against Ivory"),
                ("Bronze", BRONZE, "Accent on light grounds",
                 f"{contrast(BRONZE, IVORY):.2f}:1 on Ivory     {contrast(BRONZE, NIGHT):.2f}:1 on Night"),
                ("Gold", GOLD, "Accent on dark grounds only",
                 f"{contrast(GOLD, NIGHT):.2f}:1 on Night     never on Ivory ({contrast(GOLD, IVORY):.2f}:1)"),
                ("Ivory", IVORY, "Light ground, reversed ring and text",
                 f"{contrast(IVORY, NIGHT):.2f}:1 against Night")]
    W, ROW = 1200, 150
    new_doc(vc, "palette", W, ROW * 4 + 40, "CASSANDRA palette", "Bronze and night, with WCAG contrast ratios.")
    rect(vc, 0, 0, W, ROW * 4 + 40, WHITE)
    for i, (name, hx, role, ratios) in enumerate(swatches):
        y = 20 + i * ROW
        rect(vc, 20, y, 120, 120, hx, stroke="#C8C8C8" if hx == IVORY else None)
        for text, size, dy, col in [(f"{name}  {hx}", 30, 18, "#111111"), (role, 20, 62, "#444444"), (ratios, 20, 96, "#444444")]:
            t, b = free_text(vc, text, size, col)
            set_box(vc, t, 170, y + dy, b["width"], b["height"])
    export(vc, "palette", pdf_eps=False, png=[("", 1)], source=False)
    os.replace(os.path.join(DIRS["svg"], "palette.svg"), os.path.join(DIRS["guide"], "palette.svg"))
    os.replace(os.path.join(DIRS["png"], "palette.png"), os.path.join(DIRS["guide"], "palette.png"))

    # Construction drawing.
    S, D = 760, 460
    cx, cy = S / 2, 330
    new_doc(vc, "construction", S, S, "CASSANDRA mark construction", "Radii and angles of the Forecast mark.")
    rect(vc, 0, 0, S, S, WHITE)
    ids = draw_mark(vc, cx, cy, D, dict(c="#D9DCE2", dash="#E7D9BD"))
    guide_col = "#B04A2E"
    for frac in (0.5, FULL["r_in"], FULL["dash_out"], FULL["dash_in"]):
        vc.tool("draw_shape", shape="ellipse", x=cx - frac * D, y=cy - frac * D, width=2 * frac * D,
                height=2 * frac * D, fill="none", stroke=guide_col, strokeWidth=1)
    for ang in (-FULL["gap"], FULL["gap"]) + tuple(a for pair in FULL["dashes"] for a in pair):
        x1, y1 = _pt(cx, cy, 0.56 * D, ang)
        vc.tool("draw_path", d=f"M {cx} {cy} L {x1:.2f} {y1:.2f}", fill="none", stroke=guide_col, strokeWidth=0.75)
    for text, ang in [("50°", -50), ("37°", -37), ("21°", -21), ("8°", -8)]:
        lx, ly = _pt(cx, cy, 0.585 * D, ang)
        t, b = free_text(vc, text, 15, guide_col)
        set_box(vc, t, lx, ly - b["height"] / 2, b["width"], b["height"])
    legend = ["Ring: outer radius 0.50 D, inner radius 0.32 D (thickness 0.18 D)",
              "Forecast dashes: radius 0.365 D to 0.455 D, centred on the ring's mid-line 0.41 D",
              "Opening 100° = 3 dashes × 16° + 4 spaces × 13°, symmetric about the horizontal"]
    for k, line in enumerate(legend):
        t, b = free_text(vc, line, 17, "#111111")
        set_box(vc, t, 30, S - 96 + k * 30, b["width"], b["height"])
    export(vc, "construction", pdf_eps=False, png=[("", 1)], source=False)
    os.replace(os.path.join(DIRS["svg"], "construction.svg"), os.path.join(DIRS["guide"], "construction.svg"))
    os.replace(os.path.join(DIRS["png"], "construction.png"), os.path.join(DIRS["guide"], "construction.png"))

    # Clear space.
    H, X = 200, CLEAR_SPACE * 200
    new_doc(vc, "clear-space", 1400, 600, "CASSANDRA clear space", "Keep X = 0.25 H free on every side.")
    rect(vc, 0, 0, 1400, 600, WHITE)
    ids, w, h = horizontal(vc, 0, 0, H, VARIANTS["on-light"])
    g = group(vc, ids)
    ox, oy = (1400 - w) / 2, 170
    set_box(vc, g, ox, oy, w, h)
    rect(vc, ox - X, oy - X, w + 2 * X, h + 2 * X, "none", stroke=guide_col, weight=1.5)
    rect(vc, ox, oy, w, h, "none", stroke="#9AA3B2", weight=1)
    for qx, qy in [(ox - X, oy - X), (ox + w, oy + h)]:
        rect(vc, qx, qy, X, X, "#F3D9CF")
    t, b = free_text(vc, "X = 0.25 H  (H = mark height)", 22, "#111111")
    set_box(vc, t, ox - X, oy + h + X + 30, b["width"], b["height"])
    export(vc, "clear-space", pdf_eps=False, png=[("", 1)], source=False)
    os.replace(os.path.join(DIRS["svg"], "clear-space.svg"), os.path.join(DIRS["guide"], "clear-space.svg"))
    os.replace(os.path.join(DIRS["png"], "clear-space.png"), os.path.join(DIRS["guide"], "clear-space.png"))


def build_board(vc):
    """One overview image of the whole system for the guide's opening."""
    W, Hb = 2400, 1300
    new_doc(vc, "board", W, Hb, "CASSANDRA brand board", "Overview of the CASSANDRA identity.")
    panels = [(0, 0, IVORY, "on-light"), (W / 2, 0, NIGHT, "on-dark"),
              (0, 760, WHITE, "black"), (W / 2, 760, BLACK, "white")]
    for px, py, ground, vname in panels:
        ph = 760 if py == 0 else 540
        rect(vc, px, py, W / 2, ph, ground)
        v = VARIANTS[vname]
        ids, w, h = horizontal(vc, 0, 0, 150, v)
        g = group(vc, ids)
        set_box(vc, g, px + (W / 2 - w) / 2, py + 90, w, h)
        if py == 0:
            ids, w, h = stacked(vc, 0, 0, 200, v)
            g = group(vc, ids)
            set_box(vc, g, px + 120, py + 340, w, h)
            draw_mark(vc, px + W / 2 - 120 - 140, py + 340 + 140, 280, v)
        else:
            for k, size in enumerate((128, 64, 32)):
                draw_mark(vc, px + 264 + k * 260, py + 390, size, v)
            draw_mark(vc, px + 264 + 3 * 260, py + 390, 16, v, SMALL)
    export(vc, "brand-board", vector=False, pdf_eps=False, png=[("", 1)], source=False)
    os.replace(os.path.join(DIRS["png"], "brand-board.png"), os.path.join(DIRS["guide"], "brand-board.png"))


def main():
    ephesus_out = None
    if "--ephesus-out" in sys.argv:
        ephesus_out = os.path.abspath(sys.argv[sys.argv.index("--ephesus-out") + 1])
        if not os.path.isdir(os.path.join(ephesus_out, "docs", "brand")):
            raise SystemExit(f"--ephesus-out: {ephesus_out} is not an Ephesus checkout")
    for d in DIRS.values():
        os.makedirs(d, exist_ok=True)
    with VC(BRAND) as vc:
        build_marks(vc)
        build_marks(vc, PROJECT_MARK_VARIANTS)
        build_lockups(vc)
        build_web(vc)
        build_project_cards(vc)
        build_ephesus_card(vc, ephesus_out)
        build_guide(vc)
        build_board(vc)
    print("done")


if __name__ == "__main__":
    main()
