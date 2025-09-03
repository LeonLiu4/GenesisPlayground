from dataclasses import dataclass
from typing import Any, Mapping, Optional, Tuple, Generic, TypeVar, Dict
import torch
from typing import Final
from abc import ABC, abstractmethod

class BaseEnv(ABC):
    """Core simulator/task with a minimal, tensor-only API. """

    def __init__(self, device: torch.device, seed: int | None = None):
        self.device: Final[torch.device] = device
        self._rng = torch.Generator(device=self.device)  # seeding for any stochastic ops
        if seed is not None:
            self._rng.manual_seed(int(seed))
        self._episode_steps: int = 0
        self._episode_length_limit: int | None = None

    def reset(self) -> None:
        envs_idx = torch.IntTensor(range(self.num_envs))
        self.reset_idx(envs_idx=envs_idx)
 
    @abstractmethod
    def reset_idx(self, envs_idx: torch.IntTensor):
        ...
    
    @abstractmethod
    def apply_action(self, action: torch.Tensor) -> None:
        ...
        
    @abstractmethod
    def get_observations(self) -> torch.Tensor:
        ...
        
    @abstractmethod
    def get_extra_infos(self) -> dict[str, Any]:
        ...

    @abstractmethod
    def get_terminated(self) -> torch.Tensor:
        ...
        
    @abstractmethod
    def get_truncated(self) -> torch.Tensor:
        ...
        
    @abstractmethod
    def get_reward(self) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        ...
        
    @property
    @abstractmethod
    def num_envs(self) -> int:
        ...

    def observation_spec(self) -> Mapping[str, Any]:
        return {}

    def action_spec(self) -> Mapping[str, Any]:
        return {}

    def episode_steps(self) -> int:
        return self._episode_steps

    def set_time_limit(self, max_steps: Optional[int]) -> None:
        self._episode_length_limit = max_steps

