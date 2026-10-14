# Security policy

This policy covers every repository in the [Cassandra Collective](https://github.com/Cassandra-Collective) organisation that does not have a `SECURITY.md` of its own. A repository's own policy takes precedence: [Ephesus has one](https://github.com/Cassandra-Collective/Ephesus/blob/main/SECURITY.md).

## Reporting a vulnerability

**Do not open a public issue, pull request or comment for a security problem.**

Report it privately, in either of two ways.

1. **GitHub's private vulnerability reporting** (preferred). It is enabled on every repository in the organisation. Open the repository's **Security** tab and select **Report a vulnerability**, or go straight to the form:

   | Repository | Private report |
   |---|---|
   | CASSANDRA | [Report a vulnerability](https://github.com/Cassandra-Collective/CASSANDRA/security/advisories/new) |
   | CASSANDRA-Chorus | [Report a vulnerability](https://github.com/Cassandra-Collective/CASSANDRA-Chorus/security/advisories/new) |
   | Dervish | [Report a vulnerability](https://github.com/Cassandra-Collective/Dervish/security/advisories/new) |
   | Ephesus | [Report a vulnerability](https://github.com/Cassandra-Collective/Ephesus/security/advisories/new) |
   | `.github` (profile and brand files) | [Report a vulnerability](https://github.com/Cassandra-Collective/.github/security/advisories/new) |

   For any other repository, the form is at `https://github.com/Cassandra-Collective/<repository>/security/advisories/new`. You need a GitHub account to use it.

2. **Email** to **sensoymertefe@gmail.com**, with `SECURITY` in the subject line.

## What to include

- The repository, and the commit, branch or release you looked at.
- What the problem is and where it is: file, function, workflow or configuration.
- Steps to reproduce it, or a proof of concept.
- What you think the impact is: who could do what, and under which conditions.
- Whether anyone else knows about it, and whether you plan to publish it, and when.

Describe secrets and personal data rather than pasting them. If you found a live token or key, say where it is; do not use it.

## What to expect

The Cassandra Collective is a small organisation run by volunteers. There is no security team and no guaranteed response time. What we aim for:

- A person reads every report and replies. We aim to acknowledge a report within a few days; it can take longer.
- We tell you whether we could reproduce the problem, and keep you informed while it is fixed.
- When a fix is ready, we publish a GitHub security advisory where it is warranted, crediting you unless you would rather stay anonymous.

## Scope

In scope: the code, configuration, workflows and published files of the organisation's repositories. For example:

- a secret, token or key committed to a repository or its history;
- code that loads, imports or executes an untrusted file or network input in an unsafe way;
- a GitHub Actions workflow that an outside pull request or issue can abuse;
- a dependency vulnerability that our code actually makes reachable.

Out of scope:

- Vulnerabilities in third-party software or services themselves. Report those to their maintainers, and tell us if our use of them makes the problem worse.
- What a model trained by these projects writes (wrong, biased or unsafe text). That is a research finding or a bug: open an ordinary issue. It is a security problem only if it exposes private data or lets someone run code or reach systems they should not.
- Problems that need an attacker who already controls your machine or your account.

## Supported versions

The projects are research and pre-release software. Security fixes go to each repository's default branch (`main`) only, unless that repository's own policy says otherwise.

## Disclosure

Please give us a reasonable time to ship a fix before you publish anything. We coordinate disclosure through GitHub security advisories.
