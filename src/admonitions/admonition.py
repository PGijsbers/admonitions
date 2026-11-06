"""Converts GitHub/GitLab 'alerts' to MkDocs Material admonitions.

The supported syntaxes are documented in `admonitions.flavors.github` and
`admonitions.flavors.gitlab`.
"""

from __future__ import annotations

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

from admonitions._common import convert_alerts
from admonitions.flavors.github import GitHubAlert
from admonitions.flavors.gitlab import GitLabMultilineAlert, GitLabTitledAlert


class AdmonitionConverter(BasePlugin):
    def on_page_markdown(
        self, markdown: str, /, *, page: Page, config: MkDocsConfig, files: Files
    ) -> str | None:
        """Converts all GitHub/GitLab alerts to MkDocs Material admonitions."""
        # convert basic syntax, with or without a title (GitLab only), in one pass
        markdown = convert_alerts(markdown, GitHubAlert(), GitLabTitledAlert())

        # convert multiline blockquote syntax (GitLab only)
        return convert_alerts(markdown, GitLabMultilineAlert())
