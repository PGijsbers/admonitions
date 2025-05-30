"""Converts GitHub/GitLab 'alerts' to MkDocs Material admonitions.

## GitHub alerts syntax

See: https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#alerts

> [!caution]
> This is a caution admonition.

Supported GitHub alert types are:
- note
- tip
- important
- warning
- caution

## GitLab alerts syntax

GitLab embraces GitHub syntax with some minor additions.

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
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

GH_CODEBLOCK_PATTERN = re.compile(
    r"^```.*^```",
    flags=re.MULTILINE | re.DOTALL,
)
ALERT_BASIC_PATTERN = re.compile(
    r"^> {,3}\[!(?P<type>note|tip|important|caution|warning)] *(?P<title>.*)\r?\n(?P<body>(?:> +.*\r?\n)+)",
    flags=re.IGNORECASE | re.MULTILINE,
)
"""
Basic alert syntax pattern with capturing groups:
- `type`: Alert type (GitHub & GitLab)
- `title`: Overridden title (GitLab only)
- `body`: Alert body (GitHub & GitLab)
"""

ALERT_BASIC_BODY_PREFIX = re.compile("^> ", re.MULTILINE)

ALERT_MULTILINE_PATTERN = re.compile(
    r"^>>> {,3}\[!(?P<type>note|tip|important|caution|warning)] *(?P<title>.*)\r?\n(?P<body>(?:.*\r?\n)+)>>>",
    flags=re.IGNORECASE | re.MULTILINE,
)
"""Multiline blockquotes alert syntax pattern (GitLab only)."""

ALERT_MULTILINE_BODY_PREFIX = re.compile("^", re.MULTILINE)

# TODO: Make this configurable
ADMONITION_TYPE_MAP = {
    "caution": "danger",
    "important": "warning",
}


class AdmonitionConverter(BasePlugin):
    def on_page_markdown(
        self, markdown: str, /, *, page: Page, config: MkDocsConfig, files: Files
    ) -> str | None:
        """Converts all instances of GitHub/GitLab admonition to MM admonitions."""
        codeblock_matches: list[re.Match] = None

        def in_codeblock(admonition: re.Match) -> bool:
            return any(
                codeblock.start() < admonition.start()
                and admonition.end() < codeblock.end()
                for codeblock in codeblock_matches
            )

        body_prefix: re.Pattern = None

        def convert_admonition(match: re.Match) -> str:
            if in_codeblock(match):
                # don't convert
                return match.group()
            alert_type: str = match.group("type")
            alert_title: str = match.group("title").strip()
            alert_body: str = match.group("body")

            admonition_type = ADMONITION_TYPE_MAP.get(
                alert_type.lower(), alert_type.lower()
            )
            admonition_title = alert_title or alert_type.title()
            admonition_body = body_prefix.sub("    ", alert_body.strip())
            return f'!!! {admonition_type} "{admonition_title}"\n{admonition_body}\n'

        # convert basic syntax
        codeblock_matches = list(GH_CODEBLOCK_PATTERN.finditer(markdown))
        body_prefix = ALERT_BASIC_BODY_PREFIX
        markdown = ALERT_BASIC_PATTERN.sub(convert_admonition, markdown)

        # convert multiline blockquote syntax (GitLab only)
        codeblock_matches = list(GH_CODEBLOCK_PATTERN.finditer(markdown))
        body_prefix = ALERT_MULTILINE_BODY_PREFIX
        markdown = ALERT_MULTILINE_PATTERN.sub(convert_admonition, markdown)

        return markdown
