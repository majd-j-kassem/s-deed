import logging
from typing import Any, Dict

import numpy as np

from src.environment import StochasticEnv
from src.estimator import ParticleFilter


class SimulationEngine:
    """
    Simulation engine for S-DEED.
    Updated to bridge anomalous regime detection with the Particle Filter update step.
    """

    def __init__(self, cfg: Dict[str, Any]) -> None:
        self.cfg = cfg
        self.rng = np.random.default_rng(cfg["simulation"]["random_seed"])

        self.env = StochasticEnv(
            rng=self.rng,
            env_cfg=cfg["environment"],
            sim_cfg=cfg,
        )

        self.pf = ParticleFilter(
            estimator_cfg=cfg["estimator"],
            rng=self.rng,
        )

        self.logger = logging.getLogger(__name__)

        est_cfg = self.cfg["estimator"]
        self.n_eff_threshold = est_cfg["n_eff_threshold"] * est_cfg["num_particles"]
        self.recovery_threshold = (
            est_cfg["recovery_threshold"] * est_cfg["num_particles"]
        )

        self.collapse_window = int(est_cfg["collapse_window"])
        self.recovery_error_limit = float(est_cfg["recovery_error_threshold"])

    def run(self) -> Dict[str, Any]:
        self.logger.info("Simulation started...")

        steps, distances, n_eff_history, errors, collapse_flags = [], [], [], [], []
        breakdown_time, already_broken, recovery_events = None, False, 0
        collapse_streak = 0

        max_steps = self.cfg["simulation"]["max_steps"]
        dt = self.cfg["simulation"]["dt"]

        for step in range(max_steps):
            # 1. Predict
            self.pf.predict(steering_angle=0.0, dt=dt, ego_speed=self.env.ego_speed)

            # 2. Update Environment
            noisy_ego_pos, _, _, _ = self.env.step(steering_angle=0.0)
            true_pos, obstacle_pos = self.env.get_ground_truth_states()

            # 3. Detect anomaly regime for robust estimation
            # We determine if the environment is in an anomalous regime based on \
            # Effective Sample Size (n_eff)
            # This informs the estimator to inflate noise and maintain stability
            n_eff = float(1.0 / np.sum(self.pf.weights**2))
            is_anomalous_regime = n_eff < self.n_eff_threshold

            # 4. Update Estimator with regime awareness
            self.pf.update(noisy_ego_pos, is_anomalous=is_anomalous_regime)
            self.pf.resample()

            # 5. Metrics
            ego_to_obstacle = float(np.linalg.norm(true_pos - obstacle_pos))
            estimate = np.average(self.pf.particles, weights=self.pf.weights, axis=0)
            error = float(np.linalg.norm(estimate - true_pos))

            # 6. Breakdown / Recovery Logic
            collapse_flags.append(is_anomalous_regime)
            collapse_streak = collapse_streak + 1 if is_anomalous_regime else 0

            if collapse_streak >= self.collapse_window and not already_broken:
                breakdown_time = step
                already_broken = True

            if (
                already_broken
                and n_eff > self.recovery_threshold
                and error < self.recovery_error_limit
            ):
                recovery_events += 1
                already_broken = False

            # 7. Store
            steps.append(step)
            distances.append(ego_to_obstacle)
            n_eff_history.append(n_eff)
            errors.append(error)

        # 8. Final State
        if breakdown_time is None:
            label = "stable"
        elif recovery_events > 0:
            label = "degraded"
        else:
            label = "collapsed"

        return {
            "steps": steps,
            "distances": distances,
            "n_eff": n_eff_history,
            "errors": errors,
            "collapse_flags": collapse_flags,
            "breakdown_time": breakdown_time,
            "recovery_events": recovery_events,
            "final_label": label,
        }
