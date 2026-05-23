from typing import Any, Dict, Tuple

import numpy as np
from numpy.typing import NDArray

from noise_model import ContextDependentGMM


class StochasticEnv:
    def __init__(
        self, rng: np.random.Generator, env_cfg: Dict[str, Any], sim_cfg: Dict[str, Any]
    ) -> None:
        self.rng: np.random.Generator = rng
        self.dt: float = float(sim_cfg["dt"])
        self.collision_threshold: float = float(env_cfg["collision_threshold"])
        self.ego_pos: NDArray[np.float64] = np.array(env_cfg["ego_start"], dtype=float)
        self.ego_speed: float = float(env_cfg["ego_speed"])
        self.goal: NDArray[np.float64] = np.array(env_cfg["goal"], dtype=float)

        self.obstacle_pos: NDArray[np.float64] = np.array(
            env_cfg["obstacle_start"], dtype=float
        )
        self.obstacle_vel: NDArray[np.float64] = np.array(
            env_cfg["obstacle_velocity"], dtype=float
        )

        # Compositional dependency injection
        self.noise_model = ContextDependentGMM(rng=self.rng, env_cfg=env_cfg)

    def get_ground_truth_states(
        self,
    ) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
        return self.ego_pos.copy(), self.obstacle_pos.copy()

    def step(
        self, steering_angle: float, noise_enabled: bool = True
    ) -> Tuple[NDArray[np.float64], NDArray[np.float64], bool, bool]:
        # 1. Clear, Explicit Ego Kinematics (No cross-contamination)
        delta_x = self.ego_speed * np.cos(steering_angle) * self.dt
        delta_y = self.ego_speed * np.sin(steering_angle) * self.dt

        self.ego_pos[0] = self.ego_pos[0] + delta_x
        self.ego_pos[1] = self.ego_pos[1] + delta_y

        # 2. Stochastic Obstacle Kinematics (Isolated generation)
        velocity_drift: NDArray[np.float64] = self.rng.normal(
            loc=0.0, scale=0.05, size=2
        )
        actual_velocity = self.obstacle_vel + velocity_drift
        self.obstacle_pos += actual_velocity * self.dt

        # 3. Distance Metrics
        dist_to_goal: float = float(np.linalg.norm(self.goal - self.ego_pos))
        dist_to_obstacle: float = float(
            np.linalg.norm(self.obstacle_pos - self.ego_pos)
        )

        # 4. Conditional Measurement Noise
        if noise_enabled:
            position_noise = self.noise_model.sample_noise(dist_to_obstacle)
            noisy_ego_pos = self.ego_pos + position_noise
        else:
            noisy_ego_pos = self.ego_pos.copy()

        # 5. Pipeline Terminal Evaluators
        collision: bool = dist_to_obstacle < self.collision_threshold
        reached_goal: bool = dist_to_goal < 0.2
        done: bool = reached_goal or collision

        return noisy_ego_pos, self.obstacle_pos.copy(), collision, done
