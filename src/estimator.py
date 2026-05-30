from typing import Any, Dict

import numpy as np
from numpy.typing import NDArray


class ParticleFilter:
    """
    Particle Filter implementation for state estimation in S-DEED.
    Estimates the 2D position of the ego vehicle based on noisy observations.
    Updated to handle anomalous noise regimes by scaling measurement variance.
    """

    def __init__(
        self,
        estimator_cfg: Dict[str, Any],
        rng: np.random.Generator,
    ) -> None:
        self.N: int = int(estimator_cfg["num_particles"])
        self.state_dim: int = 2
        self.process_noise: float = float(estimator_cfg["process_noise"])
        # Base measurement noise from config
        self.measurement_noise: float = float(estimator_cfg["measurement_noise"])
        self.resample_threshold: float = float(estimator_cfg["resample_threshold"])
        self.rng: np.random.Generator = rng

        self.particles: NDArray[np.float64] = np.zeros((self.N, self.state_dim))
        self.weights: NDArray[np.float64] = np.ones(self.N) / self.N

    def predict(self, steering_angle: float, dt: float, ego_speed: float) -> None:
        """Propagates particles using motion model with process noise."""
        delta: NDArray[np.float64] = np.array(
            [
                ego_speed * np.cos(steering_angle) * dt,
                ego_speed * np.sin(steering_angle) * dt,
            ],
            dtype=np.float64,
        )
        noise: NDArray[np.float64] = self.rng.normal(
            0.0, self.process_noise, size=self.particles.shape
        )
        self.particles += delta + noise

    def update(
        self, measurement: NDArray[np.float64], is_anomalous: bool = False
    ) -> None:
        """
        Update step: Updates particle weights using Gaussian likelihood.
        If the system is in an anomalous regime, we inflate the measurement noise
        to account for higher observation uncertainty.
        """
        # Inflate noise if anomalous to prevent filter over-confidence
        effective_sigma = (
            self.measurement_noise * 5.0 if is_anomalous else self.measurement_noise
        )
        sigma2: float = effective_sigma**2

        # Calculate squared Euclidean distances for likelihood weighting
        dist: NDArray[np.float64] = np.sum((self.particles - measurement) ** 2, axis=1)

        # Compute Gaussian likelihood
        likelihood: NDArray[np.float64] = np.exp(-0.5 * dist / sigma2)

        self.weights *= likelihood
        self.weights += 1.0e-300
        self.weights /= np.sum(self.weights)

    def resample(self) -> None:
        """Systematic Resampling to maintain particle diversity."""
        n_eff: float = 1.0 / np.sum(self.weights**2)
        if n_eff < (self.N * self.resample_threshold):
            positions = (self.rng.random() + np.arange(self.N)) / self.N
            cumulative_sum = np.cumsum(self.weights)
            indices = np.searchsorted(cumulative_sum, positions)
            self.particles = self.particles[indices]
            self.weights.fill(1.0 / self.N)
