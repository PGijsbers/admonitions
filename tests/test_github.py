from textwrap import dedent

from admonitions._common import convert_alerts
from admonitions.admonition import AdmonitionConverter
from admonitions.flavors.github import GitHubAlert


def test_tip_alert():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        dedent("""\
            > [!tip]
            > This is a tip admonition.
        """),
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert converted == dedent("""\
        !!! tip "Tip"
            This is a tip admonition.
    """)


def test_multiline_body():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        dedent("""\
            > [!note]
            > This is a note admonition,
            > that spans over two lines.
        """),
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert converted == dedent("""\
        !!! note "Note"
            This is a note admonition,
            that spans over two lines.
    """)


def test_alert_with_blank_lines():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        "> [!note]\n> This is the first chapter.\n>\n> This is the second chapter.\n",
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert (
        converted
        == '!!! note "Note"\n    This is the first chapter.\n    \n    This is the second chapter.\n'
    )


def test_alert_at_end_of_file_without_newline():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        dedent("""\
            > [!warning]
            > This is a warning admonition."""),
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert converted == dedent("""\
        !!! warning "Warning"
            This is a warning admonition.
    """)


def test_alert_with_blank_line_at_end_of_file_without_newline():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        "> [!warning]\n> \n> This is a warning admonition.",
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert (
        converted == '!!! warning "Warning"\n    \n    This is a warning admonition.\n'
    )


def test_alert_followed_by_empty_line():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        dedent("""\
            > [!warning]
            > This is a warning admonition.

        """),
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert converted == dedent("""\
        !!! warning "Warning"
            This is a warning admonition.

    """)


def test_pattern_ignores_overridden_title():
    # GIVEN
    original = dedent("""\
        > [!tip] Alert titles can be overridden
        > This is a tip admonition.
    """)
    # WHEN
    converted = convert_alerts(original, GitHubAlert())
    # THEN
    assert converted == original
