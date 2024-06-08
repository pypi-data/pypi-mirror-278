# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from typing import Any, Dict, SupportsFloat, Tuple

import composabl_core.utils.logger as logger_util
import gymnasium as gym
from composabl_core.agent.scenario import Scenario
from composabl_core.networking.server_composabl import ServerComposabl
from gymnasium.envs.registration import EnvSpec

from {{NAME_MODULE}}.sim import Env

logger = logger_util.get_logger(__name__)


class SimImpl(ServerComposabl):
    def __init__(self):
        self.env = Env()

    async def make(self, env_id: str, env_init: dict) -> EnvSpec:
        spec = {"id": "starship", "max_episode_steps": 400}
        return spec

    async def sensor_space_info(self) -> gym.Space:
        return self.env.sensor_space

    async def action_space_info(self) -> gym.Space:
        return self.env.action_space

    async def action_space_sample(self) -> Any:
        return self.env.action_space.sample()

    async def reset(self) -> Tuple[Any, Dict[str, Any]]:
        sensors, info = self.env.reset()
        return sensors, info

    async def step(
        self, action
    ) -> Tuple[Any, SupportsFloat, bool, bool, Dict[str, Any]]:
        return self.env.step(action)

    async def close(self):
        self.env.close()

    async def set_scenario(self, scenario):
        self.env.scenario = scenario

    async def get_scenario(self):
        if self.env.scenario is None:
            return Scenario({"dummy": 0})

        return self.env.scenario

    async def set_render_mode(self, render_mode):
        self.env.render_mode = render_mode

    async def get_render_mode(self):
        return self.env.render_mode

    async def get_render(self):
        return self.env.get_render_frame()
