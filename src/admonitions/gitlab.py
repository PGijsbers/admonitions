"""Converts GitLab 'alerts' to MkDocs Material admonitions.

## GitLab alerts syntax

GitLab embraces GitHub syntax with some minor additions.
The basic syntax, including the overridden title, is converted by
`admonitions.github`; this module converts the GitLab-only additions.

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

from ._common import convert_alerts

ALERT_MULTILINE_PATTERN = re.compile(
    r"^>>> {,3}\[!(?P<type>note|tip|important|caution|warning)] *(?P<title>.*)\r?\n(?P<body>(?:.*\r?\n)+)>>>",
    flags=re.IGNORECASE | re.MULTILINE,
)
"""Multiline blockquotes alert syntax pattern (GitLab only)."""

ALERT_MULTILINE_BODY_PREFIX = re.compile("^", re.MULTILINE)


def convert(markdown: str) -> str:
    """Converts all multiline blockquote alerts to MM admonitions."""
    return convert_alerts(
        markdown, ALERT_MULTILINE_PATTERN, ALERT_MULTILINE_BODY_PREFIX
    )
