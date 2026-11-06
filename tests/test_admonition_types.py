from textwrap import dedent

from admonitions.admonition import AdmonitionConverter


def test_caution_alert_becomes_danger():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        dedent("""\
            > [!caution]
            > This is a caution admonition.
        """),
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert converted == dedent("""\
        !!! danger "Caution"
            This is a caution admonition.
    """)


def test_important_alert_becomes_warning():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        dedent("""\
            > [!important]
            > This is an important admonition.
        """),
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert converted == dedent("""\
        !!! warning "Important"
            This is an important admonition.
    """)
