"""Converts GitLab 'alerts' to MkDocs Material admonitions.

## GitLab alerts syntax

GitLab embraces GitHub syntax (see `admonitions.github`) with some minor
additions, which are converted by this module.

See: https://docs.gitlab.com/user/markdown/#alerts

### Override the alert block's title

> [!caution] Overridden title
> This is a caution admonition with overridden title.

### Multiline blockquotes

>>> [!tip]
GitLab alerts supports:
- basic GitHub alert syntax,
- overriding the alert block's title,
- and multiline blockquotes.
>>>
"""

from __future__ import annotations

import re

from ._common import AlertRule, convert_alerts
from .github import ALERT_BODY_PREFIX

ALERT_TITLE_PATTERN = re.compile(
    r"^> {,3}\[!(?P<type>note|tip|important|caution|warning)] *(?P<title>.*\S.*)\r?\n(?P<body>(?:>.*(?:\r?\n|\Z))+)",
    flags=re.IGNORECASE | re.MULTILINE,
)
"""
Overridden title alert syntax pattern with capturing groups:
- `type`: Alert type
- `title`: Overridden title
- `body`: Alert body
"""

ALERT_TITLE_RULE: AlertRule = (ALERT_TITLE_PATTERN, ALERT_BODY_PREFIX)

ALERT_MULTILINE_PATTERN = re.compile(
    r"^>>> {,3}\[!(?P<type>note|tip|important|caution|warning)] *(?P<title>.*)\r?\n(?P<body>(?:.*\r?\n)+)>>>",
    flags=re.IGNORECASE | re.MULTILINE,
)
"""Multiline blockquotes alert syntax pattern."""

ALERT_MULTILINE_BODY_PREFIX = re.compile("^", re.MULTILINE)

ALERT_MULTILINE_RULE: AlertRule = (ALERT_MULTILINE_PATTERN, ALERT_MULTILINE_BODY_PREFIX)


def convert(markdown: str) -> str:
    """Converts all GitLab-only alerts to MM admonitions."""
    markdown = convert_alerts(markdown, ALERT_TITLE_RULE)
    return convert_alerts(markdown, ALERT_MULTILINE_RULE)
