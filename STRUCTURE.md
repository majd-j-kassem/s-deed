# S-DEED Repository Structure Guide

This document explains the purpose and role of every major directory and file in the S-DEED research framework.

## Root Structure Overview

| Path | Type | Purpose |
| :--- | :--- | :--- |
| `README.md` | File | Main project overview, architecture summary, setup instructions, and research motivation. |
| `.gitignore` | File | Prevents unnecessary files (logs, PDFs, caches, build artifacts) from being tracked by Git. |
| `requirements.txt` | File | Python dependency versions for reproducible experiments. |
| `config.yaml` | File | Centralized simulation and experiment configuration parameters. |
| `create_paper.sh` | Script | Utility script for quickly generating LaTeX paper templates and folders. |

## Literature & Research Knowledge

| Path | Type | Purpose |
| :--- | :--- | :--- |
| `literature/` | Directory | Central research knowledge repository used during study and implementation. |
| `literature/notes/` | Directory | Markdown summaries, annotations, and implementation insights extracted from papers. |
| `literature/surveys/` | Directory | Comparative reviews and thematic summaries across multiple papers. |
| `literature/README.md` | File | Maps research papers to project modules and explains reading priorities. |
| `literature/research_log/` | Directory | Daily research notes, experiment reflections, debugging insights, and idea evolution logs. |

## Academic Paper Workspace

| Path | Type | Purpose |
| :--- | :--- | :--- |
| `paper/` | Directory | Main academic writing workspace for the publication/manuscript. |
| `paper/main.tex` | File | Primary LaTeX entry point for the paper. |
| `paper/references.bib` | File | Bibliography database automatically synchronized with Zotero. |
| `paper/sections/` | Directory | Modular LaTeX sections (Introduction, Methodology, Results, etc.). |
| `paper/figures/` | Directory | Final figures and plots used inside the paper. |
| `paper/build/` | Directory | Temporary LaTeX compilation artifacts and generated PDFs. |

## Source Code (Core Framework)

| Path | Type | Purpose |
| :--- | :--- | :--- |
| `src/` | Directory | Main implementation of the S-DEED framework. |
| `src/environment.py` | File | Defines the stochastic 2-agent simulation environment. |
| `src/noise_model.py` | File | Implements context-dependent GMM uncertainty injection. |
| `src/estimator.py` | File | Particle Filter implementation for non-Gaussian state estimation. |
| `src/risk.py` | File | Computes CVaR and probabilistic safety metrics. |
| `src/planners.py` | File | Decision-making policies (deterministic and risk-aware planners). |
| `src/metrics.py` | File | Computes evaluation metrics and breakdown statistics. |
| `src/simulation.py` | File | Main integration loop connecting all framework components. |
| `src/utils/` | Directory | Shared helper functions, reproducibility utilities, math helpers, and config loaders. |

## Testing Infrastructure

| Path | Type | Purpose |
| :--- | :--- | :--- |
| `tests/` | Directory | Unit and integration testing framework. |
| `tests/test_estimator.py` | File | Verifies Particle Filter correctness and stability. |
| `tests/test_risk.py` | File | Validates CVaR and risk metric computations. |
| `tests/test_planners.py` | File | Tests planner decision logic under multiple risk conditions. |
| `tests/conftest.py` | File | Shared fixtures and reusable test configurations. |

## Experiment Management

| Path | Type | Purpose |
| :--- | :--- | :--- |
| `experiments/` | Directory | Stores experiment configurations, outputs, and reproducibility artifacts. |
| `experiments/configs/` | Directory | Individual YAML experiment configurations. |
| `experiments/runs/` | Directory | Full outputs of each executed experiment run. |
| `experiments/logs/` | Directory | Numerical logs and simulation outputs. |
| `experiments/plots/` | Directory | Generated plots such as Decision Breakdown Curves. |

## Automation Scripts

| Path | Type | Purpose |
| :--- | :--- | :--- |
| `scripts/` | Directory | Automation utilities for experiments and paper workflows. |
| `scripts/run_experiment.sh` | Script | Executes standardized experiment pipelines. |
| `scripts/build_paper.sh` | Script | Compiles the LaTeX manuscript automatically. |
| `scripts/export_notes.sh` | Script | Exports Zotero annotations and notes into Markdown summaries. |

## Final Outputs

| Path | Type | Purpose |
| :--- | :--- | :--- |
| `results/` | Directory | Curated final outputs used for publication and reporting. |

---

## Research Philosophy of the Repository

S-DEED is designed as a reproducible research-engineering framework focused on:

* Probabilistic state estimation under non-Gaussian uncertainty
* Risk-aware autonomous decision-making
* Decision degradation characterization
* Failure regime analysis
* Reliability evaluation of uncertainty-aware systems

The repository structure intentionally separates:

1.  Research literature and knowledge extraction
2.  Academic writing and publication assets
3.  Core source code and algorithms
4.  Experiment tracking and reproducibility
5.  Testing and validation infrastructure

This separation ensures scalability, maintainability, and publication-grade reproducibility.