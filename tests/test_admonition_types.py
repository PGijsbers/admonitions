from admonitions.admonition import AdmonitionConverter


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
