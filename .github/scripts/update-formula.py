#!/usr/bin/env python3
"""Update Formula/brew-aged-upgrade.rb with a new stable release URL and SHA256.

Usage: update-formula.py <url> <sha256> <version>

Inserts url/sha256/version before the existing `head` line on first release,
or updates them in place on subsequent releases.
"""

import re
import sys

url, sha256, version = sys.argv[1], sys.argv[2], sys.argv[3]
path = "Formula/aged-upgrade.rb"

with open(path) as f:
    content = f.read()

stable_block = f'  url "{url}"\n  sha256 "{sha256}"\n  version "{version}"\n'

if re.search(r'^\s+url "https://', content, re.MULTILINE):
    # Subsequent release — replace the existing stable block
    content = re.sub(
        r'^\s+url "[^"]*"\n\s+sha256 "[^"]*"\n\s+version "[^"]*"\n',
        stable_block,
        content,
        flags=re.MULTILINE,
    )
else:
    # First release — insert stable block before the head line
    content = re.sub(r'(\s+head ")', f"\n{stable_block}\\1", content, count=1)

with open(path, "w") as f:
    f.write(content)

print(f"Formula updated to {version}")
print(f"  url:    {url}")
print(f"  sha256: {sha256}")
