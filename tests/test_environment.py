import numpy as np
import pytest

from src.environment import StochasticEnv


def get_full_config():
    """
    Returns a configuration dictionary that matches the expected
    structure of StochasticEnv and ContextDependentGMM.
    """
    env_cfg = {
        "ego_start": [0.0, 0.0],
        "ego_speed": 1.0,
        "obstacle_start": [5.0, 0.0],
        "obstacle_velocity": [0.0, 0.0],
        "goal": [10.0, 0.0],
        "collision_threshold": 0.5,
    }

    sim_cfg = {
        "simulation": {"dt": 0.1},
        "physics_engine": {"goal_threshold": 0.2, "velocity_drift_std": 0.0},
        "noise_model": {
            "mu_nominal": [0.0, 0.0],
            "mu_anomalous": {"base": [0.0, 0.0], "variability": 0.01},
            "sigma_nominal": {"base": 0.0, "jitter": 0.0},
            "sigma_anomalous": {"base": 0.0, "jitter": 0.0},
            "critical_distance": {
                "base": 3.0,
                "adaptive": False,
                "adaptation_std": 0.1,
            },
            "anomaly_probability": {
                "base_rate": 0.0,
                "distance_multiplier": 0.0,
                "max_anomaly_prob": 0.0,
            },
        },
    }
    return env_cfg, sim_cfg


# === Test Cases ===


def test_step_kinematics():
    """Verify ego moves exactly as predicted by steering_angle=0."""
    rng = np.random.default_rng(seed=42)
    env_cfg, sim_cfg = get_full_config()
    env = StochasticEnv(rng=rng, env_cfg=env_cfg, sim_cfg=sim_cfg)

    # 0.0 + (1.0 * cos(0) * 0.1) = 0.1
    pos, _, _, _ = env.step(steering_angle=0.0, noise_enabled=False)
    assert pos[0] == pytest.approx(0.1)
    assert pos[1] == 0.0


def test_collision_detection():
    """Verify collision is detected when within threshold."""
    rng = np.random.default_rng(seed=42)
    env_cfg, sim_cfg = get_full_config()
    env = StochasticEnv(rng=rng, env_cfg=env_cfg, sim_cfg=sim_cfg)

    env.obstacle_pos = np.array([0.1, 0.0])
    _, _, collision, done = env.step(steering_angle=0.0, noise_enabled=False)

    # Use assert statement directly for boolean values from numpy
    assert collision
    assert done


def test_goal_reached():
    """Verify goal reached condition."""
    rng = np.random.default_rng(seed=42)
    env_cfg, sim_cfg = get_full_config()
    env = StochasticEnv(rng=rng, env_cfg=env_cfg, sim_cfg=sim_cfg)

    env.ego_pos = np.array([9.9, 0.0])
    _, _, _, done = env.step(steering_angle=0.0, noise_enabled=False)

    assert done
