from textwrap import dedent

from admonitions.admonition import AdmonitionConverter


def test_gh_alert_in_gl_alert_body_isnt_converted():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        dedent("""\
            > [!tip] Overridden title
            > [!note]
            > This is the body.
        """),
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert converted == dedent("""\
        !!! tip "Overridden title"
            [!note]
            This is the body.
    """)


def test_nested_alert_isnt_converted():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        "> [!tip]\n> This is the tip content.\n> \n>     > [!note]\n>     > This is the note content.\n",
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert (
        converted
        == '!!! tip "Tip"\n    This is the tip content.\n    \n        > [!note]\n        > This is the note content.\n'
    )


def test_consecutive_alerts_are_converted_as_one():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        dedent("""\
            > [!tip]
            > This is the first body.
            > [!note]
            > This is the second admonition.
        """),
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert converted == dedent("""\
        !!! tip "Tip"
            This is the first body.
            [!note]
            This is the second admonition.
    """)


def test_gh_alert_in_gl_multiline_alert_is_nested():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        dedent("""\
            >>> [!note]
            > [!tip]
            > Inner tip.
            >>>
        """),
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert converted == dedent("""\
        !!! note "Note"
            !!! tip "Tip"
                Inner tip.

    """)
