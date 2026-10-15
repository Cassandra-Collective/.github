# 2026-10-15 · Questions go to Discussions

| | |
|---|---|
| Repository | `Cassandra-Collective/.github` |
| Branch | `docs/discussions-qa` |
| Status | Verified on 2026-10-15 |

Prose style: no em or en dashes.

## Problem / Motivation

To draw in more contributors, the owner turned on GitHub Discussions in every repository of the organisation on 2026-10-15. The owner asked for the "Questions" links to point there.

Until then the only way to ask anything was a formal issue, through the Question form, because blank issues are off. A newcomer with a half-formed question had no lighter place to start.

## What Changed

| File | Description |
|---|---|
| `SUPPORT.md` | "Where to ask" sends questions to each repository's Discussions, Q&A category, and lists those five links. The Question form stays, for a question that should be tracked as an issue from the start. |
| `.github/ISSUE_TEMPLATE/config.yml` | A first contact link, "Ask a question", pointing at this repository's Q&A. It is the default chooser for any repository without templates of its own. |
| `CONTRIBUTING.md` | The questions line points at Discussions, Q&A, as well as the support page. |
| `docs/implementations/2026-10-15-discussions-qa.md` | This document. |

The repository setting itself (`has_discussions`) was changed through the API on the owner's decision. That change is outside the tree.

## Implementation Approach

GitHub creates six default categories when Discussions is turned on. Q&A is the one whose posts can have a marked answer (`isAnswerable` true), so a solved question stays findable. Every questions link uses the stable category URL, `https://github.com/Cassandra-Collective/<repo>/discussions/categories/q-a`.

The other four repositories get the same change in their own pull requests, made under their own rules.

## Mathematical / Statistical Details

None.

## Design Decisions

- **Keep the Question forms.** Removing them would leave no route for a question that should be tracked as an issue. Keeping them means one sentence in `SUPPORT.md`.
- **Q&A rather than General.** An answerable category lets a maintainer mark the answer, which is what makes old questions useful to the next person.

## Verification

- **Settings:** `gh api` reads `has_discussions` as `true` on all five repositories. GraphQL lists the categories Announcements, General, Ideas, Polls, Q&A (answerable) and Show and tell in each.
- **Links:** all five Q&A URLs return HTTP 200 signed out.
- **Config:** `config.yml` parses with `blank_issues_enabled: false` and three contact links, each with `name`, `url` and `about`.
- **Style:** no em or en dashes in the changed files.

## Related Docs

- `SUPPORT.md`, `CONTRIBUTING.md`
- `2026-10-14-community-health-files.md`
