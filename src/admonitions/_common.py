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

    Alerts within code blocks are left untouched.

    The patterns are applied in a single left-to-right pass, as if they were
    one pattern. At each step, the leftmost match of any pattern is converted
    and the search resumes after its end. So the body of an alert is never
    converted by another pattern, even when it contains a line that looks like
    the start of an alert. This matches GitHub and GitLab, which support neither
    nested nor consecutive alerts, and render a later alert marker in an alert's
    body as plain text.

    Example, with a titled alert whose body contains a GitHub alert marker:
    ```
    > [!tip] Overridden title
    > [!note]
    > This is the body.
    ```

    In a single pass, the titled alert matches first and takes the whole block:
    ```
    !!! tip "Overridden title"
        [!note]
        This is the body.
    ```

    Applying the GitHub pattern first, then the titled one, would instead convert
    the inner `> [!note]` alert, leaving the outer one with no body to match:
    ```
    > [!tip] Overridden title
    !!! note "Note"
        This is the body.
    ```

    Swapping the order breaks the reverse case, a GitHub alert whose body
    contains a titled alert marker.
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
