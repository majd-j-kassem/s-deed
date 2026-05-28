from typing import Any, Dict

import numpy as np


class ContextDependentGMM:
    def __init__(self, rng: np.random.Generator, env_cfg: Dict[str, Any]) -> None:
        self.rng: np.random.Generator = rng
        # Component parameters (Nominal vs Anomalous)
        self.mu_nominal = np.array([0.0, 0.0])
        self.sigma_nominal = 0.02
        self.mu_anomalous = np.array([0.1, -0.1])
        self.sigma_anomalous = 0.3
        # Aligning perfectly with your environment configuration pattern
        self.critical_distance: float = float(env_cfg.get("critical_distance", 3.0))

    def sample_noise(self, dist_to_obstacle: float) -> np.ndarray:
        """Samples 2D non-Gaussian noise based on the proximity context."""
        # 1. Context Dependency: If close to the obstacle, anomaly probability spikes
        if dist_to_obstacle < self.critical_distance:
            p_anomalous = 0.7  # 70% chance of severe non-Gaussian noise
        else:
            p_anomalous = 0.05  # 5% baseline glitch chance

        # 2. Categorical Selection (Decide which distribution component to use)
        use_anomalous = self.rng.random() < p_anomalous

        # 3. Generate the actual structural sample
        if use_anomalous:
            noise = self.rng.normal(
                loc=self.mu_anomalous, scale=self.sigma_anomalous, size=2
            )
        else:
            noise = self.rng.normal(
                loc=self.mu_nominal, scale=self.sigma_nominal, size=2
            )

        return noise
