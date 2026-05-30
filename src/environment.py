from typing import Any, Dict, Tuple

import numpy as np
from numpy.typing import NDArray

from src.noise_model import ContextDependentGMM


class StochasticEnv:
    """
    Simulation environment for S-DEED: handles state transition and sensor noise.
    Physics parameters are dynamically loaded from configuration.
    """

    def __init__(
        self, rng: np.random.Generator, env_cfg: Dict[str, Any], sim_cfg: Dict[str, Any]
    ) -> None:
        self.rng = rng
        self.dt = float(sim_cfg["simulation"]["dt"])
        self.collision_threshold = float(env_cfg["collision_threshold"])

        # Load physics parameters from configuration (Single Source of Truth: base.yaml)
        physics = sim_cfg.get("physics_engine", {})
        self.goal_threshold = float(physics.get("goal_threshold", 0.2))
        self.drift_std = float(physics.get("velocity_drift_std", 0.05))

        self.ego_pos = np.array(env_cfg["ego_start"], dtype=float)
        self.ego_speed = float(env_cfg["ego_speed"])
        self.goal = np.array(env_cfg["goal"], dtype=float)

        self.obstacle_pos = np.array(env_cfg["obstacle_start"], dtype=float)
        self.obstacle_vel = np.array(env_cfg["obstacle_velocity"], dtype=float)

        self.noise_model = ContextDependentGMM(
            rng=self.rng, noise_cfg=sim_cfg["noise_model"]
        )

    def get_ground_truth_states(
        self,
    ) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Returns the true positions of ego and obstacle."""
        return self.ego_pos.copy(), self.obstacle_pos.copy()

    def step(
        self, steering_angle: float, noise_enabled: bool = True
    ) -> Tuple[NDArray[np.float64], NDArray[np.float64], bool, bool]:
        """
        Executes one simulation step.
        Returns: (noisy_ego_pos, obstacle_pos, collision, done)
        """
        # 1. Update Ego motion
        self.ego_pos[0] += self.ego_speed * np.cos(steering_angle) * self.dt
        self.ego_pos[1] += self.ego_speed * np.sin(steering_angle) * self.dt

        # 2. Update Obstacle motion with stochastic drift from config
        velocity_drift = self.rng.normal(0.0, self.drift_std, size=2)
        self.obstacle_pos += (self.obstacle_vel + velocity_drift) * self.dt

        # 3. Calculate distances
        dist_to_goal = np.linalg.norm(self.goal - self.ego_pos)
        dist_to_obstacle: float = np.linalg.norm(self.obstacle_pos - self.ego_pos)

        # 4. Inject noise if enabled
        if noise_enabled:
            position_noise = self.noise_model.sample_noise(
                dist_to_obstacle=dist_to_obstacle
            )
            noisy_ego_pos = self.ego_pos + position_noise
        else:
            noisy_ego_pos = self.ego_pos.copy()

        # 5. Evaluate termination conditions using config threshold
        collision: np.bool_ = dist_to_obstacle < self.collision_threshold
        reached_goal = dist_to_goal < self.goal_threshold
        done = collision or reached_goal

        return noisy_ego_pos, self.obstacle_pos.copy(), collision, done
