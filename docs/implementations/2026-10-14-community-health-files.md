# 2026-10-14 · Organisation-wide community health files

| | |
|---|---|
| Repository | `Cassandra-Collective/.github` |
| Branch | `docs/community-health` |
| Status | Verified on 2026-10-14 by static checks (Python 3.13.14 with PyYAML 6.0.3, git 2.53, gh 2.92, Windows 11); how GitHub renders the defaults can only be seen after merge |

Prose style: no em or en dashes.

## Problem / Motivation

The organisation had no code of conduct, security policy, support guide, contributing guide or templates outside Ephesus. Of the five repositories:

| Repository | Had of its own, before this change |
|---|---|
| CASSANDRA | none of the six file types |
| Dervish | none of the six file types |
| CASSANDRA-Chorus | `CONTRIBUTING.md`, issue forms, pull request template |
| Ephesus | `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, issue forms, pull request template |
| `.github` | none |

So a person who found a security problem in CASSANDRA, Dervish or CASSANDRA-Chorus had no published private route to report it, and could only open a public issue. Nobody outside Ephesus was told what conduct is expected or where to ask a question.

The owner asked, on 2026-10-14, for a contributing guide, a code of conduct and templates across the organisation, and decided that the shared files live as organisation defaults in this repository. CASSANDRA, Dervish and CASSANDRA-Chorus get their own repository-specific guides and templates in parallel pull requests. Ephesus keeps its own complete set and is not touched.

## What Changed

| File | Description |
|---|---|
| `CODE_OF_CONDUCT.md` | The Contributor Covenant 2.1 with the enforcement contact sensoymertefe@gmail.com: a byte-for-byte copy of Ephesus's file. |
| `SECURITY.md` | The organisation-wide security policy: report privately through GitHub's private vulnerability reporting or by email, what to include, what to expect, scope; a repository's own policy takes precedence. |
| `SUPPORT.md` | Where to ask questions (an issue labelled `question` in the repository concerned), what to include, and that there is no paid support. |
| `CONTRIBUTING.md` | The organisation's general guide: the projects, the shared values, how to start, the issue-first flow, and the rules specific to this repository. A project's own guide takes precedence. |
| `.github/ISSUE_TEMPLATE/bug-report.yml` | Default issue form for a bug report, labelled `bug`. |
| `.github/ISSUE_TEMPLATE/feature-or-improvement.yml` | Default issue form for a feature or improvement, labelled `enhancement`. |
| `.github/ISSUE_TEMPLATE/question.yml` | Default issue form for a question, labelled `question`. |
| `.github/ISSUE_TEMPLATE/config.yml` | Template chooser: blank issues allowed, contact links to the security policy and the code of conduct. |
| `.github/pull_request_template.md` | Default pull request template: what changes, the issue it closes, evidence, docs updated, checklist. |
| `README.md` | The table lists the new files, and a sentence explains that GitHub applies them as organisation defaults. |
| `docs/implementations/2026-10-14-community-health-files.md` | This document. |

## Implementation Approach

**How GitHub uses these files.** GitHub's documentation, "Creating a default community health file" (read on 2026-10-14), says:

- default community health files go in a **public** repository named `.github` owned by the organisation;
- GitHub uses a default file for every repository in the organisation that has no file of that type of its own, whatever that repository's visibility;
- issue templates and their `config.yml` must be stored in `.github/ISSUE_TEMPLATE`;
- every other supported file (code of conduct, contributing, security, support, pull request template) may be stored in the root, the `.github` folder or the `docs` folder; inside the `.github` repository the same order of precedence applies (`.github` folder, then root, then `docs`);
- if a repository has valid issue templates or an issue template `config.yml` of its own, **none** of the default issue templates are used there; the replacement is all or nothing for the folder, file by file for everything else;
- a label set by an issue template must exist in the repository where the template is used, or it is not applied.

**Placement.**

- The four Markdown policies are at the root. The root is valid, it is what a reader browsing this repository sees first, and the parallel pull requests in CASSANDRA, Dervish and CASSANDRA-Chorus link to this repository's `CODE_OF_CONDUCT.md` and `SECURITY.md`, which at the root are `https://github.com/Cassandra-Collective/.github/blob/main/CODE_OF_CONDUCT.md` and `.../SECURITY.md`.
- The issue forms and `config.yml` are in `.github/ISSUE_TEMPLATE/`, the only location GitHub accepts for them.
- The pull request template is `.github/pull_request_template.md`, so the repository root holds only documents a reader should open.

**Which defaults each repository will show.** File by file, until the parallel pull requests merge:

| Repository | Code of conduct | Contributing | Security | Support | Issue forms | Pull request template |
|---|---|---|---|---|---|---|
| CASSANDRA | default | default | default | default | default | default |
| Dervish | default | default | default | default | default | default |
| CASSANDRA-Chorus | default | its own | default | default | its own | its own |
| Ephesus | its own | its own | its own | **default** | its own | its own |
| `.github` | these files | these files | these files | these files | these files | these files |

Ephesus has no `SUPPORT.md`, so the default `SUPPORT.md` will appear on Ephesus too. Nothing in the Ephesus repository changes; only what GitHub displays there.

**Links.** Every link in the default files is an absolute URL. GitHub shows a default file in the context of another repository (the issue page's "contributing guidelines" link, the repository's overview tabs), and a relative link written for this repository could resolve against the wrong one.

**Code of conduct.** Ephesus's `CODE_OF_CONDUCT.md` is the Contributor Covenant 2.1 with the owner-approved contact address. It is copied unchanged: it is plain ASCII, has no em or en dashes, and never names Ephesus ("community leaders", "our community"), so it reads correctly for the whole organisation. Its attribution section is kept.

**Issue forms.** Each form is YAML with the three required keys, `name`, `description` and `body`. They use only the element types GitHub's form schema defines, and only the labels `bug`, `enhancement` and `question`, which exist in this repository and in all four project repositories. They set no `type`, `projects` or `assignees`: the organisation defines no issue types, and the forms serve any repository. They ask nothing project-specific (no "which project" field: the issue already lives in its repository).

## Mathematical / Statistical Details

None. This is a documentation and configuration change.

## Design Decisions

| Decision | Alternatives | Why | Who |
|---|---|---|---|
| Shared files as organisation defaults in this repository; CASSANDRA, Dervish and CASSANDRA-Chorus get their own guides and templates; Ephesus untouched | A full copy in every repository | One place to change the shared policy | Owner, 2026-10-14 |
| Enforcement and security contact sensoymertefe@gmail.com | A new role address | Already public in Ephesus | Owner, 2026-10-14 |
| Private vulnerability reporting as the first reporting route | Email only | Enabled on all five repositories on 2026-10-14; keeps the report, the fix and the advisory in one place | Owner, 2026-10-14 (enabling); engineering (preferring it over email) |
| Code of conduct copied byte for byte from Ephesus | Fetching the Covenant text afresh | Same text and contact across the organisation; the copy already met the dash rule | Engineering |
| Markdown policies at the root; pull request template in `.github/` | All in `.github/`; all at the root | The root matches the links in the parallel pull requests; GitHub accepts all three locations | Engineering |
| Absolute URLs in every default file | Relative links | Defaults are displayed in other repositories' contexts | Engineering |
| `blank_issues_enabled: true` | `false` | Friendlier for a small organisation, and a typo report needs no form; matches Ephesus | Engineering default, stated for review |
| Labels `bug`, `enhancement`, `question` only | Adding `needs-triage` or `documentation` forms | They exist in every repository today, so the forms work wherever they are shown | Engineering |
| Response times stated as aims ("a few days"), never as guarantees | A fixed service level | A small, volunteer-run organisation cannot promise one; the wording matches Ephesus | Engineering, following the owner's brief |
| `SUPPORT.md` also applies to Ephesus | Leaving Ephesus without one; adding one to Ephesus | Ephesus must not be touched; the default is generic enough to fit it | Engineering, stated for review |

## Verification

1. **State before the change,** read through the GitHub API on 2026-10-14:
   - which of the six file types each repository has (the table under Problem / Motivation);
   - private vulnerability reporting: `gh api repos/Cassandra-Collective/<repo>/private-vulnerability-reporting` returned `"enabled": true` for all five repositories;
   - labels: `bug`, `enhancement` and `question` exist in `.github`, CASSANDRA, CASSANDRA-Chorus, Dervish and Ephesus (`gh label list`);
   - Discussions are disabled on all five repositories, so `SUPPORT.md` does not mention them.
2. **Code of conduct is an exact copy.** `git rev-parse HEAD:CODE_OF_CONDUCT.md` gives `4860e75b35034fa7b88d3b78e3de8068c7289514`, the same blob SHA that `gh api repos/Cassandra-Collective/Ephesus/contents/CODE_OF_CONDUCT.md --jq .sha` reports for Ephesus's `main`. The file is plain ASCII, contains no em or en dash, and does not contain the word "Ephesus" (`grep -i`), so no adaptation was needed.
3. **Issue forms are valid.** A validator (kept outside the repository) loads each file with `yaml.safe_load` and checks it against GitHub's documented schema:
   - each form has non-empty `name` and `description` strings and a non-empty `body` list, and the names are unique across forms;
   - every element's `type` is one of `markdown`, `textarea`, `input`, `dropdown`, `checkboxes`, `upload`, and it uses only that type's documented attributes and validations;
   - every non-markdown element has a `label` and an `id` that matches `[A-Za-z0-9_-]+` and is unique in its form; markdown elements have a `value` and no `id`;
   - dropdown options are non-empty and distinct; every checkbox option has a `label`; every `required` is a boolean;
   - labels are a subset of {`bug`, `enhancement`, `question`}, and no form sets `type`, `projects` or `assignees`;
   - `config.yml` has a boolean `blank_issues_enabled` and every contact link has `name`, `url` (https) and `about`.

   Result: `OK: 4 files, every check passed` (bug report 7 fields, feature or improvement 6, question 3).

   The validator was checked against faults. On two of Ephesus's forms it reports their `needs-triage` label. On mutated copies of these files it caught all 7 injected faults: a missing `description`, an invalid element type, an `id` containing a space, a duplicate form name, a misspelt `label` key, a string `blank_issues_enabled` and a contact link without `about`.
4. **No em or en dashes.** A byte-level search (`LC_ALL=C grep` for U+2014 and U+2013) finds 0 in each of the 11 files in this change; the same search finds 9 in Ephesus's `SECURITY.md`, showing that it detects them. The only non-ASCII character in the change is the middle dot in this document's title.
5. **Line endings.** `git ls-files --eol` shows `i/lf w/lf` for all 11 files, and none starts with a byte order mark.
6. **Links.** All 43 distinct absolute URLs were fetched signed out with `curl`:
   - 24 answer 200 (two of them only on a retry; the first attempt returned 503), including both organisation-wide label searches (31 open `good first issue` results at the time).
   - 4 answer 404 today and **resolve only after this pull request merges**: `.github/blob/main/CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md` and `SUPPORT.md`. The forms, `config.yml`, the pull request template, `SUPPORT.md` and `CONTRIBUTING.md` link to them.
   - 10 redirect to GitHub's sign-in page, as expected: the five `security/advisories/new` forms and the five `issues/new/choose` pages need an account.
   - 4 redirect permanently, all in the copied Contributor Covenant text: three contributor-covenant.org pages (to the same path with a trailing slash) and `github.com/mozilla/diversity` (now `mozilla/inclusion`). They are left as Ephesus has them, to keep the copy exact.
   - 1 is not a link: the `<repository>` placeholder in `SECURITY.md`, inside a code span.

   Every relative link in `README.md` and in this document resolves to a file on the branch.

**Not tested:**
- How GitHub displays the defaults (the template chooser, the forms, the pull request template, the "contributing guidelines" link, and the repository tabs in CASSANDRA, Dervish, Chorus and Ephesus). GitHub reads defaults only from the default branch, so this can be observed only after merge.
- Submitting a form or a private vulnerability report.
- That GitHub itself accepts the forms: the validator encodes the documented schema, but GitHub's parser was not run. After merge, GitHub shows an error on the file's page if it rejects a form.

## Related Docs

- [`README.md`](../../README.md)
- [`brand/README.md`](../../brand/README.md), sections "Rebuilding" and "Notes"
- [`2026-10-14-project-cards-and-org-move.md`](2026-10-14-project-cards-and-org-move.md)
- GitHub Docs: [Creating a default community health file](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file), [Configuring issue templates for your repository](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository), [Syntax for issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms), [Syntax for GitHub's form schema](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema)
