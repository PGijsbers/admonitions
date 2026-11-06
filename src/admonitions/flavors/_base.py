"""Base class for the supported alert flavors."""

from __future__ import annotations

import re


class AdmonitionFlavor:
    """An alert syntax converted to MkDocs Material admonitions."""

    pattern: re.Pattern[str]
    """Matches an alert, capturing its `type`, `body` and optionally `title`."""

    body_prefix: re.Pattern[str] | None
    """Matches the prefix to remove from every body line, if any."""

    allows_nesting: bool
    """Whether the body may contain other alerts, converted as nested admonitions."""
