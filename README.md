# 🍺 brew-aged-upgrade

**Automatically upgrade Homebrew packages — but only after they've been available for a few days.**

Most supply chain attacks on package managers are caught within 24–72 hours of a malicious commit. By giving each update a short waiting period before it lands on your machine, you let the community spot problems first — with zero extra effort on your part.

No GitHub token required. No API calls. Works with all taps.

---

## Install

```sh
brew tap nhm7/brew-aged-upgrade https://github.com/nhm7/brew-aged-upgrade
brew install nhm7/brew-aged-upgrade/brew-aged-upgrade
```

> **Bleeding edge:** replace `brew install` with `brew install --HEAD` to always track the latest `main`.

---

## Quick Start

```sh
# Enable daily auto-upgrade with the default 3-day delay
brew-aged-upgrade start

# Or choose your own delay
brew-aged-upgrade start --days 7
```

That's it. It runs daily in the background via a launchd job and logs to `~/Library/Logs/brew-aged-upgrade.log`.

---

## All Commands

| Command | Description |
|---|---|
| `brew-aged-upgrade start [--days N]` | Enable daily auto-upgrade (default: 3-day delay) |
| `brew-aged-upgrade stop` | Disable auto-upgrade and remove the background job |
| `brew-aged-upgrade status` | Show status and which packages are currently being watched |
| `brew-aged-upgrade run` | Run once immediately |
| `brew-aged-upgrade help` | Show help |

---

## How It Works

1. Runs `brew update` to refresh the formula database.
2. For each outdated package, records the date it was first seen as outdated in a local state file (`~/.config/brew-aged-upgrade/pending.json`).
3. On each subsequent run, skips packages that haven't waited long enough.
4. Once a package has been outdated for at least `N` days, it gets upgraded.
5. If a new version comes out while watching, the clock resets for that package.

No network calls beyond what Homebrew itself makes — your machine, your data.

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `BREW_AGE_MIN_DAYS` | `3` | Override the delay in days for a one-off `run` |

The delay is stored in the launchd job when you run `start`, so changing `BREW_AGE_MIN_DAYS` only affects manual `run` invocations. To change the scheduled delay, run `stop` and `start` again with the new value.

---

## Replacing `brew autoupdate`

If you already use `brew autoupdate --upgrade`, swap it out:

```sh
brew autoupdate delete
brew-aged-upgrade start --days 3
```

---

## ✅ Status Example

```
==> brew-aged-upgrade is installed and running
    Min age : 3 day(s)
    Plist   : ~/Library/LaunchAgents/com.nhm7.brew-aged-upgrade.plist
    Log     : ~/Library/Logs/brew-aged-upgrade.log

Pending packages (watching, not yet upgraded):
  curl (formula) — seen 1d ago, version 8.8.0
  iterm2 (cask)  — seen 2d ago, version 3.5.0
```

---

## Security

Please report vulnerabilities via a [GitHub Security Advisory](https://github.com/nhm7/brew-aged-upgrade/security/advisories/new) rather than a public issue.

---

## License

[MIT](LICENSE)
