import numpy as np
import pytest

from environment import StochasticEnv


# Helper fixture to provide a standard configuration
def get_mock_config():
    env_cfg = {
        "ego_start": [0.0, 0.0],
        "ego_speed": 1.0,
        "obstacle_start": [6.0, 2.0],
        "obstacle_velocity": [0.0, -0.5],
        "goal": [10.0, 0.0],
        "collision_threshold": 0.4,
        "critical_distance": 3.0
    }
    sim_cfg = {"dt": 0.1}
    return env_cfg, sim_cfg


# === TEST CASE 1: Kinematics ===
def test_environment_deterministic_step():
    """Verifies horizontal ego movement works (cos(0) = 1)."""
    rng = np.random.default_rng(seed=42)
    env_cfg, sim_cfg = get_mock_config()
    env = StochasticEnv(rng=rng, env_cfg=env_cfg, sim_cfg=sim_cfg)

    # FIX: Explicitly turn off the GMM noise propagation layer for this calculation
    ego_pos, _, _, _ = env.step(steering_angle=0.0, noise_enabled=False)

    assert ego_pos[0] == pytest.approx(0.1)  # 0.0 + 1.0 * 1.0 * 0.1
    assert ego_pos[1] == 0.0


# === TEST CASE 2: State Integrity ===
def test_environment_state_immutability():
    """Verifies arrays returned by get_ground_truth_states are protected copies."""
    rng = np.random.default_rng(seed=42)
    env_cfg, sim_cfg = get_mock_config()
    env = StochasticEnv(rng=rng, env_cfg=env_cfg, sim_cfg=sim_cfg)
    ego_gt, _ = env.get_ground_truth_states()
    ego_gt[0] = 999.9  # Attempt malicious external change
    ego_gt_clean, _ = env.get_ground_truth_states()
    assert ego_gt_clean[0] == 0.0  # Should remain completely unchanged


# === TEST CASE 3: Boundary Condition (Collision) ===
def test_environment_collision_trigger():
    """Verifies that spawning the ego inside the collision zone triggers done=True."""
    rng = np.random.default_rng(seed=42)
    env_cfg, sim_cfg = get_mock_config()
    # Intentionally spawn ego right on top of the obstacle
    env_cfg["ego_start"] = [6.0, 2.0]
    env = StochasticEnv(rng=rng, env_cfg=env_cfg, sim_cfg=sim_cfg)
    _, _, collision, done = env.step(steering_angle=0.0)
    assert collision is True
    assert done is True
