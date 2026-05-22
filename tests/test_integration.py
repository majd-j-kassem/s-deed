import numpy as np
import pytest
from environment import StochasticEnv


def get_mock_config():
    env_cfg = {
        "ego_start": [0.0, 0.0],
        "ego_speed": 1.0,
        "obstacle_start": [6.0, 2.0],
        "obstacle_velocity": [0.0, 0.0],
        "goal": [10.0, 0.0],
        "collision_threshold": 0.4,
        "critical_distance": 3.0,
    }
    sim_cfg = {"dt": 0.1}
    return env_cfg, sim_cfg


# === TEST CASE 1: Pure Kinematics Validation ===
def test_environment_deterministic_step():
    """Verifies baseline kinematics calculations when stochastic noise is disabled."""
    rng = np.random.default_rng(seed=42)
    env_cfg, sim_cfg = get_mock_config()
    env = StochasticEnv(rng=rng, env_cfg=env_cfg, sim_cfg=sim_cfg)
    
    # FIX: Explicitly disable noise injection to verify pure physics formulas
    ego_pos, _, _, _ = env.step(steering_angle=0.0, noise_enabled=False)
    
    assert ego_pos[0] == pytest.approx(0.1)  # 0.0 + 1.0 * cos(0) * 0.1
    assert ego_pos[1] == pytest.approx(0.0)  # 0.0 + 1.0 * sin(0) * 0.1


# === TEST CASE 2: State Immutability Verification ===
def test_environment_state_immutability():
    """Verifies defensive copying ensures internal positions are read-only snapshot references."""
    rng = np.random.default_rng(seed=42)
    env_cfg, sim_cfg = get_mock_config()
    env = StochasticEnv(rng=rng, env_cfg=env_cfg, sim_cfg=sim_cfg)
    
    ego_pos, _, _, _ = env.step(steering_angle=0.0)
    ego_pos[0] = 999.9  # Malicious mutation attempt
    
    gt_ego, _ = env.get_ground_truth_states()
    assert gt_ego[0] != 999.9


# === TEST CASE 3: Boundary Collision Conditions ===
def test_environment_collision_trigger():
    """Verifies that spawning the ego inside the collision zone triggers done=True."""
    rng = np.random.default_rng(seed=42)
    env_cfg, sim_cfg = get_mock_config()
    env_cfg["ego_start"] = [6.0, 2.0]  # Spawn directly on top of obstacle location
    
    env = StochasticEnv(rng=rng, env_cfg=env_cfg, sim_cfg=sim_cfg)
    _, _, collision, done = env.step(steering_angle=0.0)
    
    assert collision is True
    assert done is True