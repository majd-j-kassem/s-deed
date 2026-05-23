import numpy as np
import pytest

from environment import StochasticEnv

# === FIXTURES (The Setup Crew) ===


@pytest.fixture
def env_config():
    """Provides a standard configuration for the environment."""
    env_cfg = {
        "ego_start": [0.0, 0.0],
        "ego_speed": 1.0,
        "obstacle_start": [6.0, 2.0],
        "obstacle_velocity": [0.0, -0.5],
        "goal": [10.0, 0.0],
        "collision_threshold": 0.4,
        "critical_distance": 3.0,
    }
    sim_cfg = {"dt": 0.1}
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
    """Verifies arrays returned are protected copies and \
        cannot be modified externally."""
    ego_gt, _ = env.get_ground_truth_states()

    # Attempt "malicious" modification
    ego_gt[0] = 999.9

    # Verify the internal state remains untouched
    ego_gt_clean, _ = env.get_ground_truth_states()
    assert ego_gt_clean[0] == 0.0


def test_environment_collision_trigger():
    """Verifies that spawning the ego inside the collision zone triggers done=True."""
    # We override setup here because this test requires a specific start position
    rng = np.random.default_rng(seed=42)
    env_cfg = {
        "ego_start": [6.0, 2.0],
        "obstacle_start": [6.0, 2.0],
        "collision_threshold": 0.4,
        "critical_distance": 3.0,
        "ego_speed": 1.0,
        "obstacle_velocity": [0.0, -0.5],
        "goal": [10.0, 0.0],
    }
    sim_cfg = {"dt": 0.1}

    custom_env = StochasticEnv(rng=rng, env_cfg=env_cfg, sim_cfg=sim_cfg)
    _, _, collision, done = custom_env.step(steering_angle=0.0)

    assert collision is True
    assert done is True
