from itertools import permutations
from textwrap import dedent

from admonitions._common import convert_alerts
from admonitions.flavors.github import GitHubAlert
from admonitions.flavors.gitlab import GitLabMultilineAlert, GitLabTitledAlert


def test_flavor_order_doesnt_matter():
    # GIVEN
    flavors = [GitHubAlert(), GitLabTitledAlert(), GitLabMultilineAlert()]
    original = dedent("""\
        > [!tip] Overridden title
        > [!note]
        > This is the body.

        > [!note]
        > [!tip] Overridden title
        > This is the body.

        >>> [!note]
        > [!tip]
        > Inner tip.
        >>>
    """)
    # WHEN
    converted = {convert_alerts(original, *order) for order in permutations(flavors)}
    # THEN
    assert len(converted) == 1
