# 2026-10-14 · CASSANDRA brand identity (the Forecast mark)

| | |
|---|---|
| Repository | `Cassandra-Collective/.github` (organisation profile and brand home) |
| Branch | `brand/cassandra-identity` |
| Status | Verified on 2026-10-14 (VectorCraft 0.10.0, Python 3.12.10, Windows 11). Tagline choice pending with the owner. |

Project prose style: no em or en dashes.

## Problem / Motivation

The organisation that hosts CASSANDRA, CASSANDRA-Chorus, Ephesus and Dervish (renamed from `CASANDRA-Lab` to `Cassandra-Collective` on 2026-10-14) had no official logo. The owner asked for one inspired by Kassandra of Greek myth, drawn in VectorCraft, and set out requirements in two briefs:

1. Simplicity, significance, ingenuity, uniqueness, and "beauty is not enough to sell".
2. A professional checklist:
   - legible from a 16 px favicon to a billboard, and in one solid colour;
   - every choice justified by the brand;
   - two to four colours with hex codes and checked contrast;
   - at most two typefaces;
   - horizontal, stacked and icon lockups;
   - production-ready vector and raster files.

Without a mark, the organisation page, repositories, slides and papers show nothing recognisable, and each project improvises its own image.

## What Changed

| File | Description |
|---|---|
| `brand/tools/build_brand.py` | Generator: draws every asset in VectorCraft from exact geometry and exports all formats. |
| `brand/tools/check_brand.py` | Checks every built file against the specification and exits non-zero on any failure. |
| `brand/tools/vcdriver.py` | Minimal stdio MCP client for VectorCraft's headless engine (`vectorcraft-cli mcp --headless`). |
| `brand/tools/wcag.py` | WCAG 2.x relative luminance and contrast ratio. |
| `brand/svg/` (20 files) | Mark, small mark, horizontal, compact and stacked lockups, each in `on-light`, `on-dark`, `black` and `white`. Text as outlines. |
| `brand/png/` (68 files) | The same with transparent backgrounds: marks at 64 to 1024 px, small marks at 16 to 32 px, lockups at 1x, 2x and 4x. |
| `brand/pdf/`, `brand/eps/` (16 files each) | Marks and the three lockups in every variant, for print. |
| `brand/web/` (17 files) | Favicon (SVG and 16, 32, 48 px), app icon (180, 192, 512 px), organisation avatar (500, 1024 px), three social cards (1280×640). |
| `brand/source/` (26 files) | Gzip-compressed `.vectorcraft` document behind each deliverable. |
| `brand/guide/` (7 files) | Palette, construction and clear-space figures and the brand board, used by the guide. |
| `brand/README.md` | Brand guide: idea, construction, lockups, clear space, minimum sizes, colour, typography, files, misuse, taglines. |
| `profile/README.md` | Organisation profile page: stacked lockup, tagline, the four projects, how we work. |
| `README.md` | What this repository is, and the visibility caveat for the profile. |
| `.gitattributes`, `.gitignore` | LF line endings, binary assets left untouched, Python caches ignored. |
| `docs/implementations/_TEMPLATE.md` | Implementation doc template from the owner's global standards. |
| `docs/implementations/2026-10-14-cassandra-brand-identity.md` | This document. |

## Implementation Approach

**Tool.** VectorCraft 0.10.0 is driven headlessly via its own MCP server (`vectorcraft-cli mcp --headless`). The automation is confined to one read root and one write root, the repository's `brand/` folder. Every asset is built in its own VectorCraft document, exported, saved as `.vectorcraft`, and closed. That keeps each export isolated: the EPS exporter always embeds the whole native document, so a shared multi-artboard file would leak every asset into every EPS.

**Reproducibility.** Nothing is drawn by hand. The geometry is a table of numbers in `build_brand.py`, so re-running the script reproduces every file. The `.vectorcraft` sources are for people who want to edit in the app; the script remains the reference.

**Mark construction.** All values are in units of the mark's outer diameter D:

- **The C.** An annular sector with outer radius 0.5 D and inner radius 0.32 D. The ring is 0.18 D thick. It spans 50° to 310°, so the opening is 100° and faces right, the reading direction.
- **The forecast.** Three annular sectors on the ring's mid-line, from radius 0.365 D to 0.455 D (half the ring's thickness). They sit at -37° to -21°, -8° to 8° and 21° to 37°: each 16° long, with 13° spaces between them and at both ends.
- **Small mark** (24 px and below, redrawn rather than scaled):
  - the ring runs from 0.30 D to 0.5 D;
  - the opening is ±52°;
  - a single sector from 0.325 D to 0.475 D at ±17°.

  The three dashes merge into grey at 16 px (observed in the 2026-10-14 size test), so the forecast is reduced to its first step: the next token.

**Lockups**, in units of the mark height H. The compact horizontal lockup was added during implementation, once the minimum sizes were worked out; see the Design Decisions.

- **Horizontal.** The mark, then a gap of 0.30 H from the ring's right edge. Then the wordmark "CASSANDRA", 0.30 H letter height, over the descriptor "COLLECTIVE", 0.095 H letter height, with 0.11 H between them. Letter height is the measured height of the outlined letters: cap height plus the overshoot of the round letters. The text block is centred vertically on the mark's centre. The descriptor is left-aligned with tracking +350. Tracking it to the wordmark's full width was planned, but the arithmetic gave a space of about two letter heights between letters, too sparse to read as one word.
- **Stacked.** Mark on top. Then 0.24 H, the wordmark at 0.20 H letter height, 0.085 H, and the descriptor at 0.068 H letter height, tracking +350. All centred on the mark's axis.
- **Compact horizontal.** The mark, 0.30 H, then the wordmark alone, 0.34 H letter height, centred on the mark's centre line.
- **Icon.** The mark alone, centred on the ring's centre (not its bounding box, which the dashes make asymmetric).

**Text.** Set in VectorCraft with its bundled open-licence fonts, then converted to outlines, so no file needs the fonts installed.

**Exports per asset.**

- Colour variants, as fitting:
  - colour on light: night C, bronze dashes, night text;
  - colour on dark: ivory C, gold dashes, ivory text;
  - solid black, solid white.
- Formats: SVG (outlined, artboard as viewBox), PDF (`preserveEditing` off), EPS, and PNG with a transparent background at the sizes listed in the guide.
- Also a favicon set, a 1024 px organisation avatar, and three 1280×640 social cards, one per tagline candidate.

## Mathematical / Statistical Details

**Contrast** follows WCAG 2.x.

- **Relative luminance** of an sRGB colour with 8-bit channels R, G, B: each channel becomes c = v / 255, then is linearised as c_lin = c / 12.92 if c ≤ 0.04045, else ((c + 0.055) / 1.055)^2.4. Then L = 0.2126 R_lin + 0.7152 G_lin + 0.0722 B_lin.
- **Contrast ratio** between colours with luminances L1 ≥ L2: (L1 + 0.05) / (L2 + 0.05). It ranges from 1 to 21.
- **Targets:**
  - text colours at least 4.5:1 against their ground (WCAG 1.4.3, level AA for normal text);
  - graphical parts of the mark at least 3:1 (WCAG 1.4.11, non-text contrast).
- **Accent tuning.** An accent that serves both grounds must satisfy (L_light + 0.05) / (L_acc + 0.05) ≥ 4.5 and (L_acc + 0.05) / (L_dark + 0.05) ≥ 3. That holds only in a narrow luminance band: for ivory (L = 0.8668) and night (L = 0.0116), L_acc must lie between 3 × (0.0116 + 0.05) − 0.05 = 0.1347 and (0.8668 + 0.05) / 4.5 − 0.05 = 0.1537.
  - Bronze `#8A672B` (L = 0.1528) sits in that band: 4.52:1 on ivory and 3.29:1 on night.
  - Gold `#D2A65A` is the brighter accent for dark grounds only: 7.59:1 on night, 1.96:1 on ivory. It must never be used on ivory.
- **Minimum sizes.** A text line of letter height f × H stays legible while f × H ≥ m, where m is 6 px or 1.5 mm for the descriptor and 7 px or 2 mm for the wordmark. So H ≥ m / f, and the lockup's minimum width is (W / H) × m / f.
  - Horizontal: W/H = 4.255, f = 0.095, so 269 px and 67.2 mm, stated as 270 px and 68 mm.
  - Compact: W/H = 4.649, f = 0.34, so 96 px and 27.4 mm, stated as 100 px and 28 mm.
  - Stacked: W/H = 1.970, f = 0.068, so 174 px and 43.5 mm, stated as 175 px and 44 mm.
- **Dash geometry.** Three dashes of 16° and four spaces of 13° fill the 100° opening exactly: 3 × 16 + 4 × 13 = 100.

## Design Decisions

| Decision | Alternatives considered | Why | Who |
|---|---|---|---|
| Concept "Forecast": a C (the known past) closed by dashes (the prediction). | "Serpent" (the temple serpents that gave Kassandra her gift) and "Foretold" (the missing arc drawn ahead). All three were rendered on one comparison sheet at full size, reversed, 32 px and 16 px. | The clearest link between the myth (prophecy) and the work (language models predict the next token). Dashes are the universal chart notation for a forecast, so the prediction is honestly marked as a prediction, which answers Kassandra's curse. | Owner, 2026-10-14 |
| No eye motif. | An eye is the obvious Kassandra symbol. | Apache Cassandra's logo is an eye (checked 2026-10-14 on Wikimedia Commons); an eye would fail the uniqueness requirement. | Engineering, stated to owner |
| Palette "Bronze and night" for the organisation. | "Red-figure" (kiln black, terracotta, clay ivory) and "Laurel" (ink, laurel green, parchment), rendered side by side with contrast ratios. | Owner's choice. Red-figure is reserved for a possible CASSANDRA-Chorus or CASSANDRA project mark. | Owner, 2026-10-14 |
| Two accent tones (bronze on light, gold on dark). | One accent for both grounds. | A single gold that passes both contrast targets is a dull brown; see the maths above. | Engineering, stated to owner |
| Typefaces: Source Serif 4 (wordmark) and Inter (descriptor, taglines, guide). | Perpetua Titling, Castellar and other installed system fonts. | Both are under the SIL Open Font License 1.1, which allows outlining in a logo and redistribution with the files. Microsoft- and Monotype-licensed system fonts are a grey area for a public repository. The serif carries the classical inscription tone; the sans carries the technical one. | Engineering, stated to owner |
| Organisation name `Cassandra-Collective`, descriptor COLLECTIVE. | The-Cassandra-Lab, Cassandra-Foresight, Kassandra-Lab (all free on GitHub on 2026-10-14). `CASSANDRA-Lab` was taken by a user account `cassandra-lab` (created 2025-04-02; GitHub logins are case-insensitive). | Owner's choice. "Collective" says many people, one model: the volunteer pool. | Owner, 2026-10-14 |
| Tagline: three candidates rendered as social cards. | | The owner asked to see all three before choosing. | Owner, pending |
| A separate small mark for 24 px and below. | Scaling the full mark down. | The 16 px render of the full mark turns the dashes into grey noise. This follows the earlier project-marks rule: redraw small sizes, don't resize. | Engineering |
| A compact horizontal lockup (no descriptor). | Only the three lockups the brief names. | The descriptor sets the horizontal lockup's minimum at 270 px and 68 mm. Without a compact version, anything smaller would have to fall back to the bare mark and lose the name. | Engineering, stated to owner |
| Every asset in its own VectorCraft document. | One master document with an artboard per asset. | The EPS exporter embeds the whole native document, so a shared document would put every asset inside every EPS. | Engineering |
| Files in `Cassandra-Collective/.github`. | The CASSANDRA repo, Chorus, a Desktop folder. | The logo belongs to the organisation, not to one project. The owner created the repository. | Owner, 2026-10-14 |

## Verification

All runs on the owner's laptop (Windows 11 Home 10.0.26300), VectorCraft 0.10.0 (`vectorcraft-cli`, headless MCP server), Python 3.12.10, standard library only.

1. **Build.** `python brand/tools/build_brand.py` from the repository root prints `done` and writes 170 files in about 10 to 20 seconds.
2. **Check.** `python brand/tools/check_brand.py` printed:
   - `ok files, SVG hygiene and PNG sizes (170 checked)`
   - `ok WCAG contrast (8 checked)`
   - `ok mark geometry (2 checked)`
   - `ALL CHECKS PASSED`, exit 0

   The 170 are every file the build writes. The contrast lines are the ratios quoted in the guide: 14.89, 4.52, 7.59 and 21.00.
3. **The check can fail.** Three deliberately broken copies of `cassandra-mark-on-light.svg` were each caught: one with a `<text>` element, one with a colour outside the variant (`#FF0000`), one with no `<title>`.
4. **Reproducibility.** Two complete builds from empty output folders were compared by SHA-256:
   - All 29 SVGs are byte-identical.
   - The 83 PNGs differ only in a `Creation Time` text chunk: decompressed pixel data and every other chunk are identical in all 83.
   - PDF, EPS and `.vectorcraft` files carry creation dates and were not compared further.
5. **Visual review.** Each step's output was looked at:
   - the concept sheet;
   - the palette sheet (three directions);
   - the small-size test (16, 24, 32 and 48 px for full, two-dash and one-dash variants);
   - the brand board, the construction, palette and clear-space figures;
   - the compact lockup and social card A.

   The construction figure's first version had colliding labels and the palette figure printed meaningless 1.00:1 ratios. Both were fixed and re-checked.
6. **Prose.** A scan of every `.md` and `.py` file found no em or en dashes.

**Not tested:**

- How the files render on GitHub. The repository is private and nothing has been pushed. That includes whether `profile/README.md` resolves its relative image paths on the organisation page.
- Print. No physical proof of the CMYK conversion, and Night is slightly outside the SWOP-like gamut (ΔE 3.4).
- Opening the PDF and EPS files in third-party software, and opening the `.vectorcraft` sources in the VectorCraft desktop app (only the headless engine wrote them).
- Favicon behaviour in real browsers.
- A registered-trademark search for the name. Only the visual uniqueness against Apache Cassandra's logo was checked.

## Related Docs

- Brand guide: [`brand/README.md`](../../brand/README.md)
- Earlier reference marks (not shipped): the owner's local `project-marks/README.md`, which holds the "streak into an open question" Cassandra mark of the dropped Mihenk umbrella. The Forecast mark continues its idea of a solid stroke resolving into a prediction.
