# brew-aged-upgrade — Developer Guide

## What this project does

A Homebrew tap that delays package upgrades until a formula version has been
outdated on the user's machine for at least N days. This gives the community
time to catch supply chain attacks before they reach end users.

Users install via:
```sh
brew tap nhm7/aged-upgrade
brew install brew-aged-upgrade   # stable, after first release
brew install --HEAD brew-aged-upgrade  # latest main
```

---

## Repository structure

```
libexec/
  brew-aged-upgrade           Bash CLI — start / stop / status / run / help
  brew-aged-upgrade-core.py   Python — state file management and upgrade logic
Formula/
  brew-aged-upgrade.rb        Homebrew formula (url/sha256 auto-updated on release)
.github/
  scripts/
    update-formula.py         Updates formula url/sha256/version after a release
  workflows/
    ci.yml                    ShellCheck (bash) + Ruff (Python) + Ruby syntax
    codeql.yml                CodeQL static analysis — Ruby and Python
    release.yml               Release Please + formula update on release
    pr-title.yml              Enforces conventional commit format on PR titles
VERSION                       Current version, managed by Release Please
.release-please-config.json   Release Please config (simple release type)
.release-please-manifest.json Release Please version manifest
pyproject.toml                Ruff config for the Python file
```

---

## How the tool works

1. `brew-aged-upgrade run` calls `brew update` then `brew outdated --json=v2`.
2. For each outdated package, `brew-aged-upgrade-core.py` checks
   `~/.config/brew-aged-upgrade/pending.json`.
3. If the package+version is new, it is recorded with today's date and skipped.
4. If the package+version has been in the state file for ≥ `BREW_AGE_MIN_DAYS`
   days (default 3), it is upgraded and removed from the state file.
5. If a new version appears while watching, the clock resets for that package.
6. Packages no longer listed in `brew outdated` are evicted from the state file.

No GitHub API calls. No token. Works for all taps including third-party ones.

The `start` command installs a launchd agent that runs `brew-aged-upgrade run`
daily. Logs go to `~/Library/Logs/brew-aged-upgrade.log`.

---

## Development workflow

### Branching

Use short-lived branches off `main`. No enforced naming convention — the PR
title carries the semantic meaning.

### Commit and PR title format (required)

PR titles must follow [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | When to use | Version bump |
|---|---|---|
| `feat:` | New user-facing feature | minor (1.0.0 → 1.1.0) |
| `fix:` | Bug fix | patch (1.0.0 → 1.0.1) |
| `feat!:` | Breaking change | major (1.0.0 → 2.0.0) |
| `chore:` | Maintenance, deps, CI | none |
| `docs:` | Documentation only | none |
| `refactor:` | Code change without behaviour change | none |
| `perf:` | Performance improvement | none |
| `test:` | Test changes | none |
| `ci:` | CI/CD changes | none |

The `pr-title.yml` workflow validates the PR title on every push. CI must pass
before merging.

### CI checks (all must pass)

| Check | What it covers |
|---|---|
| ShellCheck | `libexec/brew-aged-upgrade` (bash) |
| Ruff lint + format | `libexec/brew-aged-upgrade-core.py` (Python) |
| Ruby syntax | `Formula/brew-aged-upgrade.rb` |
| CodeQL (Python) | Static security analysis of the Python file |
| CodeQL (Ruby) | Static security analysis of the formula |
| PR title | Conventional commit format |

### Testing locally

```sh
# Lint the shell script
shellcheck libexec/brew-aged-upgrade

# Lint and format-check the Python file
ruff check libexec/
ruff format --check libexec/

# Check the Ruby formula syntax
ruby -c Formula/brew-aged-upgrade.rb

# Test the CLI without actually upgrading anything
BREW_AGE_MIN_DAYS=9999 brew-aged-upgrade run   # watches everything, upgrades nothing

# Inspect the state file
cat ~/.config/brew-aged-upgrade/pending.json

# Manually backdate an entry to test upgrade path
# Edit the "first_seen" date to something old, then run:
brew-aged-upgrade run
```

---

## Release process

This project uses [Release Please](https://github.com/googleapis/release-please).
**Do not create tags or releases manually.**

### How it works

1. Merge a PR with a `feat:` or `fix:` title to `main`.
2. Release Please opens (or updates) a "release PR" titled
   `chore(main): release X.Y.Z`. This PR contains the bumped `VERSION` file
   and an updated `CHANGELOG.md`.
3. Review the release PR and merge it when ready to ship.
4. Release Please creates the git tag and GitHub Release automatically.
5. The `update-formula` job then computes the archive SHA256, updates
   `Formula/brew-aged-upgrade.rb`, and commits it back to `main`.

### Version bumping rules

- `fix:` → patch (1.0.0 → 1.0.1)
- `feat:` → minor (1.0.0 → 1.1.0)
- `feat!:` / body contains `BREAKING CHANGE:` → major (1.0.0 → 2.0.0)
- `chore:`, `docs:`, `ci:`, `refactor:` → no bump, not included in changelog

### After a release

The formula on `main` is automatically updated with the new `url`, `sha256`,
and `version`. Users on stable installs (`brew upgrade brew-aged-upgrade`) will
get the new version. Users on `--HEAD` always track `main`.

---

## Key design decisions

**State file instead of GitHub API**
Early versions checked the GitHub API for the age of each formula file. This
required a token for users with many outdated packages and didn't work for
third-party taps. The state file approach records when the user's machine first
saw a version as outdated — which is arguably the more meaningful signal anyway,
since it measures how long the version has been "in the wild" on the user's end.

**launchd over cron**
macOS launchd is the native scheduler. It handles sleep/wake cycles correctly,
retries missed runs, and integrates with system logs. cron is available but is
not recommended on macOS for persistent background tasks.

**Two-file design (bash + Python)**
The bash file handles the CLI and launchd integration. The Python file handles
all JSON parsing, date arithmetic, and subprocess management. This keeps the
bash script ShellCheck-clean and avoids embedding fragile Python heredocs inside
shell.

**No token required**
The tool is deliberately designed to work with zero configuration beyond
`brew-aged-upgrade start`. Adding a GitHub token requirement would be a
significant UX regression.

---

## Security

Report vulnerabilities via a
[GitHub Security Advisory](https://github.com/nhm7/homebrew-aged-upgrade/security/advisories/new).
Do not open a public issue for security problems.
