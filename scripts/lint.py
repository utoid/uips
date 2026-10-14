#!/usr/bin/env python3
"""Minimal repository consistency checks for UIP documents and vectors."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UIP_NAME = re.compile(r"uip-(\d{4})\.md$")
REQUIRED_HEADERS = (
    "UIP",
    "Layer",
    "Title",
    "Authors",
    "Status",
    "Type",
    "Assigned",
    "License",
    "Version",
)
REQUIRED_SECTIONS = ("Abstract", "Motivation", "Copyright")


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_preamble(text: str, path: Path) -> dict[str, str]:
    match = re.match(r"^```\n(.*?)\n```\n", text, re.DOTALL)
    if not match:
        fail(f"{path.name}: missing initial fenced RFC 822-style preamble")
    headers: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            fail(f"{path.name}: malformed preamble line: {line!r}")
        key, value = line.split(":", 1)
        headers[key.strip()] = value.strip()
    for header in REQUIRED_HEADERS:
        if not headers.get(header):
            fail(f"{path.name}: missing required header {header}")
    return headers


def check_uip(path: Path) -> None:
    number = int(UIP_NAME.fullmatch(path.name).group(1))
    text = path.read_text(encoding="utf-8")
    headers = parse_preamble(text, path)
    if headers["UIP"] != str(number):
        fail(f"{path.name}: UIP header must be {number}")
    for section in REQUIRED_SECTIONS:
        if f"# {section}\n" not in text:
            fail(f"{path.name}: missing section {section}")
    if "\t" in text:
        fail(f"{path.name}: tab characters are not permitted")


def main() -> None:
    uips = sorted(ROOT.glob("uip-[0-9][0-9][0-9][0-9].md"))
    if not uips:
        fail("no numbered UIP documents found")
    for path in uips:
        check_uip(path)
    for path in ROOT.glob("uip-[0-9][0-9][0-9][0-9]/**/*.json"):
        with path.open(encoding="utf-8") as handle:
            json.load(handle)
    print(f"checked {len(uips)} UIP documents")


if __name__ == "__main__":
    main()
