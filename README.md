# brew-aged-upgrade

A Homebrew tap that only upgrades packages whose formula has been published for at least N days — reducing exposure to supply chain attacks.

## Why?

Most supply chain compromises targeting package managers are detected within 24–72 hours. By delaying upgrades until a formula has been "in the wild" for a few days, you let the community catch problems before they reach your machine.

## Install

```sh
brew tap nhm7/aged-upgrade
brew install --HEAD brew-aged-upgrade
```

## Usage

```sh
# Upgrade packages whose formula is 3+ days old (default)
brew-aged-upgrade

# Use a custom threshold (e.g. 7 days)
BREW_AGE_MIN_DAYS=7 brew-aged-upgrade
```

## How it works

1. Runs `brew update` to refresh the formula database.
2. For each outdated formula and cask, queries the GitHub API to find when the formula file was last committed to `homebrew-core` / `homebrew-cask`.
3. Only runs `brew upgrade` if the formula is at least `BREW_AGE_MIN_DAYS` days old (default: 3).
4. Third-party tap packages are skipped (their repo structure is unknown).

**Rate limits**: The GitHub API allows 60 unauthenticated requests per hour. Each outdated package costs one request, so this works fine for typical setups. If you regularly have 60+ outdated packages, set `HOMEBREW_GITHUB_API_TOKEN` to a [fine-grained personal access token](https://github.com/settings/tokens) with no extra permissions to raise the limit to 5000/hr.

## Automate it

Wire it up as a daily launchd job (replace `brew autoupdate`):

```sh
brew autoupdate delete
# then add brew-aged-upgrade to a daily cron / launchd plist
```

## Repo name & description (suggested)

If renaming this repository, use:

- **Name**: `homebrew-aged-upgrade`
- **Description**: `Homebrew tap: upgrade packages only after their formula has been published for N days — reducing supply chain attack surface`

## License

MIT
