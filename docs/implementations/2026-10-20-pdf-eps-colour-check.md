# 2026-10-20 - Check PDF and EPS colours in check_brand.py

| | |
|---|---|
| Repository | Cassandra-Collective/.github |
| Branch | `brand/pdf-eps-colour-check` |
| Status | Implemented and verified (see Verification) |

## Problem / Motivation

`check_brand.py` verified the colours of every SVG, but for the 16 PDFs and 16 EPS files it
only checked that each file exists and is not empty. Their colours had been verified once, by
hand (2026-10-14-cassandra-brand-identity.md, Verification step 4). A new VectorCraft version
or a build change could alter the PDF or EPS colours without anyone noticing. Tracked as
issue #9.

## What Changed

| File | Description |
|---|---|
| `brand/tools/build_brand.py` | New `EPS_CMYK` table: the expected CMYK values for every palette colour, keyed by hex. |
| `brand/tools/check_brand.py` | New `check_pdf()` and `check_eps()` plus helpers, run as a new "PDF and EPS colours" group. |
| `docs/implementations/2026-10-20-pdf-eps-colour-check.md` | This record. |

## Implementation Approach

`check_pdf(p, rel)` reads every stream in the PDF, decompresses the FlateDecode ones with
`zlib` (unfiltered streams are read as-is), and scans the content for painting operators: a
run of numbers followed by one of `rg RG g G k K sc SC scn SCN setrgbcolor setgray
setcmykcolor`, or a `/Name cs` colour space selection. Every `rg`/`RG` triple must match one
of the variant's palette colours; any other operator, a named colour space, or a colour
outside the variant fails the check. Expected RGB floats are derived from the hex values in
`build_brand.VARIANTS` and `build_brand.PROJECT_MARK_VARIANTS` as n/255.

`check_eps(p, rel)` verifies the DOS EPS magic `C5 D0 D3 C6`, reads the PostScript section at
the offset and length in the 30-byte binary header, strips `%` comments (which include the
ASCII85 thumbnail data), and scans the same way. Every `k` quartet must match the variant's
expected CMYK values in `build_brand.EPS_CMYK`; any other painting operator fails the check.

Where the non-`k` matches come from: the plain-text `rg`, `RG`, `setrgbcolor` and `setgray`
hits in an EPS file are (a) the prolog's alias definitions `/g {setgray} bd /rg {setrgbcolor}
bd /k {setcmykcolor} bd`, which define but do not invoke, and (b) coincidental bytes inside
the ASCII85 thumbnail, which sits in PostScript comment lines. Neither paints, so the check
counts as painting only a run of numbers immediately followed by the operator token.

`variant_of()` maps a file stem to its variant, longest name first so `red-figure-on-light`
is not shadowed by `on-light`.

Contracts: both functions take an absolute path and the repository-relative path for
messages, append to the module-level `failures` list via `fail()`, and return nothing. They
rely on the existing invariant that `main()` calls `report()` after the group, which exits
non-zero if any failure was recorded.

## Mathematical / Statistical Details

Two comparisons, both absolute-tolerance tuple matches with TOL = 1e-4:

- PDF: each painted `(r, g, b)` must satisfy `|c_i - e_i| <= 1e-4` for some expected colour
  `e`, where `e = hex / 255`. Observed worst deviation on the current files is under 4e-8
  (the exporter prints n/255 to 8 decimals), so the tolerance admits rounding only.
- EPS: each painted `(c, m, y, k)` must satisfy the same per-component test against
  `EPS_CMYK`, which the exporter prints to 4 decimals.

The expected CMYK values cannot be recomputed from hex in stdlib Python: they are
VectorCraft's "Generic CMYK (SWOP-like)" conversion (relative colorimetric, black-point
compensation), an ICC profile lookup, not a closed formula. They are therefore recorded
data. The four values that appear in the guide's colour table (Night 85 70 42 64, Bronze
27 39 82 34, Gold 15 29 65 6, Ivory 5 4 9 0 percent) agree with the table at the guide's
rounding. Black, White and the Red-figure colours have no guide entry; their values are
recorded from the current exports (a rich black `0.6666 0.6666 0.6665 1` and a paper-white
`0 0 0 0`), and whether black should be rich or pure K is a print-proof question, out of
scope for issue #9.

## Design Decisions

- One table, keyed by hex: `EPS_CMYK` lives next to the palette in `build_brand.py` so a
  palette change has one place to update, per the issue's acceptance criteria.
- Number-prefixed operator scanning instead of a full PostScript or PDF parser: the files
  are small, generator-produced and stable, and stdlib-only is required. Engineering
  default, offered for review.
- Tolerance 1e-4 rather than exact string equality, so a future exporter that prints more
  decimals of the same values does not trip the check.
- No permanent self-test files: the broken-copy verification is described below and in the
  pull request, keeping the repository free of intentionally wrong fixtures.

## Verification

Run from the repository root after `build_brand.py`:

1. `python brand/tools/check_brand.py` prints `ok   PDF and EPS colours (36 checked)` and
   ends `ALL CHECKS PASSED` (observed on the current tree, Linux, Python 3.10).
2. Broken PDF: copied `cassandra-mark-on-light.pdf`, decompressed its content stream,
   changed Bronze's green channel `0.40392157` to `0.50000000`, recompressed, called
   `check_pdf()` on it. Observed: `paints (0.5411765, 0.5, 0.16862746) outside its variant
   on-light`. The clean file passes.
3. Broken EPS: copied `cassandra-mark-on-light.eps`, changed one CMYK component `0.3927` to
   `0.5000` inside the PostScript section. Observed: `paints (0.2683, 0.5, 0.8154, 0.3379)
   outside its variant on-light`. Inserting `0.5 setgray` before a `k` operator also fails:
   `paints with setgray (0.5)`. The clean file passes.

**Not tested:** PDFs from generators other than VectorCraft (object streams, other filters);
a generator change that introduces those would fail closed (the stream is skipped only when
it declares an unknown filter, which is worth a follow-up if VectorCraft ever emits one).

## Related Docs

- Issue #9, whose acceptance criteria this implements.
- `2026-10-14-cassandra-brand-identity.md`, Verification step 4: the manual check this
  automates.
- `brand/README.md` colour table, which `EPS_CMYK` agrees with.
