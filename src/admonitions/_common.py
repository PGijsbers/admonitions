"""Shared logic for converting alerts to MkDocs Material admonitions."""

from __future__ import annotations

import re
from typing import Tuple

GH_CODEBLOCK_PATTERN = re.compile(
    r"^```.*?^```",
    flags=re.MULTILINE | re.DOTALL,
)

# TODO: Make this configurable
ADMONITION_TYPE_MAP = {
    "caution": "danger",
    "important": "warning",
}

AlertRule = Tuple[re.Pattern, re.Pattern]
"""
An `(alert_pattern, body_prefix)` pair:
- `alert_pattern` has a `type` and a `body` capturing group, and optionally a
  `title` group.
- `body_prefix` matches the per-line prefix to replace with indentation.
"""


def convert_alerts(markdown: str, *rules: AlertRule) -> str:
    """Converts all alerts matching any of the `rules` to MM admonitions.

    The rules are applied in a single left-to-right pass, as if they were one
    pattern, so the body of an alert is never converted by another rule.
    Alerts within code blocks are left untouched.
    """
    codeblock_matches = list(GH_CODEBLOCK_PATTERN.finditer(markdown))

    def in_codeblock(admonition: re.Match) -> bool:
        return any(
            codeblock.start() < admonition.start()
            and admonition.end() < codeblock.end()
            for codeblock in codeblock_matches
        )

    def convert_admonition(match: re.Match, body_prefix: re.Pattern) -> str:
        if in_codeblock(match):
            # don't convert
            return match.group()
        alert_type: str = match.group("type")
        alert_title: str = (match.groupdict().get("title") or "").strip()
        alert_body: str = match.group("body")

        admonition_type = ADMONITION_TYPE_MAP.get(
            alert_type.lower(), alert_type.lower()
        )
        admonition_title = alert_title or alert_type.title()
        admonition_body = body_prefix.sub("    ", alert_body.strip())
        return f'!!! {admonition_type} "{admonition_title}"\n{admonition_body}\n'

    converted: list[str] = []
    position = 0
    while True:
        candidates = [
            (match, body_prefix)
            for alert_pattern, body_prefix in rules
            if (match := alert_pattern.search(markdown, position))
        ]
        if not candidates:
            break
        match, body_prefix = min(candidates, key=lambda candidate: candidate[0].start())
        converted.append(markdown[position : match.start()])
        converted.append(convert_admonition(match, body_prefix))
        position = match.end()
    converted.append(markdown[position:])
    return "".join(converted)
