import dataclasses

from randovania.bitpacking.bitpacking import BitPackDataclass
from randovania.bitpacking.json_dataclass import JsonDataclass
from randovania.games.game import RandovaniaGame
from randovania.layout.base.base_configuration import BaseConfiguration


@dataclasses.dataclass(frozen=True)
class AM2RArtifactConfig(BitPackDataclass, JsonDataclass):
    prefer_metroids: bool
    prefer_bosses: bool
    required_artifacts: int = dataclasses.field(metadata={"min": 0, "max": 46, "precision": 1})

@dataclasses.dataclass(frozen=True)
class AM2RConfiguration(BaseConfiguration):
    energy_per_tank: int = dataclasses.field(metadata={"min": 1, "max": 1000, "precision": 1})
    septogg_helpers: bool
    change_level_design: bool   # TODO: requires changes in DB!
    artifacts: AM2RArtifactConfig
    skip_cutscenes: bool
    respawn_bomb_blocks: bool
    remove_grave_grotto_blocks: bool
    fusion_mode: bool # TODO: requires DB changes
    nest_pipes: bool # TODO: requires DB changes
    # TODO: more setting for individual block placements, like bombs to a3?


    @classmethod
    def game_enum(cls) -> RandovaniaGame:
        return RandovaniaGame.AM2R

    def active_layers(self) -> set[str]:
        result = super().active_layers()

        #if self.include_extra_pickups:
        #    result.add("extra_pickups")

        return result
