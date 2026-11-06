"""Shared logic for converting alerts to MkDocs Material admonitions."""

from __future__ import annotations

import re

from admonitions.flavors._base import AdmonitionFlavor

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


def convert_alerts(markdown: str, *flavors: AdmonitionFlavor) -> str:
    """Converts alerts of any of the `flavors` to MkDocs Material admonitions.

    Each flavor's `pattern` captures the alert's `type` and `body`, and
    optionally its `title`. If the flavor is `quoted`, every body line starts
    with a `>` to remove.

    Alerts within code blocks are left untouched.

    The flavors are applied in a single left-to-right pass, as if their
    patterns were one pattern. At each step, the leftmost match of any flavor
    is converted and the search resumes after its end. So the body of an alert
    is left as it is, even when it contains a line that looks like the start of
    an alert, unless the alert's flavor `allows_nesting`. This matches GitHub
    and GitLab, which render an alert marker inside a quoted alert's body as
    plain text, so consecutive alerts in the same quote become a single alert.

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

    Applying the GitHub flavor first, then the titled one, would instead convert
    the inner `> [!note]` alert, leaving the outer one with no body to match:
    ```
    > [!tip] Overridden title
    !!! note "Note"
        This is the body.
    ```

    Swapping the order breaks the reverse case, a GitHub alert whose body
    contains a titled alert marker.

    If the alert's flavor `allows_nesting`, its body is converted first, with
    all the flavors, so alerts inside it become nested admonitions. GitLab
    renders alerts inside multiline (`>>>`) alerts this way.

    The order of the `flavors` doesn't matter. When two flavors match at the
    same position, the longest match wins.
    """
    codeblocks = list(CODEBLOCK_PATTERN.finditer(markdown))

    def in_codeblock(alert: re.Match) -> bool:
        return any(
            codeblock.start() < alert.start() and alert.end() < codeblock.end()
            for codeblock in codeblocks
        )

    def to_admonition(alert: re.Match, flavor: AdmonitionFlavor) -> str:
        """ Convert the found alert match into a MkDocs admonition. """
        alert_type: str = alert.group("type")
        alert_title: str = (alert.groupdict().get("title") or alert_type.title()).strip()
        alert_body: str = alert.group("body")

        # If the current admonition supports nesting, convert its body first.
        if flavor.allows_nesting:
            alert_body = convert_alerts(alert_body, *flavors)

        body_prefix = "^> ?" if flavor.quoted else "^"
        alert_body = re.sub(
            body_prefix, "    ", alert_body.strip(), flags=re.MULTILINE
        )

        # Normalize types that do not exist in MkDocs into supported ones.
        normalized_type = ADMONITION_TYPE_MAP.get(
            alert_type.lower(), alert_type.lower()
        )

        return f'!!! {normalized_type} "{alert_title}"\n{alert_body}\n'

    converted = []
    position = 0
    while True:
        candidates = [
            (flavor.pattern.search(markdown, position), flavor) for flavor in flavors
        ]
        candidates = [(match, flavor) for match, flavor in candidates if match]
        if not candidates:
            break

        # the leftmost alert wins, as it would with a single combined pattern,
        # then the longest one, so the order of the flavors doesn't matter
        alert, flavor = min(
            candidates,
            key=lambda candidate: (candidate[0].start(), -candidate[0].end()),
        )
        converted.append(markdown[position : alert.start()])
        
        if in_codeblock(alert):
            converted.append(alert.group())
        else:
            converted.append(to_admonition(alert, flavor))
        position = alert.end()

    converted.append(markdown[position:])
    return "".join(converted)
