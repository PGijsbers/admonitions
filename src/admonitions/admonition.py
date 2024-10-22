from __future__ import annotations

import re
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

GH_ADMONITION_HEADER_PATTERN = r"> {,3}\[!(\w+)]\s*"
GH_ADMONITION_PATTERN = re.compile(r"> {,3}\[!\w+]\s*\n(>.*\n)+", flags=re.IGNORECASE)
GH_CODEBLOCK_PATTERN = re.compile(r"```.*?```", flags=re.DOTALL)

# TODO: Make this configurable
ADMONITION_TYPE_MAP = {
    "caution": "danger",
    "important": "warning",
}


def convert_admonition_header(gh_header: str) -> str:
    admonition_type_match = re.search(GH_ADMONITION_HEADER_PATTERN, gh_header, flags=re.IGNORECASE)
    (admonition_type,) = admonition_type_match.groups()
    mm_admonition_type = ADMONITION_TYPE_MAP.get(admonition_type.lower(), admonition_type)
    return f'!!! {mm_admonition_type} "{admonition_type.title()}"\n'


def convert_admonition_body(gh_body: str) -> str:
    starts_with_angle = r">(.*?\n)"
    return re.sub(starts_with_angle, "    \g<1>", gh_body)


def convert_admonition(github_admonition: str) -> str:
    header = re.search(GH_ADMONITION_HEADER_PATTERN, github_admonition, flags=re.IGNORECASE)
    mm_header = convert_admonition_header(header.group())
    mm_body = convert_admonition_body(github_admonition[header.end():])
    return mm_header + mm_body


class AdmonitionConverter(BasePlugin):
    def on_page_markdown(
        self, markdown: str, /, *, page: Page, config: MkDocsConfig, files: Files
    ) -> str | None:
        """"Converts all instances of Github admonition to MM admonitions."""
        admonition_matches = GH_ADMONITION_PATTERN.finditer(markdown)
        codeblock_matches = list(GH_CODEBLOCK_PATTERN.finditer(markdown))

        def not_in_codeblock(admonition: re.Match) -> bool:
            return not any(
                codeblock.start() < admonition.start() < codeblock.end()
                for codeblock in codeblock_matches
            )
        admonitions_to_convert = list(filter(not_in_codeblock, admonition_matches))

        # We traverse backwards so that the match indices stay correct
        for match in reversed(admonitions_to_convert):
            mm_admonition = convert_admonition(match.group())
            markdown = markdown[:match.start()] + mm_admonition + markdown[match.end():]
        return markdown
