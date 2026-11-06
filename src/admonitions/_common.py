"""Shared logic for converting alerts to MkDocs Material admonitions."""

from __future__ import annotations

import re

GH_CODEBLOCK_PATTERN = re.compile(
    r"^```.*?^```",
    flags=re.MULTILINE | re.DOTALL,
)

# TODO: Make this configurable
ADMONITION_TYPE_MAP = {
    "caution": "danger",
    "important": "warning",
}


def convert_alerts(
    markdown: str, alert_pattern: re.Pattern, body_prefix: re.Pattern
) -> str:
    """Converts all alerts matching `alert_pattern` to MM admonitions.

    `alert_pattern` must have `type`, `title` and `body` capturing groups.
    `body_prefix` matches the per-line prefix to replace with indentation.
    Alerts within code blocks are left untouched.
    """
    codeblock_matches = list(GH_CODEBLOCK_PATTERN.finditer(markdown))

    def in_codeblock(admonition: re.Match) -> bool:
        return any(
            codeblock.start() < admonition.start()
            and admonition.end() < codeblock.end()
            for codeblock in codeblock_matches
        )

    def convert_admonition(match: re.Match) -> str:
        if in_codeblock(match):
            # don't convert
            return match.group()
        alert_type: str = match.group("type")
        alert_title: str = match.group("title").strip()
        alert_body: str = match.group("body")

        admonition_type = ADMONITION_TYPE_MAP.get(
            alert_type.lower(), alert_type.lower()
        )
        admonition_title = alert_title or alert_type.title()
        admonition_body = body_prefix.sub("    ", alert_body.strip())
        return f'!!! {admonition_type} "{admonition_title}"\n{admonition_body}\n'

    return alert_pattern.sub(convert_admonition, markdown)
