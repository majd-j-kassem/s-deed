# S-DEED: A Framework for Characterizing Decision Degradation under Non-Gaussian Uncertainty

A minimal, reproducible research framework for analyzing failure regimes of risk-aware decision-making under non-Gaussian uncertainty. The system focuses on identifying decision breakdown thresholds rather than optimizing tracking performance.

---

## 🧭 System Overview

The framework consists of a four-stage probabilistic pipeline:


Environment (2-agent scenario)
↓
Context-dependent GMM (uncertainty model)
↓
Particle Filter (state estimation)
↓
CVaR-based risk-aware planner
↓
Evaluation module (breakdown analysis)


---

## ⚙️ Repository Structure

### Core Implementation (feature branches)

- `feat/environment`  
  2-agent kinematic simulation environment

- `feat/noise-model`  
  Context-dependent Gaussian Mixture Model (GMM)

- `feat/state-estimation`  
  Particle Filter for non-Gaussian belief tracking

- `feat/risk-planner`  
  CVaR-based risk-aware decision module

- `feat/evaluation`  
  Metrics computation and Decision Breakdown Curve generation

---

### Experimental Branches

- `exp/noise-ablation`  
  Sensitivity to uncertainty intensity

- `exp/risk-comparison`  
  Deterministic vs CVaR-based policy evaluation

- `exp/multi-agent`  
  Extended interaction scenarios

- `exp/sensitivity-analysis`  
  Parameter robustness analysis

---

## 🎯 Primary Research Objective

To characterize the uncertainty levels at which risk-aware decision-making policies fail, and to quantify decision breakdown thresholds under non-Gaussian noise conditions.

---

## 📊 Key Output

- Decision Breakdown Curves
- Safety violation probability vs uncertainty level
- Failure threshold estimation
- Risk-aware vs deterministic comparison

---

## 📌 Core Metric

The primary metric is the uncertainty level at which safety violation probability exhibits a sharp increase (decision breakdown threshold).

---

## 🧪 Reproducibility

All experiments are designed to be:
- Fully deterministic via fixed seeds
- Isolated per experimental branch
- Reproducible using standard Python stack (NumPy, SciPy, Matplotlib)

requirements.txt
config.yaml
fixed random seeds

---

## 🧠 Research Positioning

This framework studies decision degradation under uncertainty, focusing on failure regimes of risk-aware planning rather than trajectory optimization or tracking accuracy.

## Communication: Add Mattermost Wehook