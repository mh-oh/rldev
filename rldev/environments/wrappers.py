
import gymnasium

from gymnasium import spaces
from gymnasium.utils.step_api_compatibility import convert_to_done_step_api


class BoxObservation(gymnasium.wrappers.FlattenObservation):

  def __init__(self, env):
    u""""""

    observation_space = env.observation_space
    if not isinstance(observation_space, spaces.Dict):
      raise ValueError(f"")
    self.dict_observation_space = observation_space

    super().__init__(env)

  def dict_observation(self, observation):
    return spaces.unflatten(
      self.dict_observation_space, observation)


class SuccessInfo(gymnasium.Wrapper):

  def __init__(self, env):
    super().__init__(env)

  def step(self, action):
    *step, info = super().step(action)
    if "is_success" in info:
      info["success"] = info["is_success"]
    return *step, info


class GymApi(gymnasium.Wrapper):

  def __init__(self, env):
    super().__init__(env)
    self._seed = None
  
  def reset(self):
    seed = self._seed
    if seed is None:
      return self.env.reset()[0]
    observation, info = self.env.reset(seed=seed)
    self.env.observation_space.seed(seed=seed)
    self.env.action_space.seed(seed=seed)
    self._seed = None
    return observation
  
  def step(self, action):
    step_return = self.env.step(action)
    return convert_to_done_step_api(step_return)

  def seed(self, seed):
    self._seed = seed