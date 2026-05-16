#!/usr/bin/env python3
"""State-based age tracking for brew-aged-upgrade.

Reads `brew outdated --json=v2` from stdin (--run mode) and maintains
a local JSON state file that records when each package version was first
seen as outdated. Upgrades only after MIN_DAYS have elapsed.

No GitHub API calls — no token, no rate limits, works for all taps.
"""

import json
import os
import subprocess
import sys
from datetime import date


def _load(path: str) -> dict:
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save(path: str, state: dict) -> None:
    with open(path, "w") as f:
        json.dump(state, f, indent=2)


def run(state_file: str, min_days: int) -> None:
    outdated = json.load(sys.stdin)
    state = _load(state_file)
    today = date.today()

    to_upgrade_formulae: list[str] = []
    to_upgrade_casks: list[str] = []
    current_names: set[str] = set()

    for kind, is_cask in [("formulae", False), ("casks", True)]:
        for pkg in outdated.get(kind, []):
            name: str = pkg["name"]
            new_ver: str = pkg.get("current_version") or "unknown"
            current_names.add(name)
            entry = state.get(name, {})

            if entry.get("available_version") != new_ver:
                # New package or new available version — start the clock
                state[name] = {
                    "first_seen": today.isoformat(),
                    "available_version": new_ver,
                    "is_cask": is_cask,
                }
                print(f"==> Watching {name} {new_ver} (0d old, need {min_days}d)")
            else:
                age = (today - date.fromisoformat(entry["first_seen"])).days
                if age >= min_days:
                    print(f"==> Upgrading {name} {new_ver} ({age}d old)")
                    (to_upgrade_casks if is_cask else to_upgrade_formulae).append(name)
                    del state[name]
                else:
                    print(f"==> Skipping {name} ({age}d old, need {min_days}d)")

    # Remove packages that are no longer outdated (manually upgraded, etc.)
    for name in list(state.keys()):
        if name not in current_names:
            del state[name]

    _save(state_file, state)

    for name in to_upgrade_formulae:
        subprocess.run(["brew", "upgrade", name], check=False)
    for name in to_upgrade_casks:
        subprocess.run(["brew", "upgrade", "--cask", name], check=False)


def status(state_file: str) -> None:
    state = _load(state_file)
    if not state:
        print("  (none)")
        return
    today = date.today()
    for name, info in sorted(state.items()):
        age = (today - date.fromisoformat(info["first_seen"])).days
        kind = "cask" if info.get("is_cask") else "formula"
        ver = info.get("available_version", "?")
        print(f"  {name} ({kind}) — seen {age}d ago, version {ver}")


if __name__ == "__main__":
    if sys.argv[1] == "--run":
        run(
            state_file=os.environ["BREW_AGE_STATE_FILE"],
            min_days=int(os.environ.get("BREW_AGE_MIN_DAYS", "3")),
        )
    elif sys.argv[1] == "--status":
        status(sys.argv[2])
