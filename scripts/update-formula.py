#!/usr/bin/env python3
"""Point Formula/brewup.rb at the latest brewup GitHub release.

Exits 0 without writing when the formula already matches that release.
"""

import hashlib
import json
import re
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

REPO = "xcrong/brewup"
FORMULA = Path("Formula/brewup.rb")
ASSETS = (
    "brewup-aarch64-apple-darwin.tar.gz",
    "brewup-x86_64-apple-darwin.tar.gz",
    "brewup-x86_64-unknown-linux-gnu.tar.gz",
)


def latest_tag() -> str:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/releases/latest",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "homebrew-brewup-update",
        },
    )
    with urllib.request.urlopen(req) as response:
        payload = json.load(response)
    tag = payload["tag_name"]
    names = {asset["name"] for asset in payload["assets"]}
    missing = [name for name in ASSETS if name not in names]
    if missing:
        sys.exit(f"latest release {tag} is missing assets: {', '.join(missing)}")
    return tag


def formula_tag(text: str) -> str:
    found = set(re.findall(r"releases/download/(v[^/]+)/", text))
    if len(found) != 1:
        sys.exit(f"formula should pin one release tag, found {sorted(found)}")
    return found.pop()


def sha256(url: str) -> str:
    with tempfile.NamedTemporaryFile() as tmp:
        subprocess.run(["curl", "-fsSL", "-o", tmp.name, url], check=True)
        digest = hashlib.sha256()
        with open(tmp.name, "rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()


def replace_asset(text: str, filename: str, tag: str, digest: str) -> str:
    pattern = (
        rf'(url "https://github.com/{REPO}/releases/download/)v[^/]+'
        rf'(/{re.escape(filename)}"\n\s*sha256 ")[0-9a-f]+(")'
    )
    def repl(match: re.Match[str]) -> str:
        return f"{match.group(1)}{tag}{match.group(2)}{digest}{match.group(3)}"

    updated, count = re.subn(pattern, repl, text, count=1)
    if count != 1:
        sys.exit(f"could not update {filename} in {FORMULA}")
    return updated


def main() -> None:
    if not FORMULA.is_file():
        sys.exit(f"missing {FORMULA}; run from the tap repository root")
    text = FORMULA.read_text()
    current = formula_tag(text)
    tag = latest_tag()
    if tag == current:
        print(f"formula already matches {tag}")
        return

    print(f"updating {current} -> {tag}")
    for filename in ASSETS:
        url = f"https://github.com/{REPO}/releases/download/{tag}/{filename}"
        text = replace_asset(text, filename, tag, sha256(url))
    if formula_tag(text) != tag:
        sys.exit("formula tag was not updated")
    FORMULA.write_text(text)
    print(f"updated formula to {tag}")


if __name__ == "__main__":
    main()
