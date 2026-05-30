import copy
from pathlib import Path

import numpy as np
import yaml


def load_base_config():
    script_dir = Path(__file__).resolve().parent
    root_dir = script_dir.parent
    config_path = root_dir / "configs" / "base.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Base config not found at {config_path}")

    with open(config_path, "r") as f:
        return yaml.safe_load(f), root_dir


# Initialize
BASE_CFG, ROOT_DIR = load_base_config()
OUTPUT_DIR = ROOT_DIR / "configs" / "generated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Strict check for required sections
required_sections = ["simulation", "noise_model", "grid_search", "failure_model"]
for section in required_sections:
    if section not in BASE_CFG:
        raise KeyError(f"Missing required section: {section} in base.yaml")

# Read parameters directly from base.yaml (No hardcoded fallback values)
grid_cfg = BASE_CFG["grid_search"]
sigma_cfg = grid_cfg["sigma_range"]
prob_cfg = grid_cfg["prob_range"]

SIGMA_VALUES = np.linspace(sigma_cfg[0], sigma_cfg[1], int(sigma_cfg[2]))
PROB_VALUES = np.linspace(prob_cfg[0], prob_cfg[1], int(prob_cfg[2]))

seeds_list = BASE_CFG["simulation"]["seeds"]
if not seeds_list:
    raise ValueError("Simulation seeds list cannot be empty.")

# Pre-calculate and print total expected scenarios
total_scenarios = len(SIGMA_VALUES) * len(PROB_VALUES) * len(seeds_list)
print(f"Total scenarios to generate: {total_scenarios}")

count = 0
for sigma in SIGMA_VALUES:
    for p in PROB_VALUES:
        if not (0.0 <= p <= 1.0):
            raise ValueError(f"Probability p={p} is out of bounds [0, 1]")

        for seed in seeds_list:
            cfg = copy.deepcopy(BASE_CFG)

            try:
                cfg["simulation"]["random_seed"] = int(seed)
                cfg["noise_model"]["sigma_anomalous"]["base"] = float(sigma)
                cfg["noise_model"]["anomaly_probability"]["base_rate"] = float(p)
            except Exception as e:
                raise ValueError("Failed to generate configuration") from e

            filename = OUTPUT_DIR / f"sigma{sigma:.2f}_p{p:.2f}_s{seed}.yaml"
            with open(filename, "w") as f:
                yaml.dump(cfg, f)

            count += 1

print(f"Successfully generated {count} scenarios in {OUTPUT_DIR}")
