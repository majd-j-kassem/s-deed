import numpy as np
from numpy.typing import NDArray


class ParticleFilter:
    def __init__(
        self,
        num_particles: int,
        process_noise: float,
        measurement_noise: float,
        resample_threshold: float,
        rng: np.random.Generator,
    ) -> None:
        self.N: int = num_particles
        self.state_dim: int = 2
        self.process_noise: float = process_noise
        self.measurement_noise: float = measurement_noise
        self.resample_threshold: float = resample_threshold
        self.rng: np.random.Generator = rng

        self.particles: NDArray[np.float64] = np.zeros((self.N, self.state_dim))
        self.weights: NDArray[np.float64] = np.ones(self.N) / self.N

    def predict(self, u: float, dt: float, ego_speed: float) -> None:
        delta: NDArray[np.float64] = np.array(
            [ego_speed * np.cos(u) * dt, ego_speed * np.sin(u) * dt], dtype=np.float64
        )

        noise: NDArray[np.float64] = self.rng.normal(
            loc=0.0, scale=self.process_noise, size=self.particles.shape
        )
        self.particles += delta + noise

    def update(self, z: NDArray[np.float64]) -> None:
        dist: NDArray[np.float64] = np.linalg.norm(self.particles - z, axis=1)
        likelihood: NDArray[np.float64] = (
            1 / (np.sqrt(2 * np.pi) * self.measurement_noise)
        ) * np.exp(-(dist**2) / (2 * self.measurement_noise**2))

        self.weights *= likelihood
        self.weights += 1.0e-300
        self.weights /= np.sum(self.weights)

    def resample(self) -> None:
        n_eff: float = 1.0 / np.sum(self.weights**2)
        if n_eff < (self.N * self.resample_threshold):
            indices: NDArray[np.int64] = self.rng.choice(
                self.N, size=self.N, p=self.weights
            )
            self.particles = self.particles[indices]
            self.weights = np.ones(self.N) / self.N
