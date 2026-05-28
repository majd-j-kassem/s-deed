import numpy as np
import pytest

from src.noise_model import ContextDependentGMM

# === FIXTURES ===


@pytest.fixture
def default_config():
    """Provides a standard configuration dict."""
    return {"critical_distance": 3.0}


@pytest.fixture
def mock_rng():
    """Provides a clean NumPy random generator."""
    return np.random.default_rng(seed=42)


# === TEST CASES ===


def test_noise_model_context_switching(mock_rng, default_config):
    """Verifies GMM shifts distributions between safe and dangerous zones."""
    model = ContextDependentGMM(rng=mock_rng, env_cfg=default_config)

    # Use vectorized sampling for statistical stability
    safe_noises = np.array(
        [model.sample_noise(dist_to_obstacle=10.0) for _ in range(100)]
    )
    assert np.mean(np.abs(safe_noises)) < 0.05

    danger_noises = np.array(
        [model.sample_noise(dist_to_obstacle=1.0) for _ in range(100)]
    )
    assert np.any(np.abs(danger_noises) > 0.1)


@pytest.mark.parametrize(
    "distance, expected_safe",
    [
        (3.01, True),  # Safe zone
        (2.99, False),  # Danger zone
    ],
)
def test_noise_model_boundary_switching(distance, expected_safe, default_config):
    """Verifies that the probability shift occurs exactly at the boundary edge."""
    # Isolated seed to ensure boundary test consistency
    rng = np.random.default_rng(seed=100)
    model = ContextDependentGMM(rng=rng, env_cfg=default_config)

    samples = np.array(
        [model.sample_noise(dist_to_obstacle=distance) for _ in range(50)]
    )

    if expected_safe:
        assert np.mean(np.abs(samples)) < 0.05
    else:
        assert np.any(np.abs(samples) > 0.1)


def test_noise_model_determinism(default_config):
    """Verifies that identical seeds produce 100% identical noise sequences."""
    rng_1 = np.random.default_rng(seed=42)
    rng_2 = np.random.default_rng(seed=42)

    model_1 = ContextDependentGMM(rng=rng_1, env_cfg=default_config)
    model_2 = ContextDependentGMM(rng=rng_2, env_cfg=default_config)

    seq_1 = [model_1.sample_noise(dist_to_obstacle=2.0) for _ in range(10)]
    seq_2 = [model_2.sample_noise(dist_to_obstacle=2.0) for _ in range(10)]

    np.testing.assert_array_equal(seq_1, seq_2)


def test_noise_model_default_config(mock_rng):
    """Verifies the fallback mechanism when critical_distance key is missing."""
    model = ContextDependentGMM(rng=mock_rng, env_cfg={})
    assert model.critical_distance == 3.0
