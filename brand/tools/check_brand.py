"""Check every built brand asset against the specification in build_brand.py.

Usage (from the repository root, after build_brand.py):
    python brand/tools/check_brand.py

Checks, each over ALL files of its kind (not a sample):
  1. Every expected file exists (the list is derived from build_brand's tables), and the
     output folders hold nothing else (no stale files from an earlier build).
  2. Every SVG parses, has a <title> and a viewBox, contains no <text> (all type outlined),
     no <image> and no external references, and uses only its variant's colours.
  3. Every PNG has the expected pixel size; the transparent sets are 8-bit RGBA with a fully
     transparent top-left pixel (always background in these layouts).
  4. Every PDF paints only with `rg` at its variant's sRGB values, and every EPS only with
     `k` at the CMYK values in build_brand.EPS_CMYK; no other colour operator, colour space,
     shading, pattern or image, and no stream the check cannot decode.
  5. The palette meets its WCAG targets for every variant's use.
  6. The dash arithmetic of the mark fills the opening exactly.
Exits 1 on the first failed group, after printing every failure in it.
"""
import os
import re
import struct
import sys
import xml.etree.ElementTree as ET
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_brand as B  # noqa: E402
from wcag import contrast  # noqa: E402

SVG_NS = "{http://www.w3.org/2000/svg}"
GITHUB_LIGHT, GITHUB_DARK = "#FFFFFF", "#0D1117"  # README grounds in GitHub's light and dark themes
failures = []


def fail(msg):
    failures.append(msg)


def expected_files():
    """(relative path, expected PNG size or None, alpha required) for every deliverable."""
    out = []
    for v in B.VARIANTS:
        for kind in ("mark", "horizontal", "compact", "stacked"):
            stem = f"cassandra-{kind}-{v}"
            out += [(f"svg/{stem}.svg", None, False), (f"pdf/{stem}.pdf", None, False),
                    (f"eps/{stem}.eps", None, False), (f"source/{stem}.vectorcraft", None, False)]
        out += [(f"png/cassandra-mark-{v}-{px}.png", (px, px), True) for px in (64, 128, 256, 512, 1024)]
        out += [(f"svg/cassandra-mark-small-{v}.svg", None, False),
                (f"source/cassandra-mark-small-{v}.vectorcraft", None, False)]
        out += [(f"png/cassandra-mark-small-{v}-{px}.png", (px, px), True) for px in (16, 24, 32)]
        for kind in ("horizontal", "compact", "stacked"):
            out += [(f"png/cassandra-{kind}-{v}{s}.png", None, True) for s in ("", "@2x", "@4x")]
    for v in B.PROJECT_MARK_VARIANTS:
        stem = f"cassandra-mark-{v}"
        out += [(f"svg/{stem}.svg", None, False), (f"pdf/{stem}.pdf", None, False),
                (f"eps/{stem}.eps", None, False), (f"source/{stem}.vectorcraft", None, False)]
        out += [(f"png/{stem}-{px}.png", (px, px), True) for px in (64, 128, 256, 512, 1024)]
        out += [(f"svg/cassandra-mark-small-{v}.svg", None, False),
                (f"source/cassandra-mark-small-{v}.vectorcraft", None, False)]
        out += [(f"png/cassandra-mark-small-{v}-{px}.png", (px, px), True) for px in (16, 24, 32)]
    out += [("web/favicon.svg", None, False)] + [(f"web/favicon-{px}.png", (px, px), True) for px in (16, 32, 48)]
    out += [("web/app-icon.svg", None, False)] + [(f"web/app-icon-{px}.png", (px, px), False) for px in (180, 192, 512)]
    out += [("web/avatar.svg", None, False), ("web/avatar-500.png", (500, 500), False),
            ("web/avatar-1024.png", (1024, 1024), False)]
    out += [("web/social-card.svg", None, False), ("web/social-card.png", (1280, 640), False)]
    out += [(f"source/{n}.vectorcraft", None, False) for n in ("favicon", "app-icon", "avatar", "social-card")]
    for k in list(B.PROJECT_CARDS) + ["ephesus"]:
        out += [(f"web/social-card-{k}.svg", None, False), (f"web/social-card-{k}.png", (1280, 640), False),
                (f"source/social-card-{k}.vectorcraft", None, False)]
    out += [(f"guide/{n}", None, False) for n in ("palette.svg", "palette.png", "construction.svg",
                                                   "construction.png", "clear-space.svg", "clear-space.png",
                                                   "brand-board.png")]
    return out


def png_info(p):
    """(width, height, colour type, alpha of the top-left pixel or None)."""
    with open(p, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h, depth, ctype = struct.unpack(">IIBB", data[16:26])
    idat, i = b"", 8
    while i < len(data):
        n, = struct.unpack(">I", data[i:i + 4])
        if data[i + 4:i + 8] == b"IDAT":
            idat += data[i + 8:i + 8 + n]
        i += 12 + n
    alpha = None
    if ctype == 6 and depth == 8:
        # Row 0, pixel 0: every PNG filter type leaves these bytes unchanged (there is no
        # left neighbour and no previous row), so they are the raw RGBA values.
        alpha = zlib.decompress(idat)[1 + 3]
    return w, h, ctype, alpha


def allowed_colours(rel):
    if rel == "web/social-card-ephesus.svg":
        return B.EPH_TOKENS
    for pv, v in B.PROJECT_MARK_VARIANTS.items():
        if f"-{pv}." in rel or f"-{pv}-" in rel:
            return {v["c"], v["dash"]}
    for key, spec in B.PROJECT_CARDS.items():
        if rel == f"web/social-card-{key}.svg":
            return set(B.CARD_PALETTES[spec["palette"]].values())
    for vname, v in B.VARIANTS.items():
        if f"-{vname}." in rel or rel.endswith(f"-{vname}.svg"):
            return {v["c"], v["dash"], v["text"], v["desc"]}
    if rel.startswith("web/"):
        return {B.NIGHT, B.IVORY, B.GOLD}
    return None  # guide illustrations use annotation colours


def check_svg(p, rel):
    try:
        root = ET.parse(p).getroot()
    except ET.ParseError as e:
        return fail(f"{rel}: does not parse ({e})")
    if root.find(f"{SVG_NS}title") is None:
        fail(f"{rel}: no <title>")
    if not root.get("viewBox"):
        fail(f"{rel}: no viewBox")
    tags = {el.tag.replace(SVG_NS, "") for el in root.iter()}
    for bad in ("text", "image", "use", "style", "script"):
        if bad in tags:
            fail(f"{rel}: contains <{bad}>")
    raw = open(p, encoding="utf-8").read()
    if re.search(r'href="(?!#)', raw):
        fail(f"{rel}: external reference")
    allowed = allowed_colours(rel)
    if allowed is not None:
        used = {c.upper() for c in re.findall(r'(?:fill|stroke)="(#[0-9a-fA-F]{6})"', raw)}
        extra = used - {c.upper() for c in allowed}
        if extra:
            fail(f"{rel}: colours outside its variant: {sorted(extra)}")


def hex_rgb(h):
    """(r, g, b) floats in 0..1 for a #RRGGBB palette value."""
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


# Colour operators that paint: a run of numeric operands (any whitespace between them, starting
# at a token boundary), then the operator. A name before cs/CS selects a colour space, which is
# also a change worth failing on. The other hits a text search finds in an EPS never paint: the
# prolog's `/rg {setrgbcolor} bd` alias definitions carry no operands, and the ASCII85 thumbnail
# and embedded native document sit in `%` comments, which check_eps strips.
NUM = rb"[-+]?(?:\d+\.?\d*|\.\d+)"
NUM_OP = rb"(?<![\w.+-])((?:%s\s+)+)(%s)\b" % (NUM, b"|".join(
    [b"rg", b"RG", b"g", b"G", b"k", b"K", b"sc", b"SC", b"scn", b"SCN",
     b"setrgbcolor", b"setgray", b"setcmykcolor"]))
NAME_CS = rb"/[^\s/\[\]{}()<>%]+\s+(cs|CS)\b"
# Resources that paint with colours the operator scan cannot see (sh, Do, pattern fills).
PAINT_RESOURCES = rb"/(?:ColorSpace|Shading|Pattern)\b|/Subtype\s*/Image\b"
# One stream object; its dictionary may not run past `endobj`, so /Filter is this stream's own.
STREAM = rb"\d+\s+\d+\s+obj\s*<<((?:(?!endobj).)*?)>>\s*stream\r?\n(.*?)endstream"
PDF_TOL = 1e-4  # sRGB values are 1/255 apart, so this admits rounding of the same n/255 only
EPS_TOL = 5e-5  # half a unit at the 4 decimals EPS_CMYK is recorded to: any changed digit fails


def close(a, b, tol):
    return len(a) == len(b) and all(abs(x - y) <= tol for x, y in zip(a, b))


def operands(nums):
    return " ".join(x.decode() for x in nums.split())


def pdf_streams(data, rel):
    """Decoded contents of every stream in a small PDF, except XMP metadata.

    Unfiltered streams are returned as they are and FlateDecode ones decompressed. Any other
    filter, or a stream zlib rejects, is a failure and never a silent skip: an unread stream
    could hold paint outside the palette.
    """
    out = []
    for m in re.finditer(STREAM, data, re.S):
        dct, raw = m.group(1), m.group(2)
        if re.search(rb"/Type\s*/Metadata\b", dct):
            continue  # XMP: XML text, never painted
        filt = re.search(rb"/Filter\s*(\[[^\]]*\]|/[^\s/\[\]<>]+)", dct)
        names = re.findall(rb"/([^\s/\[\]<>]+)", filt.group(1)) if filt else []
        if not names:
            out.append(raw)
        elif names == [b"FlateDecode"]:
            try:
                out.append(zlib.decompress(raw))
            except zlib.error as e:
                fail(f"{rel}: a FlateDecode stream does not decompress ({e})")
        else:
            fail(f"{rel}: a stream with filter {b' '.join(names).decode()}, which this check cannot read")
    return out


def check_pdf(p, rel):
    allowed = allowed_colours(rel)
    if allowed is None:
        return fail(f"{rel}: no variant colours known for this file")
    expected = [hex_rgb(h) for h in allowed]
    data = open(p, "rb").read()
    streams = pdf_streams(data, rel)
    painted = set()
    for stream in streams:
        for nums, op in re.findall(NUM_OP, stream):
            op = op.decode()
            vals = tuple(float(x) for x in nums.split())
            if op in ("rg", "RG") and len(vals) == 3:
                painted.add(vals)
            else:
                fail(f"{rel}: paints with {op} ({operands(nums)})")
        if re.search(NAME_CS, stream):
            fail(f"{rel}: selects a named colour space")
    found = {m.group(0).decode() for t in [data] + streams for m in re.finditer(PAINT_RESOURCES, t)}
    if found:
        fail(f"{rel}: declares {sorted(found)}, which paint outside the operators checked")
    if not painted:
        fail(f"{rel}: paints no colours")
    for rgb in sorted(painted):
        if not any(close(rgb, e, PDF_TOL) for e in expected):
            fail(f"{rel}: paints {rgb} outside its variant {sorted(allowed)}")


def check_eps(p, rel):
    allowed = allowed_colours(rel)
    if allowed is None:
        return fail(f"{rel}: no variant colours known for this file")
    unrecorded = sorted(h for h in allowed if h not in B.EPS_CMYK)
    if unrecorded:
        return fail(f"{rel}: no EPS_CMYK entry for {unrecorded}")
    data = open(p, "rb").read()
    if data[:4] != b"\xc5\xd0\xd3\xc6":
        return fail(f"{rel}: not a DOS EPS (bad magic)")
    off, ln = struct.unpack("<II", data[4:12])
    ps = data[off:off + ln].decode("latin-1")
    ps = re.sub(r"%[^\n]*", "", ps)  # comments: the ASCII85 thumbnail and embedded native document
    expected = [B.EPS_CMYK[h] for h in allowed]
    painted = set()
    for nums, op in re.findall(NUM_OP, ps.encode("latin-1")):
        op = op.decode()
        vals = tuple(float(x) for x in nums.split())
        if op == "k" and len(vals) == 4:
            painted.add(vals)
        else:
            fail(f"{rel}: paints with {op} ({operands(nums)})")
    if not painted:
        fail(f"{rel}: paints no colours")
    for cmyk in sorted(painted):
        if not any(close(cmyk, e, EPS_TOL) for e in expected):
            fail(f"{rel}: paints {cmyk} outside its variant {sorted(allowed)}")


def main():
    base = B.BRAND
    files = expected_files()
    expected = {rel for rel, _, _ in files}
    for folder in B.DIRS.values():
        for name in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
            rel = os.path.relpath(os.path.join(folder, name), base).replace(os.sep, "/")
            if rel not in expected:
                fail(f"unexpected file (stale or unlisted): {rel}")
    for rel, size, alpha in files:
        p = os.path.join(base, rel)
        if not os.path.isfile(p) or os.path.getsize(p) == 0:
            fail(f"missing or empty: {rel}")
            continue
        if rel.endswith(".svg"):
            check_svg(p, rel)
        elif rel.endswith(".png"):
            info = png_info(p)
            if info is None:
                fail(f"{rel}: not a PNG")
                continue
            w, h, ctype, corner = info
            if size and (w, h) != size:
                fail(f"{rel}: {w}x{h}, expected {size[0]}x{size[1]}")
            if alpha and (ctype != 6 or corner != 0):
                fail(f"{rel}: not transparent (colour type {ctype}, top-left alpha {corner})")
    report("files, SVG hygiene and PNG sizes", len(files))

    n = 0
    for rel, _, _ in files:
        p = os.path.join(base, rel)
        if not os.path.isfile(p):
            continue
        if rel.endswith(".pdf"):
            check_pdf(p, rel)
            n += 1
        elif rel.endswith(".eps"):
            check_eps(p, rel)
            n += 1
    report("PDF and EPS colours", n)

    ratios = [("on-light text: Night on Ivory", B.NIGHT, B.IVORY, 4.5),
              ("on-light descriptor text: Bronze on Ivory", B.BRONZE, B.IVORY, 4.5),
              ("on-light dashes: Bronze on Ivory", B.BRONZE, B.IVORY, 3.0),
              ("on-dark text: Ivory on Night", B.IVORY, B.NIGHT, 4.5),
              ("on-dark descriptor text: Gold on Night", B.GOLD, B.NIGHT, 4.5),
              ("on-dark dashes: Gold on Night", B.GOLD, B.NIGHT, 3.0),
              ("black on white", B.BLACK, B.WHITE, 4.5), ("white on black", B.WHITE, B.BLACK, 4.5),
              ("red-figure card text: Clay on Kiln", B.CLAY, B.KILN, 4.5),
              ("red-figure card dashes: Terracotta on Kiln", B.TERRACOTTA, B.KILN, 3.0),
              ("red-figure card kicker (large text, at least 24 px): Terracotta on Kiln", B.TERRACOTTA, B.KILN, 3.0),
              ("red-figure mark on light: Kiln on GitHub white", B.KILN, GITHUB_LIGHT, 3.0),
              ("red-figure mark on light: Terracotta on GitHub white", B.TERRACOTTA, GITHUB_LIGHT, 3.0),
              ("red-figure mark on dark: Clay on GitHub dark", B.CLAY, GITHUB_DARK, 3.0),
              ("red-figure mark on dark: Terracotta on GitHub dark", B.TERRACOTTA, GITHUB_DARK, 3.0),
              ("Ephesus card text: ink-900 on marble-100", B.EPH_INK900, B.EPH_MARBLE100, 4.5),
              ("Ephesus card kicker and footer: ink-700 on marble-100", B.EPH_INK700, B.EPH_MARBLE100, 4.5),
              ("Ephesus card rule: terracotta on marble-100", B.EPH_TERRACOTTA, B.EPH_MARBLE100, 3.0)]
    for name, a, b, target in ratios:
        r = contrast(a, b)
        print(f"  {name}: {r:.2f}:1 (target {target}:1)")
        if r < target:
            fail(f"contrast {name} {r:.2f} < {target}")
    report("WCAG contrast", len(ratios))

    for geo_name, geo in (("FULL", B.FULL), ("SMALL", B.SMALL)):
        edges = [-geo["gap"]] + [a for pair in geo["dashes"] for a in pair] + [geo["gap"]]
        spaces = [edges[i + 1] - edges[i] for i in range(0, len(edges), 2)]
        dashes = [a1 - a0 for a0, a1 in geo["dashes"]]
        total = sum(spaces) + sum(dashes)
        print(f"  {geo_name}: dashes {dashes}, spaces {spaces}, sum {total} = opening {2 * geo['gap']}")
        if total != 2 * geo["gap"] or min(spaces) <= 0 or len(set(spaces)) != 1:
            fail(f"{geo_name}: dashes and spaces do not tile the opening evenly")
    report("mark geometry", 2)
    print("ALL CHECKS PASSED")


def report(group, n):
    if failures:
        print(f"FAIL {group}:")
        for f in failures:
            print("  " + f)
        sys.exit(1)
    print(f"ok   {group} ({n} checked)")


if __name__ == "__main__":
    main()
