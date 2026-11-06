"""Converts GitHub/GitLab 'alerts' to MkDocs Material admonitions.

The supported syntaxes are documented in `admonitions.github` and
`admonitions.gitlab`.
"""

from __future__ import annotations

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

from . import github, gitlab

# Re-exported for backward compatibility
from ._common import ADMONITION_TYPE_MAP, GH_CODEBLOCK_PATTERN  # noqa: F401
from .github import ALERT_BASIC_BODY_PREFIX, ALERT_BASIC_PATTERN  # noqa: F401
from .gitlab import ALERT_MULTILINE_BODY_PREFIX, ALERT_MULTILINE_PATTERN  # noqa: F401


class AdmonitionConverter(BasePlugin):
    def on_page_markdown(
        self, markdown: str, /, *, page: Page, config: MkDocsConfig, files: Files
    ) -> str | None:
        """Converts all instances of GitHub/GitLab admonition to MM admonitions."""
        # convert basic syntax
        markdown = github.convert(markdown)

        # convert multiline blockquote syntax (GitLab only)
        markdown = gitlab.convert(markdown)

        return markdown
