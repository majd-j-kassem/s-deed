# S-DEED Repository Structure Guide

This document describes the organization of the S-DEED research framework and explains the purpose of the major directories and files.

---

# Root Directory

| Path             | Purpose                                      |
| ---------------- | -------------------------------------------- |
| README.md        | Project overview and research motivation     |
| STRUCTURE.md     | Repository structure documentation           |
| pipeline.py      | Main experiment orchestration pipeline       |
| requirements.txt | Python dependencies                          |
| pyproject.toml   | Project configuration and packaging metadata |

---

# Configuration Management

| Path               | Purpose                                      |
| ------------------ | -------------------------------------------- |
| configs/base.yaml  | Master experiment configuration              |
| configs/generated/ | Automatically generated experiment scenarios |

The generated configurations are produced through parameter sweeps and Monte Carlo scenario generation.

---

# Core Framework

| Path                | Purpose                                  |
| ------------------- | ---------------------------------------- |
| src/environment.py  | Stochastic simulation environment        |
| src/noise_model.py  | Context-dependent uncertainty generation |
| src/estimator.py    | Particle Filter implementation           |
| src/simulation.py   | Main experiment execution loop           |
| src/metrics.py      | Estimation and degradation metrics       |
| src/risk.py         | Experimental risk-analysis utilities     |
| src/planners.py     | Experimental planning modules            |
| src/batch_runner.py | Batch experiment execution support       |
| src/utils.py        | Shared utility functions                 |
| src/plots.py        | Visualization helpers                    |

---

# Experiment Infrastructure

| Path                  | Purpose                                   |
| --------------------- | ----------------------------------------- |
| experiments/runs/     | Individual experiment outputs             |
| experiments/summary/  | Aggregated Monte Carlo results            |
| experiments/logs/     | Experiment execution logs                 |
| experiments/analysis/ | Research notebooks and analysis utilities |

Each experiment run stores:

* Configuration snapshot
* Metadata
* Metrics
* Summary statistics
* Generated plots

---

# Analysis Workspace

| Path                                                   | Purpose                          |
| ------------------------------------------------------ | -------------------------------- |
| experiments/analysis/degradation_analysis.ipynb        | Degradation behavior exploration |
| experiments/analysis/uncertainty_regime_analysis.ipynb | Uncertainty regime analysis      |
| experiments/analysis/compare_runs.ipynb                | Cross-run comparisons            |
| experiments/analysis/plot_utils.py                     | Shared plotting utilities        |

---

# Automation Scripts

| Path                        | Purpose                       |
| --------------------------- | ----------------------------- |
| scripts/config_generator.py | Scenario generation           |
| scripts/build_summary.py    | Monte Carlo aggregation       |
| scripts/run_experiment.py   | Experiment execution          |
| scripts/run_experiment.sh   | Shell wrapper for experiments |
| scripts/build_paper.sh      | Paper compilation utility     |
| scripts/export_notes.sh     | Research note export utility  |

---

# Research Knowledge Base

| Path                       | Purpose                                   |
| -------------------------- | ----------------------------------------- |
| literature/papers/         | Research papers and references            |
| literature/notes/          | Reading notes and implementation insights |
| literature/RESEARCH_LOG.md | Ongoing research log                      |
| literature/README.md       | Literature organization guide             |

---

# Academic Paper Workspace

| Path                 | Purpose               |
| -------------------- | --------------------- |
| paper/main.tex       | Main manuscript       |
| paper/references.bib | Bibliography database |
| paper/sections/      | Paper sections        |
| paper/figures/       | Publication figures   |
| paper/build/         | Generated PDF outputs |

---

# Results Archive

| Path           | Purpose                           |
| -------------- | --------------------------------- |
| results/data/  | Curated datasets                  |
| results/plots/ | Final publication-quality figures |

---

# Testing

| Path                      | Purpose                |
| ------------------------- | ---------------------- |
| tests/test_environment.py | Environment validation |
| tests/test_noise_model.py | Noise model validation |
| tests/test_integration.py | End-to-end testing     |

---

# Architecture Assets

| Path          | Purpose                              |
| ------------- | ------------------------------------ |
| architecture/ | Diagrams, figures, and design assets |

---

# Current Research Focus

The current version of S-DEED focuses on:

* Non-Gaussian uncertainty modeling
* Particle Filter behavior characterization
* Estimation degradation analysis
* Effective Sample Size (N_eff) dynamics
* Breakdown and recovery detection
* Monte Carlo robustness evaluation

Future extensions may introduce:

* Risk-aware planning
* Decision degradation analysis
* CVaR-based policy evaluation
* Autonomous system resilience assessment
