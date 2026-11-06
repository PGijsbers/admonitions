"""Converts GitHub/GitLab 'alerts' to MkDocs Material admonitions.

The supported syntaxes are documented in `admonitions.flavours.github` and
`admonitions.flavours.gitlab`.
"""

from __future__ import annotations

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

from admonitions._common import convert_alerts
from admonitions.flavours import github, gitlab


class AdmonitionConverter(BasePlugin):
    def on_page_markdown(
        self, markdown: str, /, *, page: Page, config: MkDocsConfig, files: Files
    ) -> str | None:
        """Converts all instances of GitHub/GitLab admonition to MM admonitions."""
        # convert basic syntax, with or without a title (GitLab only), in one pass
        markdown = convert_alerts(
            markdown, github.ALERT_PATTERN, gitlab.TITLED_ALERT_PATTERN
        )

        # convert multiline blockquote syntax (GitLab only)
        return convert_alerts(markdown, gitlab.MULTILINE_ALERT_PATTERN, quoted=False)
