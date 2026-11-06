"""GitHub 'alerts' syntax.

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

ALERT_PATTERN = re.compile(
    r"""
    ^>\ {,3}\[!(?P<type>note|tip|important|caution|warning)]  # > [!type]
    [^\S\n]*\r?\n                                             # and nothing else
    (?P<body>(?:>.*(?:\r?\n|\Z))+)                            # > body lines
    """,
    flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
)
"""
Example:
```
> [!NOTE]
> This is a note admonition.
```
"""
