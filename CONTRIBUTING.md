# Contributing to the Cassandra Collective

Thank you for your interest. This is the organisation's general guide. GitHub shows it in every repository of the organisation that has no `CONTRIBUTING.md` of its own.

**A project's own `CONTRIBUTING.md` has its specific rules and takes precedence over this guide.** Read it first when the project has one, for example [CASSANDRA-Chorus](https://github.com/Cassandra-Collective/CASSANDRA-Chorus/blob/main/CONTRIBUTING.md) or [Ephesus](https://github.com/Cassandra-Collective/Ephesus/blob/main/CONTRIBUTING.md).

## The organisation

We build language models, machines that predict, and we publish everything needed to check them: code, run logs, weights, and the results that did not work. ([Organisation profile](https://github.com/Cassandra-Collective))

| Repository | What it is |
|---|---|
| [CASSANDRA](https://github.com/Cassandra-Collective/CASSANDRA) | Low-hardware language-model research: can useful language-model behaviour be formed on consumer hardware, by structure, reuse and search rather than brute force? |
| [CASSANDRA-Chorus](https://github.com/Cassandra-Collective/CASSANDRA-Chorus) | Training a mixture-of-experts language model across a pool of volunteer machines, where no machine holds the whole model. Stage 0 closed with a negative result, reported in full. |
| [Dervish](https://github.com/Cassandra-Collective/Dervish) | A Muon-variant PyTorch optimizer whose hidden matrices have a provably bounded spectrum, with a pre-registered evaluation record. |
| [Ephesus](https://github.com/Cassandra-Collective/Ephesus) | An agent company you govern as its architect: a desktop harness that turns the terminal coding CLIs you already pay for into a self-coordinating crew. Pre-alpha, built in public. |
| [`.github`](https://github.com/Cassandra-Collective/.github) | The organisation's profile, its brand (the CASSANDRA identity) and these shared community files. |

## What we value

- **Claims are tested honestly.** A claim comes with its evidence: the command, its output, the test, the measurement. Say what was tested, on what, and what was not.
- **Negative results are reported.** A result that did not work is published with the same care as one that did.
- **Runs are reproducible.** Hypotheses and pass criteria are written down before the runs that judge them. Every run can be repeated from its configuration and seed, and its logs are kept.
- **Documentation changes with the code.** If a change makes a document wrong, the same pull request fixes the document.

Everyone taking part follows the [code of conduct](https://github.com/Cassandra-Collective/.github/blob/main/CODE_OF_CONDUCT.md).

## How to start

1. Read the project's README and, if it has one, its own `CONTRIBUTING.md`.
2. Find an issue. Every project keeps its backlog as GitHub issues. Good places to begin:
   - [`good first issue`](https://github.com/search?q=org%3ACassandra-Collective+label%3A%22good+first+issue%22+state%3Aopen&type=issues): small, well-described tasks for newcomers;
   - [`help wanted`](https://github.com/search?q=org%3ACassandra-Collective+label%3A%22help+wanted%22+state%3Aopen&type=issues): tasks where help is especially welcome.
3. Comment on the issue to say you would like to take it, and wait for a maintainer to confirm, so that two people do not do the same work.

Questions are welcome: see [getting help](https://github.com/Cassandra-Collective/.github/blob/main/SUPPORT.md).

## How a change gets in

1. **Issue first.** For anything beyond a typo or a broken link, open an issue (or use an existing one) before writing code, so the approach can be agreed before the work is done. Use the repository's issue forms.
2. **Branch.** Fork the repository, or branch from `main` if you have write access. Name the branch after the kind of change, for example `docs/fix-install-steps` or `fix/42-seed-handling`; a project's own guide may set a stricter pattern.
3. **Keep it focused.** One change per pull request.
4. **Open a pull request** that references the issue (`Closes #42`) and fill in the template.
5. **Show the evidence** in the pull request: the commands you ran and their output, test results, or before and after screenshots. Say what you did not test.
6. **Update the docs** that the change affects, in the same pull request.
7. **Review and merge.** A maintainer reviews the pull request. Merging is the maintainers' decision.

## Reporting security problems

Never report a vulnerability in a public issue. Follow the [security policy](https://github.com/Cassandra-Collective/.github/blob/main/SECURITY.md).

## Contributing to this repository (`.github`)

- **Brand changes are made in [`brand/tools/build_brand.py`](https://github.com/Cassandra-Collective/.github/blob/main/brand/tools/build_brand.py), never by editing the exported files.** Rebuild with `python brand/tools/build_brand.py` and check with `python brand/tools/check_brand.py`, which must print `ALL CHECKS PASSED`. The requirements and the full rules are in [`brand/README.md`](https://github.com/Cassandra-Collective/.github/blob/main/brand/README.md).
- **The community files here are defaults for the whole organisation.** A change to `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md` or the templates in `.github/` reaches every repository that has no file of its own, so open an issue first.
- **Every meaningful change has an implementation document,** `docs/implementations/YYYY-MM-DD-<slug>.md`, copied from [`docs/implementations/_TEMPLATE.md`](https://github.com/Cassandra-Collective/.github/blob/main/docs/implementations/_TEMPLATE.md).
- **Prose style:** plain English, and no em or en dashes; use a comma, a colon, a middle dot or a new sentence.
- **Licence:** you contribute under the Apache License 2.0 (`LICENSE`), including changes to the brand scripts and any brand files rebuilt from them. The repository publishes the brand files under CC BY-ND 4.0 (`brand/LICENSE-BRAND.md`). `NOTICE` lists the exceptions.
