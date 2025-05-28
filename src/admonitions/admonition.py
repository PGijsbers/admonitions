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
ALERT_PATTERN = re.compile(
    r"^> {,3}\[!(?P<type>note|tip|important|caution|warning)] *\r?\n(?P<body>(?:> +.*\r?\n)+)",
    flags=re.IGNORECASE | re.MULTILINE,
)

ALERT_BODY_PREFIX = re.compile("^> ", re.MULTILINE)

# TODO: Make this configurable
ADMONITION_TYPE_MAP = {
    "caution": "danger",
    "important": "warning",
}


class AdmonitionConverter(BasePlugin):
    def on_page_markdown(
        self, markdown: str, /, *, page: Page, config: MkDocsConfig, files: Files
    ) -> str | None:
        """Converts all instances of GitHub admonition to MM admonitions."""
        codeblock_matches = list(GH_CODEBLOCK_PATTERN.finditer(markdown))

        def in_codeblock(admonition: re.Match) -> bool:
            return any(
                codeblock.start() < admonition.start()
                and admonition.end() < codeblock.end()
                for codeblock in codeblock_matches
            )

        def convert_admonition(match: re.Match) -> str:
            if in_codeblock(match):
                # don't convert
                return match.group()
            alert_type: str = match.group("type")
            alert_body: str = match.group("body")

            admonition_type = ADMONITION_TYPE_MAP.get(
                alert_type.lower(), alert_type.lower()
            )
            admonition_title = alert_type.title()
            admonition_body = ALERT_BODY_PREFIX.sub("    ", alert_body.strip())
            return f'!!! {admonition_type} "{admonition_title}"\n{admonition_body}\n'

        markdown = ALERT_PATTERN.sub(convert_admonition, markdown)

        return markdown
