import numpy as np
from noise_model import ContextDependentGMM


# Helper fixture to provide a standard random generator
def get_mock_rng(seed: int = 42) -> np.random.Generator:
    return np.random.default_rng(seed=seed)


# === TEST CASE 1: Core Context Switching ===
def test_noise_model_context_switching():
    """Verifies GMM shifts distributions between safe and dangerous zones."""
    rng = get_mock_rng()
    env_cfg = {"critical_distance": 3.0}
    model = ContextDependentGMM(rng=rng, env_cfg=env_cfg)

    # 1. Safe Zone: Obstacle is far away (10m). Noise must be minimal on average.
    safe_noises = [model.sample_noise(dist_to_obstacle=10.0) for _ in range(30)]
    # Use aggregate mean to tolerate the 5% baseline anomaly spikes without failing
    assert np.mean(np.abs(safe_noises)) < 0.05

    # 2. Danger Zone: Obstacle is close (1m). Noise must spike due to 70% anomaly rate.
    danger_noises = [model.sample_noise(dist_to_obstacle=1.0) for _ in range(30)]
    # At least some samples must capture the anomalous noise spikes (> 0.1)
    assert np.any(np.abs(danger_noises) > 0.1)


# === TEST CASE 2: Boundary Precision Check ===
def test_noise_model_boundary_switching():
    """Verifies that the probability shift occurs exactly at the boundary edge."""
    # We use a fixed seed to guarantee the random outcomes match our expectations on the edge
    rng = get_mock_rng(seed=100)
    env_cfg = {"critical_distance": 3.0}
    model = ContextDependentGMM(rng=rng, env_cfg=env_cfg)

    # 3.01m is strictly greater than critical_distance -> Baseline safe zone (5% chance)
    boundary_safe = [model.sample_noise(dist_to_obstacle=3.01) for _ in range(20)]
    assert np.mean(np.abs(boundary_safe)) < 0.05

    # 2.99m is strictly less than critical_distance -> Triggers danger zone (70% chance)
    boundary_danger = [model.sample_noise(dist_to_obstacle=2.99) for _ in range(20)]
    assert np.any(np.abs(boundary_danger) > 0.1)


# === TEST CASE 3: System Determinism ===
def test_noise_model_determinism():
    """Verifies that identical seeds produce 100% identical noise sequences."""
    rng_1 = get_mock_rng(seed=42)
    rng_2 = get_mock_rng(seed=42)
    env_cfg = {"critical_distance": 3.0}

    model_1 = ContextDependentGMM(rng=rng_1, env_cfg=env_cfg)
    model_2 = ContextDependentGMM(rng=rng_2, env_cfg=env_cfg)

    # Generate sequences from both identical models
    sequence_1 = [model_1.sample_noise(dist_to_obstacle=2.0) for _ in range(10)]
    sequence_2 = [model_2.sample_noise(dist_to_obstacle=2.0) for _ in range(10)]

    # Assert that every single array element matches perfectly in memory
    np.testing.assert_array_equal(sequence_1, sequence_2)


# === TEST CASE 4: Configuration Fallback ===
def test_noise_model_default_config():
    """Verifies the fallback mechanism when critical_distance key is missing."""
    rng = get_mock_rng()
    empty_env_cfg = {}  # No key provided

    model = ContextDependentGMM(rng=rng, env_cfg=empty_env_cfg)

    # System must fall back cleanly to the default value of 3.0
    assert model.critical_distance == 3.0