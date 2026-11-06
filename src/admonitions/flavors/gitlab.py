"""GitLab 'alerts' syntax.

GitLab embraces GitHub syntax (see `admonitions.flavors.github`) with some
minor additions.

See: https://docs.gitlab.com/user/markdown/#alerts

## Override the alert block's title

> [!caution] Overridden title
> This is a caution admonition with overridden title.

## Multiline blockquotes

>>> [!tip]
GitLab alerts supports:
- basic GitHub alert syntax,
- overriding the alert block's title,
- and multiline blockquotes.
>>>
"""

from __future__ import annotations

import re

TITLED_ALERT_PATTERN = re.compile(
    r"""
    ^>\ {,3}\[!(?P<type>note|tip|important|caution|warning)]  # > [!type]
    \ *(?P<title>.*\S.*)\r?\n                                 # followed by a title
    (?P<body>(?:>.*(?:\r?\n|\Z))+)                            # > body lines
    """,
    flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
)
"""
Example:
```
> [!caution] Overridden title
> This is a caution admonition with overridden title.
```
"""

MULTILINE_ALERT_PATTERN = re.compile(
    r"""
    ^>>>\ {,3}\[!(?P<type>note|tip|important|caution|warning)]  # >>> [!type]
    \ *(?P<title>.*)\r?\n                                       # optional title
    (?P<body>(?:.*\r?\n)+)                                      # body lines
    >>>                                                         # closing >>>
    """,
    flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
)
"""
Example:
```
>>> [!tip]
This is a tip admonition.
>>>
```
"""
