"""Base class for the supported alert flavors."""

from __future__ import annotations

import re


class AdmonitionFlavor:
    """An alert syntax converted to MkDocs Material admonitions."""

    pattern: re.Pattern[str]
    """Matches an alert, capturing its `type`, `body` and optionally `title`."""

    quoted: bool
    """Whether every body line starts with a `>` to remove."""

    allows_nesting: bool
    """Whether the body may contain other alerts, converted as nested admonitions."""
