from admonitions.admonition import AdmonitionConverter
# import src.admonitions.admonition


def test_gh_tip_alert():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        "> [!tip]\n> This is a tip admonition.\n", page=None, config=None, files=None
    )
    # THEN
    assert converted == '!!! tip "Tip"\n    This is a tip admonition.\n'


def test_gh_multiline_body():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        "> [!note]\n> This is a note admonition,\n> that spans over two lines.\n",
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert (
        converted
        == '!!! note "Note"\n    This is a note admonition,\n    that spans over two lines.\n'
    )


def test_caution_alert_becomes_danger():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        "> [!caution]\n> This is a caution admonition.\n",
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert converted == '!!! danger "Caution"\n    This is a caution admonition.\n'


def test_important_alert_becomes_warning():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        "> [!important]\n> This is an important admonition.\n",
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert (
        converted == '!!! warning "Important"\n    This is an important admonition.\n'
    )


def test_alert_within_codeblock_isnt_converted():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    original = "Here is the alert syntax:\n```markdown\n> [!tip]\n> This is a tip admonition.\n```\n"
    converted = converter.on_page_markdown(original, page=None, config=None, files=None)
    # THEN
    assert converted == original


def test_alert_containing_codeblock_is_converted():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    original = '> [!tip]\n> Some code expert:\n> ```json\n> {"a": 123}\n> ```\n'
    converted = converter.on_page_markdown(original, page=None, config=None, files=None)
    # THEN
    assert (
        converted
        == '!!! tip "Tip"\n    Some code expert:\n    ```json\n    {"a": 123}\n    ```\n'
    )


def test_gl_overridden_title():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        "> [!tip] Alert titles can be overridden\n> This is a tip admonition with overridden title.\n",
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert (
        converted
        == '!!! tip "Alert titles can be overridden"\n    This is a tip admonition with overridden title.\n'
    )


def test_gl_multiline_alert():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        ">>> [!tip]\nThis is a tip admonition.\n>>>\n",
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert converted == '!!! tip "Tip"\n    This is a tip admonition.\n\n'


def test_gl_complex():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        ">>> [!WARNING] Inception alert\nHere is the alert syntax:\n```markdown\n> [!tip]\n> This is a tip admonition.\n```\n>>>\n",
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert (
        converted
        == '!!! warning "Inception alert"\n    Here is the alert syntax:\n    ```markdown\n    > [!tip]\n    > This is a tip admonition.\n    ```\n\n'
    )
