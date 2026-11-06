from admonitions.admonition import AdmonitionConverter


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


def test_alert_surrounded_by_codeblocks_is_converted():
    # GIVEN
    converter = AdmonitionConverter()
    # WHEN
    converted = converter.on_page_markdown(
        "```text\ncode block\nbefore\n```\n\n> [!tip]\n> This is the alert.\n\n```\ncode block\nafter\n```\n",
        page=None,
        config=None,
        files=None,
    )
    # THEN
    assert (
        converted
        == '```text\ncode block\nbefore\n```\n\n!!! tip "Tip"\n    This is the alert.\n\n```\ncode block\nafter\n```\n'
    )
