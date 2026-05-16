# brew-aged-upgrade

> Upgrade Homebrew packages only after their formula has been published for N days.

Most supply chain compromises targeting package managers are detected within 24–72 hours of a malicious commit. By delaying upgrades until a formula has been "in the wild" for a few days, you let the community catch problems before they hit your machine — with zero ongoing maintenance on your part.

---

## Install

```sh
brew tap nhm7/aged-upgrade
brew install --HEAD brew-aged-upgrade
```

> **Note:** Once a tagged release exists, `--HEAD` will no longer be needed.

---

## Usage

```sh
# Upgrade packages whose formula is ≥ 3 days old (default)
brew-aged-upgrade

# Custom threshold — only upgrade if formula is ≥ 7 days old
BREW_AGE_MIN_DAYS=7 brew-aged-upgrade
```

**What it does, step by step:**

1. Runs `brew update` to refresh the local formula database.
2. Checks `brew outdated` for formulas and casks separately.
3. For each outdated package, queries the [GitHub API](https://docs.github.com/en/rest/commits) for the last commit on that formula's file in `homebrew-core` / `homebrew-cask`.
4. Upgrades only if the formula is at least `BREW_AGE_MIN_DAYS` days old.
5. Skips third-party tap packages (repo structure is unknown).

---

## Rate limits

The GitHub API allows **60 unauthenticated requests per hour** — one per outdated package. This is fine for most setups. If you regularly have 60+ outdated packages, set `HOMEBREW_GITHUB_API_TOKEN` to a [fine-grained personal access token](https://github.com/settings/tokens?type=beta) with **no extra permissions** (read-only public data is enough) to raise the limit to 5 000 req/hr.

```sh
export HOMEBREW_GITHUB_API_TOKEN=github_pat_...
```

---

## Replace `brew autoupdate`

If you currently use `brew autoupdate` with `--upgrade`, swap it out:

```sh
brew autoupdate delete
# then schedule brew-aged-upgrade as a daily launchd job or cron
```

A simple daily cron entry (`crontab -e`):

```cron
0 9 * * * /usr/local/bin/brew-aged-upgrade >> ~/Library/Logs/brew-aged-upgrade.log 2>&1
```

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `BREW_AGE_MIN_DAYS` | `3` | Minimum formula age in days before upgrading |
| `HOMEBREW_GITHUB_API_TOKEN` | _(unset)_ | Optional GitHub token to raise API rate limit |

---

## Why not just wait and upgrade manually?

You could — and that works. This tool is for people who want automatic upgrades but with a delay baked in, so they don't have to think about it.

---

## Security

Please report vulnerabilities via a [GitHub Security Advisory](https://github.com/nhm7/homebrew-aged-upgrade/security/advisories/new) rather than a public issue.

---

## Suggested repo rename

To work as a proper Homebrew tap (`brew tap nhm7/aged-upgrade`), rename this repo:

- **Name**: `homebrew-aged-upgrade`
- **Description**: `Homebrew tap: upgrade packages only after their formula has been published for N days — reducing supply chain attack surface`

---

## License

[MIT](LICENSE)
