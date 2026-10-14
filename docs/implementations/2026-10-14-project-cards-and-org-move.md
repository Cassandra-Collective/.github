# 2026-10-14 · Project social cards, and the follow-up to the move into the organisation

| | |
|---|---|
| Repository | `Cassandra-Collective/.github`, plus the other repositories as listed |
| Branch | `brand/project-cards` |
| Status | Verified on 2026-10-14 (VectorCraft 0.10.0, Python 3.12.10, Windows 11) |

Prose style: no em or en dashes.

## Problem / Motivation

The organisation had a logo, but every project still showed GitHub's generic link preview, and three of the four project repositories had no description at all (CASSANDRA's read just "CASSANDRA"). After the move from the personal account, about 160 links across the repositories still named `github.com/mertefesensoy/...`, and the four local checkouts still pushed to the old URLs.

The owner asked, on 2026-10-14, for:
- the old links fixed in every repository;
- the repository descriptions set;
- a social card per repository;
- topics, homepage links, a README header and pinned repositories.

The uploads and the pins are left to the owner, because GitHub only offers them in its web settings.

## What Changed

In this repository:

| File | Description |
|---|---|
| `brand/tools/build_brand.py` | The Red-figure colours; `CARD_PALETTES`, `PROJECT_CARDS`, `KICKER`, `CARD` and `build_project_cards()`: one 1280×640 card per project repository, each in its project's palette. The build fails if any text line is wider than the 650 px text column, or if a kicker colour below 4.5:1 is set under 24 px. |
| `brand/tools/check_brand.py` | Expects the 9 new files (SVG, PNG and source of each card). Each card may use only its own palette's colours. Three Red-figure contrast checks are added. |
| `brand/web/social-card-{cassandra,chorus,dervish}.{svg,png}`, `brand/source/social-card-*.vectorcraft` | The three cards, 30 to 37 KB each. |
| `brand/README.md` | A "Social cards" section: which card and palette goes on which repository, the layout, why the kicker is large text, and the upload path. "Projects" records Red-figure as the palette of CASSANDRA and CASSANDRA-Chorus. The files table lists the new cards. |
| `docs/implementations/2026-10-14-project-cards-and-org-move.md` | This document. |

Elsewhere, the same day:

**Pull requests:**

| Repository | Change | Pull request |
|---|---|---|
| CASSANDRA | 7 links in 4 files; README header | CASSANDRA#1 |
| CASSANDRA-Chorus | 100 links in 10 files; backlog `repo` field; decision D46; README header | CASSANDRA-Chorus#112 (issue #111) |
| Dervish | 1 link (`pyproject.toml`); README header | Dervish#1 |
| Ephesus | 52 links in 22 files; its two social-card SVGs held back (see below) | Ephesus#79 (issue #78) |

**Repository settings (applied directly, read back afterwards):**

| Repository | Description | Homepage | Topics |
|---|---|---|---|
| CASSANDRA | Set | Hugging Face model page (kept) | 9 |
| CASSANDRA-Chorus | Set | The organisation page | 8 |
| Dervish | Set | The organisation page | 8 |
| `.github` | Set | The organisation page | 4 |
| Ephesus | Unchanged | Unchanged | Unchanged |

**Local checkouts:** the `origin` of the owner's four Desktop checkouts (CASSANDRA, CASSANDRA Chorus, Dervish, ephesus) now points at `github.com/Cassandra-Collective/...`.

## Implementation Approach

**Cards.** Each card is drawn by the same VectorCraft session as the rest of the brand, in its project's palette:
- CASSANDRA and CASSANDRA-Chorus use Red-figure: kiln black ground, clay ivory ring and text, terracotta dashes and kicker.
- Dervish uses Bronze and night: night ground, ivory ring and text, gold dashes and kicker.

Each card has:
- the mark, 300 px, centred at (290, 320);
- a kicker "CASSANDRA COLLECTIVE" in Inter Medium, tracking +350, letters 19 px tall (a font size of about 25.3 px);
- the project name in the wordmark's setting (Source Serif 4, capitals, tracking +160), letters 62 px tall, one line per word group;
- the card line in Inter Regular 32 px, on lines broken by hand.

The text block starts at x = 520 and is centred vertically on the card.

The card lines are the short forms of the descriptions. The owner saw them as an alternative when approving the descriptions, and chose the long forms for the repositories. The card can't hold a 200-character sentence, so the cards use the short forms.

**Links.** One script (`relink.py`, kept outside the repositories) replaces exactly `github.com/mertefesensoy/(CASSANDRA|CASSANDRA-Chorus|Ephesus|Dervish)` with the organisation's path in every tracked text file, then re-greps. A second grep for the bare account name found Chorus's backlog `repo` field, which was changed by hand. Left alone everywhere:
- Hugging Face paths;
- other repositories under the personal account;
- test fixtures;
- dated records of where something ran.

**README header.** Each project README has a one-line header: the small mark (20 px, loaded from this repository's `brand/svg`) and "Part of the Cassandra Collective". The markup was checked on GitHub, in light and dark mode, before it was copied to the second and third repositories.

## Mathematical / Statistical Details

**Card layout.** The text block's height is

  h = k + g₁ + n + s_n (N − 1) + g₂ + t + s_t (L − 1),

where:
- k = 19 is the kicker's letter height;
- g₁ = 30 and g₂ = 40 are the gaps;
- n = 62 is the name's letter height, with step s_n = 1.45 n over N name lines;
- t is the measured height of a card-line glyph run, with step s_t = 1.4 × 32 over L lines.

The block's top is placed at 320 − h / 2.

**Kicker size and contrast.** Terracotta on kiln black is 3.30:1. WCAG requires 4.5:1 for normal text but only 3:1 for large text (24 px and up). The kicker's font size is computed from its letter height: an outline set at 100 px is measured, with height h₁₀₀, and the font size is 100 × 19 / h₁₀₀. That came to 25.3 px, so it qualifies as large text. The build asserts it on every card.

**Ephesus card.** The new URL does not fit the Ephesus card's text column. At 18 px in IBM Plex Mono (0.6 em per character), the 57-character line "pre-alpha · MIT · github.com/Cassandra-Collective/Ephesus" is 57 × 10.8 = 615.6 px. Starting at x = 620, it would end near x = 1236, about 107 px past the wordmark and rule (x ≈ 1129) that every other line on that card aligns to.

## Design Decisions

| Decision | Alternatives | Why | Who |
|---|---|---|---|
| A card per repository | The organisation card everywhere | Owner's choice | Owner, 2026-10-14 |
| Red-figure cards for CASSANDRA and CASSANDRA-Chorus; Bronze and night for Dervish | Bronze and night everywhere | The owner reserved Red-figure for those two projects when choosing the palettes, and confirmed it for these cards | Owner, 2026-10-14 |
| Kicker at about 25 px on every card | Clay kicker on the Red-figure cards; different kicker sizes per palette | Keeps terracotta as the accent and one layout for all cards, while meeting WCAG large-text contrast | Engineering |
| The owner uploads the cards and pins the repositories | Driving the owner's signed-in Chrome | Owner's choice. These are account settings with no API. | Owner, 2026-10-14 |
| Ephesus's cards keep the old URL for now | Shrinking the text, or showing ephesushq.com | A layout change belongs to Ephesus's own design system, not to a link fix | Engineering, stated in Ephesus#79 |
| Chorus PR stacked on #110, plus issue #111 and D46 | Basing it on `main`; no issue | #110 added 91 of the links and D42 to D45. Chorus's D45 requires an issue per PR. | Engineering, stated in the PR |
| The README header loads the mark from this repository by URL | A copy of the SVG in each repository | One source for the mark; the cost is that the header depends on this repository staying public | Engineering |

## Verification

1. **Build and check.** `python brand/tools/build_brand.py`, then `python brand/tools/check_brand.py`, printed:
   - `ok files, SVG hygiene and PNG sizes (173 checked)`
   - `ok WCAG contrast (11 checked)`, including Clay on Kiln at 15.40:1, and Terracotta on Kiln at 3.30:1 against a 3:1 target for both the dashes and the large-text kicker
   - `ok mark geometry (2 checked)`
   - `ALL CHECKS PASSED`

   The build printed a kicker size of 25.3 px for all three cards. The width guard did not trigger. Measured from the saved sources:
   - CASSANDRA: widest line 611 px.
   - Chorus: widest line 611 px.
   - Dervish: widest line 488 px (the kicker).

   The column is 650 px.
2. **Visual review:** all three cards were looked at, in both the first (all Bronze and night) and the final palettes.
3. **Links.** Each pull request reports its replacement count and an empty re-grep. Ephesus's 39 changed lines were each checked to differ from the original only in the URL: three also changed `ephesus` to `Ephesus` (GitHub paths are case-insensitive).
4. **README header,** on GitHub at the pushed commits, in a signed-out browser:
   - the image loads, with the dark variant in dark mode;
   - the mark's centre sits within 3 px of the text line's (390 against 387) in CASSANDRA, Dervish and CASSANDRA-Chorus.
5. **Repository settings:** read back through the GraphQL API after the edit. They match the approved text exactly.
6. **Remotes:** `git ls-remote origin` on the Chorus checkout reaches the organisation's repository.
7. **Chorus seed script:** `tests/test_seed_backlog.py` passes 9 of 9 on Python 3.13.14, and the backlog file parses with the new `repo`.
8. **Ephesus CI on #79:** all three checks pass ("Docs integrity", "Commit attribution", and "Typecheck · lint · test").

**Not tested:**
- The cards as link previews on social platforms. They take effect only after the owner uploads them.
- Hugging Face copies of the CASSANDRA model card still carry the old link until the next upload.

## Related Docs

- [`brand/README.md`](../../brand/README.md), sections "Social cards" and "Tagline"
- [`2026-10-14-cassandra-brand-identity.md`](2026-10-14-cassandra-brand-identity.md)
