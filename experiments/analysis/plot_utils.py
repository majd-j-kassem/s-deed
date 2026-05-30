from pathlib import Path

import matplotlib.pyplot as plt


class SDEEDPlotter:
    """
    Minimal research-grade plotting utilities for S-DEED.
    Focus: readability + reproducibility + paper-ready plots.
    """

    def __init__(self, save_dir: str):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def plot_error_curve(self, steps, errors):
        plt.figure()
        plt.plot(steps, errors)
        plt.title("Estimation Error over Time")
        plt.xlabel("Step")
        plt.ylabel("Error")

        path = self.save_dir / "error_curve.png"
        plt.savefig(path)
        plt.close()

        return path

    def plot_n_eff(self, steps, n_eff):
        plt.figure()
        plt.plot(steps, n_eff)
        plt.title("Particle Filter Effective Sample Size (N_eff)")
        plt.xlabel("Step")
        plt.ylabel("N_eff")

        path = self.save_dir / "n_eff.png"
        plt.savefig(path)
        plt.close()

        return path

    def plot_distance(self, steps, distances):
        plt.figure()
        plt.plot(steps, distances)
        plt.title("Obstacle Distance over Time")
        plt.xlabel("Step")
        plt.ylabel("Distance")

        path = self.save_dir / "distance.png"
        plt.savefig(path)
        plt.close()

        return path

    def plot_all(self, results: dict):
        """
        Convenience function: generate all standard S-DEED plots.
        """

        steps = results["steps"]

        paths = {
            "error_curve": self.plot_error_curve(steps, results["errors"]),
            "n_eff": self.plot_n_eff(steps, results["n_eff"]),
            "distance": self.plot_distance(steps, results["distances"]),
        }

        return paths
