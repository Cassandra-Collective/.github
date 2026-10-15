# 2026-10-15 · The Ephesus social card, built in VectorCraft in Ephesus's own identity

| | |
|---|---|
| Repository | `Cassandra-Collective/.github`, plus `Cassandra-Collective/Ephesus` (its own pull request) |
| Branch | `brand/ephesus-card` |
| Status | Verified on 2026-10-15 (VectorCraft 0.10.0, Python 3.12.10, Windows 11) |

Prose style: no em or en dashes.

## Problem / Motivation

The project repositories have social cards built here: CASSANDRA, CASSANDRA-Chorus and Dervish. Ephesus had a hand-drawn card of its own. That card names the old address (`github.com/mertefesensoy/Ephesus`, Ephesus issue #80), and it carries the old pitch, "an agent company you govern as its architect".

On 2026-10-15 the owner asked for a new Ephesus card made with the same app (VectorCraft) and decided, through the questions workflow:
- **The pitch** follows Phase 9 (`docs/PHASE-9-PLAN.md` in Ephesus): "An agentic harness you govern and measure" and "Every agent works behind your gates; the harness is scored by its own bench."
- **Honesty:** the pitch states the identity, and each status line says what is real (Phase 9 is approved for planning only).
- **Address:** both `ephesushq.com` and `github.com/Cassandra-Collective/Ephesus`.
- **Design:** card A, the Collective's project-card layout drawn entirely in Ephesus's identity, chosen over B (today's card refreshed) after both were rendered.
- **Headline face:** IBM Plex Mono, not Press Start 2P.
- **Placement:** this repository, and Ephesus's own files.

## What Changed

| File | Description |
|---|---|
| `brand/tools/build_brand.py` | Several additions: the Ephesus constants (tokens, faces, pitch, integer layout), `require_fonts()`, `live_text()`, `ephesus_svg()` (normalise and check Ephesus's copy), `build_ephesus_card()`, and a `--ephesus-out <checkout>` option. |
| `brand/tools/ephesus_artwork.json` | Ephesus's column master (29 rects, a 64-unit grid) and pixel wordmark (113 cells of 13 px), copied from its card at commit `4e3779a`, with the source recorded. |
| `brand/tools/install_ephesus_fonts.py` | Converts Ephesus's IBM Plex Mono WOFF2 files (Regular, Medium) to TrueType and installs them through VectorCraft. |
| `brand/tools/check_brand.py` | Expects the Ephesus card's three files, allows exactly the 7 Ephesus tokens in its SVG, and adds three contrast checks. |
| `brand/web/social-card-ephesus.{svg,png}`, `brand/source/social-card-ephesus.vectorcraft` | The card, with text outlined. |
| `brand/README.md` | A new section, "The Ephesus card"; the social-card table and the files table name it; "Rebuilding" mentions the fonts. |
| `docs/implementations/2026-10-15-ephesus-social-card.md` | This document. |

In Ephesus, written by `--ephesus-out` and committed through its own pull request: `docs/brand/ephesus-social-card.svg`, `site/public/img/social-card.svg` and `site/public/img/social-card.png`.

## Implementation Approach

**Ephesus's design rules bind the card** (`docs/design/UI-DESIGN.md` and `docs/brand/README.md` in Ephesus):
- only the section 2 colour tokens, at most 8 per screen;
- integer coordinates;
- crisp edges;
- light from the upper left;
- only its three faces.

The card uses 7 tokens:

| Token | Hex |
|---|---|
| ink-900 | `#221A14` |
| ink-700 | `#4A3B2C` |
| marble-100 | `#F4EDE0` |
| marble-200 | `#E7DCC6` |
| marble-300 | `#D3C4A5` |
| terracotta | `#C4552D` |
| terracotta-light | `#E8A987` |

It uses one face, IBM Plex Mono: Regular for the pitch line and footer, Medium for the kicker and headline.

**Artwork as data.** The column (Ephesus's 64-unit master, drawn at an integer 6x) and the pixel wordmark (113 cells of 13 px) are copied rect for rect from Ephesus's card at commit `4e3779a` into `brand/tools/ephesus_artwork.json`, with their source recorded (Ephesus is MIT). The build does not need an Ephesus checkout for the artwork.

**Fonts.** VectorCraft does not bundle IBM Plex Mono, and its font search skips web fonts. `brand/tools/install_ephesus_fonts.py` converts Ephesus's own `site/public/fonts/ibm-plex-mono-{400,500}-latin.woff2` (SIL OFL 1.1) to TrueType with fontTools. It then installs them with VectorCraft's `text.findFontFiles` and `text.addFontFiles`, into VectorCraft's Fonts folder (`%APPDATA%\VectorCraft\Fonts`). The Medium face registers as its own family, "IBM Plex Mono Medium". The build checks that both families exist and stops with instructions if not, so it can never fall back silently to another face. The fonts are not redistributed here.

**Layout, card A** (1280 by 640, all integers):
- an ink-900 field with a marble-100 panel inset by 8;
- the column, unboxed, centred on (290, 320) like the other project cards' mark;
- a text column from x = 520, 533 wide (the wordmark's width):
  - kicker "A CASSANDRA COLLECTIVE PROJECT";
  - the wordmark;
  - a terracotta rule;
  - the headline;
  - the two-line pitch;
  - the status and the two addresses.

The build fails if any text line is wider than the column.

**Two outputs.**
- **This repository** (`brand/web/social-card-ephesus.{svg,png}`, `brand/source/social-card-ephesus.vectorcraft`): text outlined, as every SVG here is, so the checker's no-live-text rule holds.
- **Ephesus** (`python brand/tools/build_brand.py --ephesus-out <Ephesus checkout>`): writes `docs/brand/ephesus-social-card.svg`, `site/public/img/social-card.svg` and `site/public/img/social-card.png`. The SVG keeps live text, as Ephesus's card always has, because outlined glyphs would put curves into a file whose rules forbid them. VectorCraft's export is normalised deterministically:
  - colours upper case, matching the token table;
  - font families rewritten to `'IBM Plex Mono','DejaVu Sans Mono',monospace`, with `font-weight="500"` for the Medium face;
  - `shape-rendering="crispEdges"`, `role="img"` and an `aria-label` on the root.

  The build then checks the result: only the 7 tokens, and no fractional coordinate.

## Mathematical / Statistical Details

**Contrast** (WCAG 2.x, `tools/wcag.py`):
- the headline and pitch are ink-900 on marble-100;
- the kicker and footer are ink-700 on marble-100, at least 4.5:1;
- the rule is terracotta on marble-100, at least 3:1 (graphics).

**Width.** IBM Plex Mono advances 600/1000 em per character. At 21 px the 41-character headline is 41 x 12.6 = 516.6 px, inside the 533 px column. The build measures the real widths rather than trusting this.

## Design Decisions

| Decision | Alternatives | Why | Who |
|---|---|---|---|
| Card A, the Collective layout in Ephesus's identity | B, today's card refreshed (both rendered) | It reads as one family with the other project cards and still obeys Ephesus's rules | Owner, 2026-10-15 |
| The Phase 9 pitch, honest about status | "The harness is the product"; "An agent company on a harness you can measure" | Names the Phase 9 difference: governed agents and a measured harness | Owner, 2026-10-15 |
| Both addresses | One of them | Owner's choice. Settles Ephesus #80 | Owner, 2026-10-15 |
| IBM Plex Mono headline | Press Start 2P | The pixel wordmark already carries the display role; Press Start 2P at that length is very wide | Owner, 2026-10-15 |
| Artwork vendored as data | Reading an Ephesus checkout at build time | The brand build stays self-contained; the source is recorded | Engineering |
| Live text in Ephesus's SVG, outlined text here | Outlined everywhere | Each file follows its own repository's rules | Engineering |

## Verification

1. **Fonts installed.** `install_ephesus_fonts.py`'s steps were run by hand. They installed `IBMPlexMono-Regular.ttf` and `IBMPlexMono-Medium.ttf` into `%APPDATA%\VectorCraft\Fonts`. `text.fontList` then lists the families "IBM Plex Mono" and "IBM Plex Mono Medium" (style Regular each).
2. **Build.** `python brand/tools/build_brand.py --ephesus-out <Ephesus checkout>` printed the measured line widths:

   | Line | Width (px) |
   |---|---|
   | Kicker | 345.6 |
   | Headline | 516.6 |
   | Pitch, first line | 453.6 |
   | Pitch, second line | 491.4 |
   | Status and site | 334.8 |
   | GitHub address | 421.2 |

   All are inside the 533 px column. The headline matches the monospace arithmetic exactly (41 x 12.6). The build wrote the three Ephesus files and left no temporary folder behind.
3. **Check.** `python brand/tools/check_brand.py` printed:
   - `ok files, SVG hygiene and PNG sizes (204 checked)`;
   - `ok WCAG contrast (18 checked)`, including ink-900 on marble-100 at 14.71:1, ink-700 at 9.23:1, and the terracotta rule at 3.85:1;
   - `ok mark geometry (2 checked)`;
   - `ALL CHECKS PASSED`.
4. **Ephesus's own checks** (from its `docs/brand/README.md`), run in the Ephesus checkout:
   - `grep -ohE '#[0-9A-Fa-f]{6}' docs/brand/*.svg | sort -u` gives exactly the 7 tokens, each found in `docs/design/UI-DESIGN.md`.
   - The fractional-coordinate grep prints nothing.
   - The new SVG parses as XML.
   - Its root carries `shape-rendering="crispEdges"`, `role="img"` and the new `aria-label`.
   - `site/public/img/social-card.svg` is byte-identical to `docs/brand/ephesus-social-card.svg`.
5. **Visual review.** Before the owner chose, cards A and B were rendered and looked at. After the build, the Ephesus PNG (live text) and `web/social-card-ephesus.png` (outlined) were looked at; they match each other and the approved A.

**Not tested:** how GitHub and social platforms show the card. That happens after the owner uploads it as Ephesus's social preview and the site is deployed. The live-text SVG renders IBM Plex Mono only where that face is available, as the previous card did; elsewhere it falls back to DejaVu Sans Mono or monospace.

## Related Docs

- `brand/README.md`, "Social cards"
- `2026-10-14-project-cards-and-org-move.md`
- Ephesus: `docs/design/UI-DESIGN.md`, `docs/brand/README.md`, `docs/PHASE-9-PLAN.md`, issue #80
