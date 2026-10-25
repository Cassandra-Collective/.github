# 2026-10-20 · Check PDF and EPS colours in check_brand.py

| | |
|---|---|
| Repository | Cassandra-Collective/.github |
| Branch | `brand/pdf-eps-colour-check` |
| Status | Verified 2026-10-25 on Windows 11 Home 10.0.26300, Python 3.13.14, after the review revisions (see Verification) |

## Problem / Motivation

`check_brand.py` verified the colours of every SVG, but for the 18 PDFs and 18 EPS files (the
16 organisation files plus the two Red-figure marks) it only checked that each file exists and
is not empty. Their colours had been verified once, by hand (2026-10-14-cassandra-brand-identity.md,
Verification step 4). A new VectorCraft version or a build change could alter the PDF or EPS
colours without anyone noticing. Tracked as issue #9.

## What Changed

| File | Description |
|---|---|
| `brand/tools/build_brand.py` | New `EPS_CMYK` table: the expected CMYK values for every palette colour, keyed by hex. |
| `brand/tools/check_brand.py` | New `check_pdf()`, `check_eps()` and `pdf_streams()`, run as a new "PDF and EPS colours" group, which the module docstring now lists. |
| `docs/implementations/2026-10-20-pdf-eps-colour-check.md` | This record. |

## Implementation Approach

`check_pdf(p, rel)` reads the file and asks `pdf_streams()` for the decoded contents of every
stream. Each stream's dictionary is matched inside its own object (`N G obj << ... >> stream`,
and the match may not cross `endobj`), so the `/Filter` it reads is that stream's own. An
unfiltered stream is used as it is, a `/FlateDecode` one is decompressed with `zlib`, and any
other filter, or a stream that `zlib` rejects, is a failure rather than a skip. Streams whose
own dictionary says `/Type /Metadata` are XMP (XML) and are left out by that explicit test.

Each decoded stream is scanned for painting operators: a run of numeric operands, separated
by any whitespace and starting at a token boundary, followed by one of `rg RG g G k K sc SC
scn SCN setrgbcolor setgray setcmykcolor`; or a `/Name cs` colour space selection. Every
`rg`/`RG` triple must match one of the variant's palette colours; any other operator, a named
colour space, or a colour outside the variant fails the check. The file also fails if its
dictionaries or any decoded stream declare a `/ColorSpace`, `/Shading` or `/Pattern` resource
or an image XObject (`/Subtype /Image`), because those paint with colours the operator scan
does not see (`sh`, `Do`, pattern fills).

The variant's colours come from `allowed_colours(rel)`, the same lookup the SVG check uses,
and expected RGB floats are their hex values as n/255. A file that `allowed_colours()` cannot
place fails.

`check_eps(p, rel)` verifies the DOS EPS magic `C5 D0 D3 C6`, reads the PostScript section at
the offset and length in the 30-byte binary header, strips `%` comments, and scans the same
way. Every `k` quartet must match the `build_brand.EPS_CMYK` entry of one of the variant's
colours; any other painting operator fails, and so does a variant colour with no `EPS_CMYK`
entry.

Where the non-`k` matches come from. A plain-text search of an EPS PostScript section finds
`rg`, `RG`, `setrgbcolor` or `setgray` 3 to 5 times per file:

- (a) 3 per file are the prolog's alias definitions `/g {setgray} bd /rg {setrgbcolor} bd`,
  which define but do not invoke.
- (b) The rest are coincidental bytes inside the two ASCII85 blocks that VectorCraft writes
  as `%` comment lines: `%VectorCraft_BeginData: thumbnail` and
  `%VectorCraft_BeginData: native` (the embedded native document). Across the 18 files there
  are 4 such matches in the thumbnail block and 6 in the native block.

Neither kind paints. The check strips comments and counts as painting only operands
immediately followed by the operator token.

Contracts:

- `pdf_streams(data, rel)` takes the raw PDF bytes and the repository-relative path (for
  messages). It returns a list of the decoded stream contents, metadata excluded. Its side
  effect is one `fail()` for each stream it cannot decode. It relies on every stream object
  being written as `N G obj << dictionary >> stream ... endstream` with an uncompressed
  dictionary, which holds for every top-level stream object in any PDF, object streams
  included.
- `check_pdf(p, rel)` and `check_eps(p, rel)` take an absolute path and the
  repository-relative path. They append to the module-level `failures` list via `fail()` and
  return nothing. They rely on the existing invariant that `main()` calls `report()` after the
  group, which exits non-zero if any failure was recorded.

## Mathematical / Statistical Details

Two comparisons, both absolute-tolerance, per-component tuple matches:

- **PDF:** each painted `(r, g, b)` must satisfy `|c_i - e_i| <= 1e-4` (`PDF_TOL`) for some
  expected colour `e`, where `e = hex / 255`. Neighbouring sRGB values differ by
  `1/255 ≈ 0.0039`, so this tolerance admits only rounding of the same `n/255`. It also admits
  any exporter that prints 4 or more decimals. The worst deviation observed on the current
  files is under 4e-8, because the exporter prints float32 values.
- **EPS:** each painted `(c, m, y, k)` must satisfy `|c_i - e_i| <= 5e-5` (`EPS_TOL`) against
  `EPS_CMYK`. That is half a unit in the 4th decimal, the precision at which the table is
  recorded and the exporter prints, so a painted value passes only if it rounds to the
  recorded value. Any change in a printed digit is at least 1e-4 away and fails on every
  channel.
  - The first version used 1e-4 here. That is exactly one unit, so whether a one-unit drift
    passed depended on float representation: `0.3927` to `0.3928` passed (difference
    9.999999999998899e-05), while `0.2683` to `0.2684` failed (1.000000000000445e-04).

The expected CMYK values cannot be recomputed from hex in stdlib Python. They are
VectorCraft's "Generic CMYK (SWOP-like)" conversion (relative colorimetric, black-point
compensation), an ICC profile lookup, not a closed formula, so they are recorded data.

- **Guide values.** The four values in the guide's colour table (Night 85 70 42 64, Bronze
  27 39 82 34, Gold 15 29 65 6, Ivory 5 4 9 0 percent) agree with the table at the guide's
  rounding.
- **No guide entry.** Black, White and the Red-figure colours have none. Their values are
  recorded from the current exports: a rich black `0.6666 0.6666 0.6665 1` and a paper-white
  `0 0 0 0`.
- **Rich or pure black** is a print-proof question, out of scope for issue #9.

## Design Decisions

- **One table, keyed by hex.** `EPS_CMYK` lives next to the palette in `build_brand.py`, so a
  palette change has one place to update, per the issue's acceptance criteria.
- **Operator scanning, not a parser.** The check scans for numeric operands followed by an
  operator instead of fully parsing PostScript or PDF. The files are small,
  generator-produced and stable, and stdlib-only is required. Engineering default, offered
  for review.
- **Tolerances, not exact string equality.** A future exporter that prints more decimals of
  the same values does not trip the check. The tolerances are per format (see the
  mathematical details).
- **No permanent self-test files.** The broken-copy verification is described below, which
  keeps the repository free of intentionally wrong fixtures.

**Review revisions** (owner review of PR #19, 2026-10-25). The owner decided to fix these on
the branch before approval; the specifics below are engineering defaults.

- **Fail, not skip, on a stream the reader cannot decode.**
  - *Before:* the first version matched `<<(.*?)>>\s*stream` from the first `<<` it met. On
    every current PDF, the captured dictionary therefore ran across the preceding Pages and
    Page objects. It also skipped any stream that `zlib` rejected or that declared another
    filter.
  - *Risk:* with two content streams, an unreadable one could carry off-palette paint while
    the other kept the "paints no colours" guard quiet.
  - *Alternative rejected:* anchoring the match on `obj` alone. A lazy match still runs past
    `endobj` into the next object.
- **Skip XMP metadata only by its explicit `/Type /Metadata`.** It is XML and cannot paint,
  and its free text (titles, descriptions) could match the whitespace-tolerant operator
  pattern by coincidence.
- **One variant lookup.** `allowed_colours()` replaces the new `variant_of()` and
  `variant_hexes()`, so SVG, PDF and EPS cannot drift apart. A file it cannot place now fails
  instead of passing silently while being counted as checked.
- **Per-format tolerances,** as above.
- **Operator pattern hardened.** It accepts any whitespace between operands, so `0 0 0\nrg`
  is seen. A run starts only at a token boundary, and a bare `.` no longer counts as a number
  (it would have raised `ValueError` instead of a failure).
- **Named colour space pattern widened.** It accepts any PDF name characters, so
  `/CS-0 cs` is caught.
- **Resource check added.** `/ColorSpace`, `/Shading`, `/Pattern` and `/Subtype /Image`.
  This goes beyond the issue's acceptance criteria, but it is cheap and covers paint that the
  operator scan cannot see.

## Verification

Run from the repository root. The check reads the committed files; `build_brand.py` is needed
only to regenerate them.

1. **The check passes on the branch.** `python brand/tools/check_brand.py` prints
   `ok   PDF and EPS colours (36 checked)` and ends `ALL CHECKS PASSED`, exit 0. Observed:
   - 2026-10-20 for the first version, on Linux with Python 3.10;
   - 2026-10-25 for the revised version, on Windows 11 Home 10.0.26300 with Python 3.13.14.
2. **Broken copies fail.**
   - *Setup:* each case starts from `cassandra-mark-on-light.pdf` or
     `cassandra-mark-on-light.eps` and makes one change. PDF content edits are made to the
     decompressed content stream, which is then recompressed. EPS edits update the
     PostScript length in the DOS header. The copy is written to a temporary directory
     outside the repository and passed to `check_pdf()` or `check_eps()` of both the first
     version and the revised one.
   - *Result:* the clean files pass in both. The first version's messages for its own three
     cases match those it reported in the pull request.

   | Change | First version | Revised |
   |---|---|---|
   | PDF: Bronze green `0.40392157` to `0.5` | fails | fails: `paints (0.5411765, 0.5, 0.16862746) outside its variant` |
   | PDF: a second, unfiltered content stream paints `1 0 0 rg`, after an object whose dictionary names FlateDecode | **passes** | fails: `paints (1.0, 0.0, 0.0) outside its variant` |
   | PDF: an extra FlateDecode stream that does not decompress | **passes** | fails: `a FlateDecode stream does not decompress` |
   | PDF: an extra stream with `/Filter /LZWDecode` | **passes** | fails: `a stream with filter LZWDecode, which this check cannot read` |
   | PDF: `1 0\n0\nrg` appended to the content (operands on separate lines) | **passes** | fails: `paints (1.0, 0.0, 0.0) outside its variant` |
   | PDF: `/CS-0 cs` appended to the content | **passes** | fails: `selects a named colour space` |
   | PDF: an object declaring a `/Shading` resource | **passes** | fails: `declares ['/Shading']` |
   | PDF: an image XObject (`/Subtype /Image`) | **passes** | fails: `declares ['/Subtype /Image']` |
   | PDF: the clean file under a name no variant matches | **passes** | fails: `no variant colours known for this file` |
   | EPS: Bronze M `0.3927` to `0.5000` | fails | fails: `paints (0.2683, 0.5, 0.8154, 0.3379) outside its variant` |
   | EPS: Bronze M `0.3927` to `0.3928` (one unit) | **passes** | fails |
   | EPS: Bronze C `0.2683` to `0.2684` (one unit) | fails | fails |
   | EPS: `0.5 setgray` inserted before a `k` | fails | fails: `paints with setgray (0.5)` |
   | EPS: a `k` quartet split across two lines, Night C changed to `0.9` | fails, as a 2-operand `k` | fails: `paints (0.9, 0.701, 0.4192, 0.6388) outside its variant` |
   | EPS: Night removed from `EPS_CMYK` | raises `KeyError` | fails: `no EPS_CMYK entry for ['#121C2E']` |

3. **Prose.** A scan of the changed files found no em or en dashes.

**Not tested:**

- **Inline images and transparency.** Inline images (`BI ... ID ... EI`) and transparency
  (ExtGState alpha, soft masks) change what a viewer sees without a colour operator or one
  of the resources checked.
- **Other generators.** PDFs from generators other than VectorCraft.
- **CR-only line endings in EPS.** Comment stripping assumes LF line endings, which all 18
  current files use. A file with CR-only line endings would lose everything after its first
  comment and fail as "paints no colours", which is failing closed.

## Related Docs

- Issue #9, whose acceptance criteria this implements.
- `2026-10-14-cassandra-brand-identity.md`, Verification step 4: the manual check this
  automates.
- `brand/README.md` colour table, which `EPS_CMYK` agrees with.
