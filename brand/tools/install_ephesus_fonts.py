"""Install the IBM Plex Mono faces the Ephesus card needs into VectorCraft.

Usage:
    python brand/tools/install_ephesus_fonts.py <path to an Ephesus checkout>

Needs a Python with fontTools and brotli (for WOFF2), and VectorCraft 0.10 or later.

What it does, and nothing else:
  1. Reads site/public/fonts/ibm-plex-mono-400-latin.woff2 and -500-latin.woff2 from the
     Ephesus checkout (IBM Plex Mono, SIL Open Font License 1.1; Ephesus ships them for its
     website).
  2. Converts them to TrueType in a temporary folder, because VectorCraft's font search
     reads .ttf/.otf files only.
  3. Asks VectorCraft to install them (text.findFontFiles, then text.addFontFiles). That copies
     them into VectorCraft's own Fonts folder (%APPDATA%\\VectorCraft\\Fonts on Windows), never
     replacing a file there. Remove them from that folder to uninstall.

The Medium face registers as its own family, "IBM Plex Mono Medium" (style Regular), next to
"IBM Plex Mono" (Regular). build_brand.py checks for both.
"""
import os
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vcdriver import VC  # noqa: E402

FACES = [("400", "IBMPlexMono-Regular", "IBM Plex Mono"), ("500", "IBMPlexMono-Medium", "IBM Plex Mono Medium")]


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if len(sys.argv) == 2 else 2)
    from fontTools.ttLib import TTFont  # imported here so --help works without fontTools

    src = os.path.join(sys.argv[1], "site", "public", "fonts")
    with tempfile.TemporaryDirectory() as tmp:
        for weight, name, _ in FACES:
            font = TTFont(os.path.join(src, f"ibm-plex-mono-{weight}-latin.woff2"))
            font.flavor = None
            font.save(os.path.join(tmp, name + ".ttf"))
        with VC(tmp) as vc:
            vc.cmd("text.findFontFiles", folder=tmp,
                   fonts=[{"family": family, "style": "Regular"} for _, _, family in FACES])
            for _ in range(60):
                state = vc.cmd("text.findFontFiles")
                if state.get("state") != "searching":
                    break
                time.sleep(1)
            files = sorted({f for font in state.get("fonts", []) for f in font.get("files", [])})
            if files:
                result = vc.cmd("text.addFontFiles", files=files)
                for item in result.get("copied", []) + result.get("kept", []):
                    print("installed:", item["to"])
            for _, _, family in FACES:
                print(family, "->", vc.cmd("text.fontList", family=family)["styles"])


if __name__ == "__main__":
    main()
