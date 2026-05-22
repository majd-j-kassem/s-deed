# Research Foundations for S-DEED

## Mission Statement
**Mission:** To study how non-Gaussian uncertainty propagates through probabilistic state estimation and affects risk-aware autonomous decision-making, specifically to quantify decision degradation inflection points in autonomous systems.

---

## Core Research Themes
These themes define the theoretical pillars of the S-DEED framework:

- **Non-Gaussian Uncertainty Propagation:** Analyzing how multi-modal noise evolves in dynamic environments.
- **Bayesian State Estimation:** Leveraging particle-based methods for robust tracking.
- **Risk-Aware Autonomous Decision-Making:** Integrating safety constraints directly into the planning loop.
- **CVaR-based Safety Evaluation:** Utilizing Conditional Value-at-Risk to model tail-risk and rare failure events.
- **Decision Degradation Analysis:** Identifying the quantitative inflection points where system performance fails under uncertainty.
- **Probabilistic Safety Verification:** Developing rigorous bounds for autonomous agent behavior in stochastic environments.

---

## Literature Mapping Table

| Module | Research Goal | Proposed Paper / Reference | Relevance to S-DEED |
| :--- | :--- | :--- | :--- |
| `estimator.py` | Bayesian State Estimation under non-Gaussian uncertainty | *Probabilistic Robotics* | Foundation for understanding Particle Filters and belief propagation. |
| `estimator.py` | Non-Gaussian uncertainty propagation | *Sequential Monte Carlo Methods in Practice* | Mathematical/methodological basis for Particle Filtering. |
| `risk.py` | Tail-risk quantification | *Conditional Value-at-Risk for General Loss Distributions* | The seminal paper establishing CVaR. |
| `risk.py` | Risk-aware safety modeling | *Safe Navigation in Uncertain Crowded Environments Using Risk Adaptive CVaR Barrier Functions* | Modern implementation of CVaR in autonomous navigation. |
| `risk.py` | Coherent risk verification | *Sample-based Bounds for Coherent Risk Measures* | Essential for understanding verification and probabilistic safety. |
| `planners.py` | Planning under uncertainty | *Chance Constrained Motion Planning for High-Dimensional Robots* | Core reference for chance-constrained planning. |
| `planners.py` | Risk-aware motion planning | *Risk-Aware Motion Planning under Uncertainty* | Explains the link between uncertainty and navigation decisions. |
| `planners.py` | Modern uncertainty-aware autonomy | *Uncertainty-Aware Decision-Making and Planning for Autonomous Forced Merging* | Highly relevant to your tactical decision-making goal. |
| `planners.py` | Prediction uncertainty handling | *Hierarchical Prediction Uncertainty-Aware Motion Planning for Autonomous Driving* | Insight into modern uncertainty-aware planning. |
| `metrics.py` | Safety evaluation & robustness | *A Survey of Metrics for Autonomous Driving Safety* | Benchmark for building your evaluation methodology. |
| `metrics.py` | Decision reliability under uncertainty | *Conformal Decision Theory: Safe Autonomous Decisions from Imperfect Predictions* | Directly links to your "Decision Degradation" framework. |
| `simulation.py` | Probabilistic decision systems | *Decision Making Under Uncertainty* | Comprehensive view of probabilistic architecture. |
| `simulation.py` | Perception uncertainty → decision failure | *Safe Tactical Decision-Making for Autonomous Vehicles Considering Uncertainties in Deep Learning-Based Visual Perception* | Vital for your research identity and failure analysis. |

---
*Maintained as part of the S-DEED Research-Software Engineering workflow.*