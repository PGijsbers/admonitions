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

GitLab supports this syntax too, extended with an optional overridden title
(see `admonitions.gitlab`), which is also handled here.
"""

from __future__ import annotations

import re

from ._common import convert_alerts

ALERT_BASIC_PATTERN = re.compile(
    r"^> {,3}\[!(?P<type>note|tip|important|caution|warning)] *(?P<title>.*)\r?\n(?P<body>(?:>.*(?:\r?\n|\Z))+)",
    flags=re.IGNORECASE | re.MULTILINE,
)
"""
Basic alert syntax pattern with capturing groups:
- `type`: Alert type (GitHub & GitLab)
- `title`: Overridden title (GitLab only)
- `body`: Alert body (GitHub & GitLab)
"""

ALERT_BASIC_BODY_PREFIX = re.compile("^> ?", re.MULTILINE)


def convert(markdown: str) -> str:
    """Converts all basic syntax alerts to MM admonitions."""
    return convert_alerts(markdown, ALERT_BASIC_PATTERN, ALERT_BASIC_BODY_PREFIX)
