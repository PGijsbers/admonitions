"""Converts GitHub/GitLab 'alerts' to MkDocs Material admonitions.

The supported syntaxes are documented in `admonitions.github` and
`admonitions.gitlab`.
"""

from __future__ import annotations

import re

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

from . import github, gitlab
from ._common import convert_alerts

# Re-exported for backward compatibility
from ._common import ADMONITION_TYPE_MAP, GH_CODEBLOCK_PATTERN  # noqa: F401
from .github import ALERT_BODY_PREFIX as ALERT_BASIC_BODY_PREFIX  # noqa: F401
from .gitlab import ALERT_MULTILINE_BODY_PREFIX, ALERT_MULTILINE_PATTERN  # noqa: F401

ALERT_BASIC_PATTERN = re.compile(
    r"^> {,3}\[!(?P<type>note|tip|important|caution|warning)] *(?P<title>.*)\r?\n(?P<body>(?:>.*(?:\r?\n|\Z))+)",
    flags=re.IGNORECASE | re.MULTILINE,
)
"""
Deprecated: kept for backward compatibility, the plugin uses
`github.ALERT_PATTERN` and `gitlab.ALERT_TITLE_PATTERN` instead.
"""


class AdmonitionConverter(BasePlugin):
    def on_page_markdown(
        self, markdown: str, /, *, page: Page, config: MkDocsConfig, files: Files
    ) -> str | None:
        """Converts all instances of GitHub/GitLab admonition to MM admonitions."""
        # convert basic syntax, with or without overridden title (GitLab only)
        markdown = convert_alerts(markdown, github.ALERT_RULE, gitlab.ALERT_TITLE_RULE)

        # convert multiline blockquote syntax (GitLab only)
        markdown = convert_alerts(markdown, gitlab.ALERT_MULTILINE_RULE)

        return markdown
