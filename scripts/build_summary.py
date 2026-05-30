import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import yaml


def load_main_config():
    """Loads the master configuration file and ensures simulation seeds are present."""
    script_dir = Path(__file__).resolve().parent
    root_dir = script_dir.parent
    config_path = root_dir / "configs" / "base.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)

    if "seeds" not in cfg.get("simulation", {}):
        raise KeyError("simulation.seeds list is missing in base.yaml")

    return cfg, root_dir


# Initialize Configuration
CONFIG, ROOT_DIR = load_main_config()
ANALYSIS_CONFIG = CONFIG.get("analysis", {})
OUTPUT_DIRS = CONFIG.get("output_directories", {})
SEEDS = CONFIG["simulation"]["seeds"]

RUNS_DIR = (ROOT_DIR / OUTPUT_DIRS.get("runs_root", "experiments/runs")).resolve()
SUMMARY_DIR = (
    ROOT_DIR / OUTPUT_DIRS.get("summary_root", "experiments/summary")
).resolve()
SUMMARY_DIR.mkdir(parents=True, exist_ok=True)


def extract_params(run_id):
    """
    Extracts sigma, probability, and seed parameters from directory names.
    Uses flexible regex to handle timestamps and multiple seed markers.
    """
    # Look for sigma followed by digits
    match_sigma = re.search(r"sigma([0-9.]+)", run_id)
    # Look for _p followed by digits
    match_p = re.search(r"_p([0-9.]+)", run_id)

    # Improved regex: search for _s followed by digits,
    # allowing for optional characters after it to handle potential name variations
    match_seed = re.search(r"_s([0-9]+)(?:$|_)", run_id)

    sigma = float(match_sigma.group(1)) if match_sigma else None
    prob = float(match_p.group(1)) if match_p else None
    seed = int(match_seed.group(1)) if match_seed else None

    return sigma, prob, seed


def bootstrap_ci(data, n_boot, ci):
    if len(data) < 2:
        return 0.0
    boot_means = [
        np.mean(np.random.choice(data, size=len(data), replace=True))
        for _ in range(n_boot)
    ]
    lower = (1 - ci) / 2
    upper = 1 - lower
    return (
        np.percentile(boot_means, upper * 100) - np.percentile(boot_means, lower * 100)
    ) / 2


def calculate_ci(data):
    method = ANALYSIS_CONFIG.get("ci_method", "gaussian")
    if method == "bootstrap":
        return bootstrap_ci(
            data,
            ANALYSIS_CONFIG["bootstrap_iterations"],
            ANALYSIS_CONFIG["confidence_level"],
        )
    else:
        std = np.std(data) if len(data) > 1 else 0.0
        return 1.96 * std / np.sqrt(len(data)) if len(data) > 0 else 0.0


def get_severity_and_stability(label, cfg_data):
    eval_cfg = cfg_data.get("evaluation", {})
    mapping = eval_cfg.get(
        "severity_mapping", {"stable": 0.0, "degraded": 0.5, "collapsed": 1.0}
    )
    threshold = eval_cfg.get("stability_threshold", 0.0)
    severity = mapping.get(label, 0.0)
    return severity, (1 if severity <= threshold else 0)


# --- Data Loading ---
rows = []
for run in RUNS_DIR.iterdir():
    if not run.is_dir():
        continue

    sigma, prob, seed = extract_params(run.name)

    if seed is None or seed not in SEEDS:
        continue

    metrics_file = run / "metrics.csv"
    summary_file = run / "summary.json"
    config_file = run / "config.yaml"

    # DEBUG: See what is missing
    if not metrics_file.exists():
        print(f"DEBUG: Missing metrics.csv in {run.name}")
        continue
    if not summary_file.exists():
        print(f"DEBUG: Missing summary.json in {run.name}")
        continue
    with open(config_file, "r") as f:
        cfg_data = yaml.safe_load(f)
    df_metrics = pd.read_csv(metrics_file)
    with open(summary_file) as f:
        summary_data = json.load(f)

    sigma, prob, seed = extract_params(run.name)

    if seed not in SEEDS:
        continue

    label = summary_data.get("metrics", {}).get("final_label", "stable")
    severity, is_stable = get_severity_and_stability(label, cfg_data)

    rows.append(
        {
            "sigma": sigma,
            "prob": prob,
            "seed": seed,
            "final_error": df_metrics["error"].iloc[-1],
            "final_n_eff": df_metrics["n_eff"].iloc[-1],
            "severity_index": severity,
            "is_stable": is_stable,
        }
    )

if not rows:
    raise ValueError("No valid runs found matching the seeds in base.yaml")

# --- Aggregation and Statistical Analysis ---
df_all = pd.DataFrame(rows).dropna(subset=["sigma", "prob"])
grouped = df_all.groupby(["sigma", "prob"])

agg = grouped.agg(
    mean_final_error=("final_error", "mean"),
    mean_severity=("severity_index", "mean"),
    stability_prob=("is_stable", "mean"),
    mean_n_eff=("final_n_eff", "mean"),
    count=("final_error", "count"),
).reset_index()

agg["ci_final_error"] = grouped["final_error"].apply(calculate_ci).values
agg.to_csv(SUMMARY_DIR / "monte_carlo_summary.csv", index=False)


# --- Visualization ---
def save_heatmap(data, title, filename, cmap="viridis"):
    plt.figure(figsize=(10, 7))
    sns.heatmap(data, annot=True, fmt=".2f", cmap=cmap)
    plt.title(title)
    plt.savefig(SUMMARY_DIR / filename, dpi=300)
    plt.close()


save_heatmap(
    agg.pivot_table(index="sigma", columns="prob", values="mean_severity"),
    "System Severity Heatmap",
    "severity_heatmap.png",
    "Reds",
)
save_heatmap(
    agg.pivot_table(index="sigma", columns="prob", values="stability_prob"),
    "Stability Probability Heatmap",
    "stability_heatmap.png",
    "Greens",
)

print(f"Analysis complete. Stats saved to {SUMMARY_DIR}")
