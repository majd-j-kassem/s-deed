import numpy as np
import pytest

from src.environment import StochasticEnv

# === FIXTURES (The Setup Crew) ===


@pytest.fixture
def env_config():
    """Provides a standard configuration for the environment, \
        including nested simulation settings."""
    env_cfg = {
        "ego_start": [0.0, 0.0],
        "ego_speed": 1.0,
        "obstacle_start": [6.0, 2.0],
        "obstacle_velocity": [0.0, -0.5],
        "goal": [10.0, 0.0],
        "collision_threshold": 0.4,
    }

    # Integration tests must provide the full configuration schema
    # expected by StochasticEnv and its dependencies (ContextDependentGMM).
    sim_cfg = {
        "simulation": {"dt": 0.1},
        "physics_engine": {"goal_threshold": 0.2, "velocity_drift_std": 0.05},
        "noise_model": {
            "mu_nominal": [0.0, 0.0],
            "mu_anomalous": {"base": [0.0, 0.0], "variability": 0.01},
            "sigma_nominal": {"base": 0.05, "jitter": 0.005},
            "sigma_anomalous": {"base": 0.1, "jitter": 0.01},
            "critical_distance": {
                "base": 3.0,
                "adaptive": False,
                "adaptation_std": 0.1,
            },
            "anomaly_probability": {
                "base_rate": 0.01,
                "distance_multiplier": 0.1,
                "max_anomaly_prob": 0.5,
            },
        },
    }
    return env_cfg, sim_cfg


@pytest.fixture
def env(env_config):
    """Provides a fresh, isolated StochasticEnv instance for every test."""
    rng = np.random.default_rng(seed=42)
    env_cfg, sim_cfg = env_config
    return StochasticEnv(rng=rng, env_cfg=env_cfg, sim_cfg=sim_cfg)


# === TEST CASES (The Logic) ===


def test_environment_deterministic_step(env):
    """Verifies horizontal ego movement works."""
    ego_pos, _, _, _ = env.step(steering_angle=0.0, noise_enabled=False)

    assert ego_pos[0] == pytest.approx(0.1)
    assert ego_pos[1] == 0.0


def test_environment_state_immutability(env):
    """Verifies arrays returned are protected copies and cannot be \
        modified externally."""
    ego_gt, _ = env.get_ground_truth_states()
    ego_gt[0] = 999.9

    ego_gt_clean, _ = env.get_ground_truth_states()
    assert ego_gt_clean[0] == 0.0


def test_environment_collision_trigger(env_config):
    """Verifies that spawning the ego inside the collision zone triggers done=True."""
    env_cfg, sim_cfg = env_config
    env_cfg["ego_start"] = [6.0, 2.0]
    rng = np.random.default_rng(seed=42)

    custom_env = StochasticEnv(rng=rng, env_cfg=env_cfg, sim_cfg=sim_cfg)
    _, _, collision, done = custom_env.step(steering_angle=0.0)

    assert collision
    assert done
