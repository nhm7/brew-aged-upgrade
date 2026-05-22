#!/usr/bin/env python3
"""State-based age tracking for brew-aged-upgrade.

Reads `brew outdated --json=v2` from stdin (--run mode) and maintains
a local JSON state file that records when each package version was first
seen as outdated. Upgrades only after MIN_DAYS have elapsed.

No GitHub API calls — no token, no rate limits, works for all taps.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import date, datetime, timedelta

LOG_RETENTION_DAYS = 183


def _load(path: str) -> dict:
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save(path: str, state: dict) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, path)


def _log_line_datetime(line: str) -> datetime | None:
    try:
        return datetime.fromisoformat(line[:19])
    except ValueError:
        pass

    marker = "==> brew-aged-upgrade run at "
    if marker not in line:
        return None
    raw = line.split(marker, 1)[1].split(" (min age:", 1)[0]
    parts = raw.split()
    if len(parts) == 6:
        parts.pop(4)
    try:
        return datetime.strptime(" ".join(parts), "%a %b %d %H:%M:%S %Y")
    except ValueError:
        return None


def _prune_log(path: str) -> None:
    cutoff = datetime.now() - timedelta(days=LOG_RETENTION_DAYS)
    try:
        with open(path) as f:
            lines = f.readlines()
    except FileNotFoundError:
        return
    except OSError:
        return

    kept = []
    keep_current_block = True
    for line in lines:
        timestamp = _log_line_datetime(line)
        if timestamp is not None:
            keep_current_block = timestamp >= cutoff
        if keep_current_block:
            kept.append(line)

    try:
        with open(path, "w") as f:
            f.writelines(kept)
    except OSError:
        return


def _write_log(path: str | None, message: str) -> None:
    if not path:
        return
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a") as f:
            f.write(f"{datetime.now().isoformat(timespec='seconds')} {message}\n")
    except OSError:
        return


def _log(message: str, log_file: str | None = None) -> None:
    print(f"{datetime.now().isoformat(timespec='seconds')} {message}")
    _write_log(log_file, message)


def _format_packages(packages: list[tuple[str, str]]) -> str:
    return ", ".join(f"{name} ({version})" for name, version in packages) or "none"


def _homebrew_icon_path() -> str | None:
    for path in (
        os.path.join(os.path.dirname(__file__), "Homebrew.png"),
        "/opt/homebrew/package/resources/Homebrew.png",
        "/usr/local/Homebrew/package/resources/Homebrew.png",
    ):
        if os.path.exists(path):
            return path
    return None


def _notify_upgrade_result(
    upgraded: list[tuple[str, str]],
    watching: list[tuple[str, str]],
) -> None:
    if not upgraded:
        return

    title = f"Homebrew Aged Upgrade {date.today():%d.%m}"
    summary = f"Upgraded: {_format_packages(upgraded)}\nWatching: {_format_packages(watching)}"
    icon = _homebrew_icon_path()
    if icon and shutil.which("terminal-notifier"):
        subprocess.run(
            [
                "terminal-notifier",
                "-title",
                title,
                "-message",
                summary,
                "-appIcon",
                icon,
                "-group",
                "com.nhm7.brew-aged-upgrade",
            ],
            check=False,
        )
        return

    script = (
        f"display notification {json.dumps(summary, ensure_ascii=False)} "
        f"with title {json.dumps(title, ensure_ascii=False)}"
    )
    subprocess.run(["osascript", "-e", script], check=False)


def run(state_file: str, min_days: int) -> None:
    sys.stdout.reconfigure(line_buffering=True)
    log_file = os.environ.get("BREW_AGE_LOG_FILE")
    if log_file:
        _prune_log(log_file)
    try:
        outdated = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        message = f"brew-aged-upgrade: could not parse brew outdated output: {e}"
        print(f"{datetime.now().isoformat(timespec='seconds')} {message}", file=sys.stderr)
        _write_log(log_file, message)
        sys.exit(1)
    state = _load(state_file)
    today = date.today()

    to_upgrade_formulae: list[tuple[str, str]] = []
    to_upgrade_casks: list[tuple[str, str]] = []
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
                _log(f"==> Watching {name} {new_ver} (0d old, need {min_days}d)", log_file)
            else:
                age = (today - date.fromisoformat(entry["first_seen"])).days
                if age >= min_days:
                    _log(f"==> Upgrading {name} {new_ver} ({age}d old)", log_file)
                    (to_upgrade_casks if is_cask else to_upgrade_formulae).append((name, new_ver))
                    del state[name]
                else:
                    _log(f"==> Skipping {name} ({age}d old, need {min_days}d)", log_file)

    # Remove packages that are no longer outdated (manually upgraded, etc.)
    for name in list(state.keys()):
        if name not in current_names:
            del state[name]

    _save(state_file, state)

    if not to_upgrade_formulae and not to_upgrade_casks:
        _log("==> Nothing to upgrade yet.", log_file)
        return

    for name, _version in to_upgrade_formulae:
        result = subprocess.run(["brew", "upgrade", "--formula", name], check=False)
        _log(f"==> brew upgrade --formula {name}: exit {result.returncode}", log_file)
    for name, _version in to_upgrade_casks:
        result = subprocess.run(["brew", "upgrade", "--cask", name], check=False)
        _log(f"==> brew upgrade --cask {name}: exit {result.returncode}", log_file)

    watching = [
        (name, info.get("available_version", "?"))
        for name, info in sorted(state.items())
        if name in current_names
    ]
    _notify_upgrade_result(to_upgrade_formulae + to_upgrade_casks, watching)


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
    elif sys.argv[1] == "--prune-log":
        _prune_log(sys.argv[2])
    elif sys.argv[1] == "--status":
        status(sys.argv[2])
