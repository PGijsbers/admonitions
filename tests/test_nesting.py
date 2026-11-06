from admonitions.admonition import AdmonitionConverter


def test_gh_alert_in_gl_alert_body_isnt_converted():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        "> [!tip] Overridden title\n> [!note]\n> This is the body.\n",
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert (
        converted == '!!! tip "Overridden title"\n    [!note]\n    This is the body.\n'
    )


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
        "> [!tip]\n> This is the first body.\n> [!note]\n> This is the second admonition.\n",
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert (
        converted
        == '!!! tip "Tip"\n    This is the first body.\n    [!note]\n    This is the second admonition.\n'
    )


def test_gh_alert_in_gl_multiline_alert_is_nested():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        ">>> [!note]\n> [!tip]\n> Inner tip.\n>>>\n",
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert converted == '!!! note "Note"\n    !!! tip "Tip"\n        Inner tip.\n\n'
