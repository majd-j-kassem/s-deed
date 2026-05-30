import csv
import json
import logging
import traceback
from datetime import datetime
from pathlib import Path

import yaml

from experiments.analysis.plot_utils import SDEEDPlotter
from src.simulation import SimulationEngine
from src.utils import enforce_reproducibility, load_config


class ExperimentRunner:
    """Handles the lifecycle of a single experiment run."""

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.cfg = load_config(config_path)
        self.run_id = self._generate_run_id()
        self.run_dir = Path("experiments/runs") / self.run_id
        self.paths = {
            "root": self.run_dir,
            "plots": self.run_dir / "plots",
            "artifacts": self.run_dir / "artifacts",
        }

    def _generate_run_id(self):
        """Generates a unique identifier based on timestamp, seed, and scenario name."""
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        seed = self.cfg["simulation"]["random_seed"]
        scenario = Path(self.config_path).stem
        return f"{ts}_seed{seed}_{scenario}"

    def run(self):
        """Executes the simulation, saves artifacts, and generates plots."""
        self._setup_dirs()
        enforce_reproducibility(self.cfg["simulation"]["random_seed"])
        self._save_config()

        engine = SimulationEngine(self.cfg)
        try:
            results = engine.run()
            self._save_results(results)
            self._save_summary(results)
            SDEEDPlotter(self.paths["plots"]).plot_all(results)
        except Exception:
            logging.error(f"Experiment {self.run_id} failed: {traceback.format_exc()}")
        return self.run_dir

    def _setup_dirs(self):
        """Creates the required directory structure for experiment artifacts."""
        for p in self.paths.values():
            p.mkdir(parents=True, exist_ok=True)

    def _save_config(self):
        """Saves a copy of the configuration YAML for audit purposes."""
        with open(self.run_dir / "config.yaml", "w") as f:
            yaml.dump(dict(self.cfg), f)

    def _save_results(self, results):
        """Saves step-by-step metrics to a CSV file."""
        with open(self.run_dir / "metrics.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["step", "dist", "n_eff", "error"])
            for i in range(len(results.get("steps", []))):
                writer.writerow(
                    [
                        results["steps"][i],
                        results["distances"][i],
                        results["n_eff"][i],
                        results["errors"][i],
                    ]
                )

    def _save_summary(self):
        """Saves final summary metrics as a JSON file."""
        summary = {
            "run_id": self.run_id,
            "params": {
                "sigma": self.cfg["noise_model"]["sigma_anomalous"]["base"],
                "prob": self.cfg["noise_model"]["anomaly_probability"]["base_rate"],
            },
        }
        with open(self.run_dir / "summary.json", "w") as f:
            json.dump(summary, f, indent=4)


class BatchRunner:
    """Orchestrates multiple experiment runs sequentially with progress tracking."""

    def __init__(self, config_list):
        self.config_list = config_list

    def run_all(self):
        """Iterates through all configurations and executes experiments."""
        total = len(self.config_list)
        logging.info(f"Starting batch of {total} experiments")

        for i, config_path in enumerate(self.config_list, 1):
            percentage = (i / total) * 100
            print(f"[{i}/{total}] ({percentage:.1f}%) Running: {config_path.name}")

            try:
                ExperimentRunner(config_path).run()
            except Exception as e:
                logging.error(f"Failed to execute batch item {config_path.name}: {e}")

        logging.info("Batch execution completed.")
