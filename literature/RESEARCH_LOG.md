# Research & Engineering Log: S-DEED Framework

## 1. Project Mission & Identity
**Core Focus:** Quantifying decision degradation in non-Gaussian autonomous environments.
**Academic Goal:** PhD Candidate (Focus: Risk-Aware Robotics / Probabilistic Reasoning).

---

## 2. Theoretical Audit (Engineering Reflection)
*Use this section for every paper you read (based on the `literature/` folder).*

### Audit: [Paper Title]
* **Date:** [YYYY-MM-DD]
* **Methodology Alignment:** Does the author's noise model assume Gaussian (unimodal) or non-Gaussian (multimodal) behavior?
* **Failure Definition:** How do they define "Safety Violation"?
* **The "Engineering Gap":** My implementation is superior/different because...

---

## 3. Implementation Log (The "Safety Helmet")
*Log every major architectural decision here. This proves you have a systematic process.*

### Slice 1: Particle Filter Implementation
* **Date:** [YYYY-MM-DD]
* **Decision:** Choosing `N=[X]` particles. Why? (Trade-off between real-time performance vs. uncertainty representation).
* **Challenge:** How to handle "particle deprivation" (the collapse of the filter).
* **Result/Refinement:** [Briefly note if the test passed or if the math needed adjustment].

---

## 4. Hypothesis Testing
*This is the most critical section for your PhD proposal.*

* **Hypothesis:** "As GMM noise standard deviation increases, the CVaR-based planner will show a measurable 'Decision Degradation' inflection point at [X] intensity."
* **Status:** [Planned / Testing / Validated]

---

## 5. Next Strategic Steps
* [ ] Finalize `estimator.py` structure.
* [ ] Verify Particle Filter convergence with `tests/test_estimator.py`.
* [ ] Document the first "Breakdown Curve" experiment.