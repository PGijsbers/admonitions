"""Shared logic for converting alerts to MkDocs Material admonitions."""

from __future__ import annotations

import re

CODEBLOCK_PATTERN = re.compile(r"^```.*?^```", flags=re.MULTILINE | re.DOTALL)
"""
Example:
```
> [!tip]
> This alert is not converted.
```
"""

# TODO: Make this configurable
ADMONITION_TYPE_MAP = {
    "caution": "danger",
    "important": "warning",
}


def convert_alerts(markdown: str, *patterns: re.Pattern, quoted: bool = True) -> str:
    """Converts alerts matching any of the `patterns` to MkDocs Material admonitions.

    Each pattern captures the alert's `type` and `body`, and optionally its
    `title`. If `quoted`, every body line starts with a `>` to remove.

    The patterns are applied in a single left-to-right pass, as if they were one
    pattern, so the body of an alert is never converted by another pattern.
    Alerts within code blocks are left untouched.
    """
    codeblocks = list(CODEBLOCK_PATTERN.finditer(markdown))
    body_prefix = re.compile("^> ?" if quoted else "^", re.MULTILINE)

    def in_codeblock(alert: re.Match) -> bool:
        return any(
            codeblock.start() < alert.start() and alert.end() < codeblock.end()
            for codeblock in codeblocks
        )

    def to_admonition(alert: re.Match) -> str:
        alert_type: str = alert.group("type")
        alert_title: str = (alert.groupdict().get("title") or "").strip()
        alert_body: str = alert.group("body")

        admonition_type = ADMONITION_TYPE_MAP.get(
            alert_type.lower(), alert_type.lower()
        )
        admonition_title = alert_title or alert_type.title()
        admonition_body = body_prefix.sub("    ", alert_body.strip())
        return f'!!! {admonition_type} "{admonition_title}"\n{admonition_body}\n'

    converted = []
    position = 0
    while True:
        matches = [pattern.search(markdown, position) for pattern in patterns]
        matches = [match for match in matches if match]
        if not matches:
            break
        # the leftmost alert wins, as it would with a single combined pattern
        alert = min(matches, key=lambda match: match.start())
        converted.append(markdown[position : alert.start()])
        converted.append(alert.group() if in_codeblock(alert) else to_admonition(alert))
        position = alert.end()
    converted.append(markdown[position:])
    return "".join(converted)
