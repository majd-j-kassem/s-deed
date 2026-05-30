import numpy as np
import pytest

from src.noise_model import ContextDependentGMM

# === FIXTURES ===


@pytest.fixture
def full_noise_config():
    """Provides the full configuration required by ContextDependentGMM."""
    return {
        "mu_nominal": [0.0, 0.0],
        "mu_anomalous": {"base": [0.0, 0.0], "variability": 0.01},
        "sigma_nominal": {"base": 0.01, "jitter": 0.001},
        "sigma_anomalous": {"base": 0.1, "jitter": 0.01},
        "critical_distance": {"base": 3.0, "adaptive": False, "adaptation_std": 0.1},
        "anomaly_probability": {
            "base_rate": 0.01,
            "distance_multiplier": 0.1,
            "max_anomaly_prob": 0.9,
        },
    }


@pytest.fixture
def mock_rng():
    return np.random.default_rng(seed=42)


# === TEST CASES ===


def test_noise_model_context_switching(mock_rng, full_noise_config):
    """Verifies GMM shifts distributions between safe and dangerous zones."""
    # Note: Corrected parameter name from env_cfg to noise_cfg
    model = ContextDependentGMM(rng=mock_rng, noise_cfg=full_noise_config)

    safe_noises = np.array(
        [model.sample_noise(dist_to_obstacle=10.0) for _ in range(100)]
    )
    # Check that in safe zone, noise remains relatively small
    assert np.mean(np.abs(safe_noises)) < 0.1

    danger_noises = np.array(
        [model.sample_noise(dist_to_obstacle=1.0) for _ in range(100)]
    )
    # Check that in danger zone, higher variance (anomalous) is triggered
    assert np.any(np.abs(danger_noises) > 0.05)


def test_noise_model_determinism(full_noise_config):
    """Verifies that identical seeds produce identical sequences."""
    rng_1 = np.random.default_rng(seed=42)
    rng_2 = np.random.default_rng(seed=42)

    model_1 = ContextDependentGMM(rng=rng_1, noise_cfg=full_noise_config)
    model_2 = ContextDependentGMM(rng=rng_2, noise_cfg=full_noise_config)

    seq_1 = [model_1.sample_noise(dist_to_obstacle=2.0) for _ in range(10)]
    seq_2 = [model_2.sample_noise(dist_to_obstacle=2.0) for _ in range(10)]

    np.testing.assert_array_equal(seq_1, seq_2)
