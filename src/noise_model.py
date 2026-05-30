from typing import Any, Dict

import numpy as np


class ContextDependentGMM:
    """
    Stochastic noise generator based on Gaussian Mixture Model (GMM).
    Switches between nominal and anomalous regimes based on environmental context.
    All parameters are strictly loaded from the provided configuration dictionary.
    """

    def __init__(self, rng: np.random.Generator, noise_cfg: Dict[str, Any]) -> None:
        self.rng = rng

        # Nominal noise parameters
        self.mu_nominal = np.array(noise_cfg["mu_nominal"], dtype=float)
        self.sigma_nominal_base = float(noise_cfg["sigma_nominal"]["base"])
        self.sigma_nominal_jitter = float(noise_cfg["sigma_nominal"]["jitter"])

        # Anomalous noise parameters
        mu_anom = noise_cfg["mu_anomalous"]
        self.mu_anomalous_base = np.array(mu_anom["base"], dtype=float)
        self.mu_anomalous_var = float(mu_anom["variability"])

        sigma_anom = noise_cfg["sigma_anomalous"]
        self.sigma_anomalous_base = float(sigma_anom["base"])
        self.sigma_anomalous_jitter = float(sigma_anom["jitter"])

        # Context switching parameters
        cd_cfg = noise_cfg["critical_distance"]
        self.base_cd = float(cd_cfg["base"])
        self.adaptive = bool(cd_cfg["adaptive"])
        self.adaptation_std = float(cd_cfg["adaptation_std"])

        # Probability model parameters
        prob_cfg = noise_cfg["anomaly_probability"]
        self.base_rate = float(prob_cfg["base_rate"])
        self.dist_mult = float(prob_cfg["distance_multiplier"])
        self.max_prob = float(prob_cfg["max_anomaly_prob"])

    def _effective_sigma(self, base: float, jitter: float) -> float:
        """Returns sampled sigma incorporating jitter."""
        return base + self.rng.normal(0.0, jitter)

    def _effective_mu_anomalous(self) -> np.ndarray:
        """Returns anomalous mean incorporating variability."""
        return self.mu_anomalous_base + self.rng.normal(
            0.0, self.mu_anomalous_var, size=2
        )

    def _effective_critical_distance(self) -> float:
        """Returns critical distance with optional adaptive variability."""
        if not self.adaptive:
            return self.base_cd
        return self.base_cd + self.rng.normal(0.0, self.adaptation_std)

    def sample_noise(self, dist_to_obstacle: float) -> np.ndarray:
        """
        Samples noise based on distance to obstacle.
        Higher probability of anomalous noise when within critical distance.
        """
        cd = self._effective_critical_distance()

        # Determine anomaly probability based on distance
        # Enforce max_prob when within critical distance to stress-test the estimator
        if dist_to_obstacle < cd:
            p_anomalous = self.max_prob
        else:
            p_anomalous = self.base_rate

        # Sample regime choice
        use_anomalous = self.rng.random() < p_anomalous

        # Debugging output to track noise injection behavior
        # print(f"DEBUG: Dist={dist_to_obstacle:.2f} | Anomalous={use_anomalous} | \
        # Prob={p_anomalous:.2f}")

        # Retrieve effective noise parameters
        sigma_nom = self._effective_sigma(
            self.sigma_nominal_base, self.sigma_nominal_jitter
        )
        sigma_anom = self._effective_sigma(
            self.sigma_anomalous_base, self.sigma_anomalous_jitter
        )

        if use_anomalous:
            # Apply anomalous noise regime
            return self.rng.normal(
                loc=self._effective_mu_anomalous(), scale=sigma_anom, size=2
            )

        # Apply nominal noise regime
        return self.rng.normal(loc=self.mu_nominal, scale=sigma_nom, size=2)
