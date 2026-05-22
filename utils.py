import os
import random

import matplotlib
import numpy as np
import yaml


def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def enforce_reproducibility(seed: int):
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)

    rng = np.random.default_rng(seed)
    matplotlib.use("Agg")

    return rng
