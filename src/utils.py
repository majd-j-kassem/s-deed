import os
import random
from pathlib import Path
from typing import Any, Dict

import matplotlib
import numpy as np
import yaml


def load_config(config_path: str = "base.yaml") -> Dict[str, Any]:
    """
    Loads configuration from a YAML file.
    Uses Pathlib for cross-platform compatibility and absolute path resolution.
    """
    path = Path(config_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {path}")

    with open(path, "r") as f:
        return yaml.safe_load(f)


def enforce_reproducibility(seed: int) -> np.random.Generator:
    """
    Ensures experiment reproducibility by seeding global libraries.
    Configures plotting backend for non-interactive environments (e.g., servers).
    """
    # Set seeds for built-in libraries
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)

    # Configure numpy
    np.random.seed(seed)
    rng = np.random.default_rng(seed)

    # Configure plotting backend to Agg (prevents UI/Display errors on servers)
    matplotlib.use("Agg")

    return rng
