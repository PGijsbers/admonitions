from textwrap import dedent

from admonitions.admonition import AdmonitionConverter


def test_alert_within_codeblock_isnt_converted():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    original = dedent("""\
        Here is the alert syntax:
        ```markdown
        > [!tip]
        > This is a tip admonition.
        ```
    """)
    converted = converter.on_page_markdown(original, page=None, config=None, files=None)
    # THEN
    assert converted == original


def test_alert_containing_codeblock_is_converted():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    original = dedent("""\
        > [!tip]
        > Some code expert:
        > ```json
        > {"a": 123}
        > ```
    """)
    converted = converter.on_page_markdown(original, page=None, config=None, files=None)
    # THEN
    assert converted == dedent("""\
        !!! tip "Tip"
            Some code expert:
            ```json
            {"a": 123}
            ```
    """)


def test_alert_surrounded_by_codeblocks_is_converted():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        dedent("""\
            ```text
            code block
            before
            ```

            > [!tip]
            > This is the alert.

            ```
            code block
            after
            ```
        """),
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert converted == dedent("""\
        ```text
        code block
        before
        ```

        !!! tip "Tip"
            This is the alert.

        ```
        code block
        after
        ```
    """)
