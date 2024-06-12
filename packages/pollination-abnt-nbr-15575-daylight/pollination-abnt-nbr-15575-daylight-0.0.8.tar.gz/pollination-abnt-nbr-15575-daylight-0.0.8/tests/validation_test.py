from pollination.abnt_nbr_15575_daylight.entry import AbntNbr15575DaylightEntryPoint
from queenbee.recipe.dag import DAG


def test_abnt_nbr_15575_daylight():
    recipe = AbntNbr15575DaylightEntryPoint().queenbee
    assert recipe.name == 'abnt-nbr15575-daylight-entry-point'
    assert isinstance(recipe, DAG)
