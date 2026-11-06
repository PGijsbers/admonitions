from textwrap import dedent

from admonitions._common import convert_alerts
from admonitions.admonition import AdmonitionConverter
from admonitions.flavors.gitlab import GitLabTitledAlert


def test_overridden_title():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        dedent("""\
            > [!tip] Alert titles can be overridden
            > This is a tip admonition with overridden title.
        """),
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert converted == dedent("""\
        !!! tip "Alert titles can be overridden"
            This is a tip admonition with overridden title.
    """)


def test_multiline_blockquote_alert():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        dedent("""\
            >>> [!tip]
            This is a tip admonition.
            >>>
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


def test_multiline_alert_with_title_and_codeblock():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        dedent("""\
            >>> [!WARNING] Inception alert
            Here is the alert syntax:
            ```markdown
            > [!tip]
            > This is a tip admonition.
            ```
            >>>
        """),
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert converted == dedent("""\
        !!! warning "Inception alert"
            Here is the alert syntax:
            ```markdown
            > [!tip]
            > This is a tip admonition.
            ```

    """)


def test_title_pattern_ignores_gh_alert():
    # GIVEN
    original = dedent("""\
        > [!tip]
        > This is a tip admonition.
    """)
    # WHEN
    converted = convert_alerts(original, GitLabTitledAlert())
    # THEN
    assert converted == original


def test_consecutive_multiline_blockquote_alerts_stay_separate():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        dedent("""\
            >>> [!tip]
            First block.
            >>>

            Text between.

            >>> [!note]
            Second block.
            >>>
        """),
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert converted == dedent("""\
        !!! tip "Tip"
            First block.


        Text between.

        !!! note "Note"
            Second block.

    """)


def test_multiline_blockquote_alert_with_crlf_line_endings_keeps_default_title():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        ">>> [!tip]\r\nThis is a tip admonition.\r\n>>>\r\n",
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert converted == '!!! tip "Tip"\n    This is a tip admonition.\n\r\n'
