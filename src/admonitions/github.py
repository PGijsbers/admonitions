"""Converts GitHub 'alerts' to MkDocs Material admonitions.

## GitHub alerts syntax

See: https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#alerts

> [!caution]
> This is a caution admonition.

Supported GitHub alert types are:
- note
- tip
- important
- warning
- caution
"""

from __future__ import annotations

import re

from ._common import AlertRule, convert_alerts

ALERT_PATTERN = re.compile(
    r"^> {,3}\[!(?P<type>note|tip|important|caution|warning)][^\S\n]*\r?\n(?P<body>(?:>.*(?:\r?\n|\Z))+)",
    flags=re.IGNORECASE | re.MULTILINE,
)
"""
Alert syntax pattern with capturing groups:
- `type`: Alert type
- `body`: Alert body
"""

ALERT_BODY_PREFIX = re.compile("^> ?", re.MULTILINE)

ALERT_RULE: AlertRule = (ALERT_PATTERN, ALERT_BODY_PREFIX)


def convert(markdown: str) -> str:
    """Converts all GitHub alerts to MM admonitions."""
    return convert_alerts(markdown, ALERT_RULE)
