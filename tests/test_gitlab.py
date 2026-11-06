from admonitions._common import convert_alerts
from admonitions.admonition import AdmonitionConverter
from admonitions.flavors import gitlab


def test_overridden_title():
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


def test_multiline_blockquote_alert():
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


def test_multiline_alert_with_title_and_codeblock():
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


def test_title_pattern_ignores_gh_alert():
    # GIVEN
    original = "> [!tip]\n> This is a tip admonition.\n"
    # WHEN
    converted = convert_alerts(original, gitlab.TITLED_ALERT_PATTERN)
    # THEN
    assert converted == original
