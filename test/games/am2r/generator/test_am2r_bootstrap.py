from __future__ import annotations

import dataclasses
from random import Random

import pytest

from randovania.game_description.game_patches import GamePatches
from randovania.game_description.resources.pickup_index import PickupIndex
from randovania.games.am2r.generator import AM2RBootstrap
from randovania.games.am2r.generator.pool_creator import METROID_DNA_CATEGORY
from randovania.games.am2r.layout.am2r_configuration import AM2RArtifactConfig
from randovania.generator.pickup_pool import pool_creator

_boss_indices = [111, 3, 6, 14, 11, 50]


@pytest.mark.parametrize(
    ("artifacts", "expected"),
    [
        (AM2RArtifactConfig(True, True, 5), [3, 50, 374, 389, 391]),
        (AM2RArtifactConfig(True, False, 46), range(350, 396)),
        (AM2RArtifactConfig(False, True, 6), _boss_indices),
        (AM2RArtifactConfig(False, False, 0), []),
    ],
)
def test_assign_pool_results(am2r_game_description, am2r_configuration, artifacts, expected):
    patches = GamePatches.create_from_game(
        am2r_game_description, 0, dataclasses.replace(am2r_configuration, artifacts=artifacts)
    )
    pool_results = pool_creator.calculate_pool_results(patches.configuration, patches.game)

    # Run
    result = AM2RBootstrap().assign_pool_results(
        Random(8000),
        patches,
        pool_results,
    )

    # Assert
    shuffled_dna = [pickup for pickup in pool_results.to_place if pickup.pickup_category == METROID_DNA_CATEGORY]

    assert result.starting_equipment == pool_results.starting
    assert set(result.pickup_assignment.keys()) == {PickupIndex(i) for i in expected}
    assert shuffled_dna == []
