from itertools import permutations

from admonitions._common import convert_alerts
from admonitions.flavors.github import GitHubAlert
from admonitions.flavors.gitlab import GitLabMultilineAlert, GitLabTitledAlert


def test_flavor_order_doesnt_matter():
    # GIVEN
    flavors = [GitHubAlert(), GitLabTitledAlert(), GitLabMultilineAlert()]
    original = (
        "> [!tip] Overridden title\n> [!note]\n> This is the body.\n\n"
        "> [!note]\n> [!tip] Overridden title\n> This is the body.\n\n"
        ">>> [!note]\n> [!tip]\n> Inner tip.\n>>>\n"
    )
    # WHEN
    converted = {convert_alerts(original, *order) for order in permutations(flavors)}
    # THEN
    assert len(converted) == 1
