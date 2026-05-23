# Research & Engineering Log: S-DEED Framework

## 1. Project Mission & Identity
**Core Focus:** Quantifying decision degradation in non-Gaussian autonomous environments.
**Academic Goal:** PhD Candidate (Focus: Risk-Aware Robotics / Probabilistic Reasoning).

---

## 2. Theoretical Audit (Refresher/Audit)
*This for book notes, paper reviews, and academic study.*

### Date: 2026-05-23 | Theme: Parametric vs. Non-Parametric Estimation
* **Concept:** Formula-Driven (Parametric) vs. Data-Driven (Non-Parametric) Modeling.
* **Summary/Refresher:** * Formula-Driven (e.g., Kalman Filter): Assumes a fixed shape (Gaussian); maps state using fixed parameters ($\mu, \Sigma$).
    * Data-Driven (e.g., Particle Filter): Non-parametric; distribution is defined empirically by the density of samples (particles).
* **Paper Gaps:** Standard parametric filters fail in high-speed, non-linear environments by "smoothing out" dangerous multi-modal risks (e.g., the "door open vs. closed" tail risk).
* **Our Contributions:** Implementing an S-DEED Particle Filter that maintains "tail risks" by preserving the non-parametric distribution. This allows us to trigger "Decision Degradation" alerts when the distribution becomes too diffuse (high variance) or inconsistent with sensor data.
* **Engineering Impact:** Must prioritize **Particle Filter** architecture in `estimator.py` over Gaussian alternatives to ensure risk sensitivity.



---

## 3. Implementation Log (The "Safety Helmet")
*Log major architectural decisions and breakthroughs here.*

### Slice 01: Estimator Specifications
* **Date:** 2026-05-23
* **Concept:** Non-parametric Particle Filter implementation.
* **Architecture:** * `__init__`: Define particle distribution and noise parameters.
    * `predict(u)`: Propagate particles through motion model $p(x_t | u_t, x_{t-1})$.
    * `update(z)`: Weight particles based on sensor likelihood $p(z_t | x_t)$.
    * `resample()`: Systematic resampling to maintain particle diversity.
* **Goal:** Create a robust estimator that reports not just the "mean," but the "tail risk" (CVaR).
* **Challenge:** Ensuring computational efficiency while maintaining enough particles to represent "tail risks."
* **Result/Refinement:** Initial skeleton design ready for `estimator.py`.

---

## 4. Hypothesis Testing
*The core of your PhD proposal and validation.*

* **Hypothesis:** "As GMM noise standard deviation increases, the CVaR-based planner will show a measurable 'Decision Degradation' inflection point at [X] intensity."
* **Status:** [Planned]

---

## 5. Next Strategic Steps
* [ ] Finalize `estimator.py` structure (Particle Filter implementation).
* [ ] Verify Particle Filter convergence with `tests/test_estimator.py`.
* [ ] Document the first "Breakdown Curve" experiment.

---

## 6. References & Literature
* [ ] Probabilistic Robotics (Thrun, Burgard, Fox) - Chapter 2: Recursive State Estimation.