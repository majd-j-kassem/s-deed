# S-DEED
## Stochastic Degradation and Estimation Error Dynamics

S-DEED is a reproducible experimental framework for studying the impact of non-Gaussian uncertainty on probabilistic state estimation.

The project investigates how estimation performance degrades under stochastic anomalies, context-dependent noise, and uncertainty regime shifts. The current focus is on understanding degradation dynamics and failure indicators before introducing downstream decision-making components.

---

# Motivation

Real-world autonomous systems operate under uncertainty that is often non-Gaussian, non-stationary, and context dependent.

Traditional evaluation methods frequently assume idealized noise conditions and focus primarily on average estimation accuracy.

S-DEED aims to provide a controlled experimental environment for analyzing:

- Estimation degradation under uncertainty
- Particle Filter behavior under anomalous observations
- Effective sample size (N_eff) dynamics
- Failure and recovery patterns
- Statistical robustness across Monte Carlo trials

---

# Current System Architecture

The current framework consists of four major components:

1. **Stochastic Environment**
   - Simple agent-based simulation
   - Reproducible trajectories
   - Controlled uncertainty injection

2. **Context-Dependent Noise Model**
   - Gaussian Mixture based uncertainty generation
   - Configurable anomaly probabilities
   - Regime-shift and burst anomaly support

3. **Particle Filter Estimator**
   - Sequential Bayesian state estimation
   - Resampling based on effective sample size
   - Tracking of estimator health indicators

4. **Degradation Analysis Module**
   - Error statistics
   - N_eff monitoring
   - Breakdown and recovery analysis
   - Monte Carlo aggregation

---

# Repository Structure

```text
S-DEED/
│
├── configs/
│   ├── base.yaml
│   └── generated/
│
├── src/
│   ├── environment/
│   ├── estimator/
│   ├── noise/
│   └── simulation/
│
├── scripts/
│   ├── config_generator.py
│   └── build_summary.py
│
├── experiments/
│   ├── runs/
│   └── summary/
│
├── run_experiment.py
├── pipeline.py
└── requirements.txt
```

---

# Installation

```bash
git clone <repository-url>
cd s-deed

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

# Experiment Pipeline

## 1. Clear previous outputs

```bash
python pipeline.py clear
```

## 2. Generate experiment configurations

```bash
python pipeline.py generate
```

## 3. Run all experiments

```bash
python pipeline.py run
```

## 4. Run a single experiment

```bash
python pipeline.py run --config configs/generated/example.yaml
```

## 5. Aggregate results

```bash
python pipeline.py collect
```

---

# Output Artifacts

Each experiment produces a self-contained run directory:

```text
experiments/runs/
└── <run_id>/
    ├── config.yaml
    ├── metadata.json
    ├── metrics.csv
    ├── summary.json
    └── plots/
```

Key metrics include:

- Final estimation error
- Average estimation error
- Effective sample size (N_eff)
- Breakdown indicators
- Recovery events

---

# Monte Carlo Evaluation

S-DEED supports Monte Carlo experimentation through multiple random seeds.

Aggregated statistics include:

- Mean performance
- Standard deviation
- Confidence intervals
- Stability probability
- Degradation severity metrics

---

# Research Direction

The current version focuses on:

- Non-Gaussian uncertainty modeling
- Particle Filter degradation analysis
- Statistical characterization of estimation failures

Future extensions may include:

- Risk-aware planning
- Decision degradation analysis
- CVaR-based decision policies
- Autonomous system resilience evaluation

---

# Reproducibility

All experiments are configuration-driven and support deterministic execution through fixed random seeds.

Generated configurations, experiment outputs, and aggregated summaries are stored independently to facilitate reproducible research workflows.

---

# Disclaimer

This repository contains ongoing research code and experimental infrastructure.

Interfaces, metrics, and evaluation procedures may evolve as the project develops.