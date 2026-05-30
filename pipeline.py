import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# Define project root and directories for centralized management
PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_DIR = PROJECT_ROOT / "configs" / "generated"
RUNS_DIR = PROJECT_ROOT / "experiments" / "runs"
SUMMARY_DIR = PROJECT_ROOT / "experiments" / "summary"


def run_script(script_name: str, args: list = None):
    """Executes a Python script from the scripts directory and handles errors."""
    script_path = PROJECT_ROOT / "scripts" / script_name
    cmd = [sys.executable, str(script_path)] + (args if args else [])
    try:
        # Run the subprocess and wait for completion
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing {script_name}: {e}")
        sys.exit(1)


def config_generator():
    """Triggers the configuration generation process."""
    print("📦 Generating configurations...")
    # Updated to reflect the agreed-upon filename
    run_script("config_generator.py")
    print("✅ Configuration generation completed.")


def run_experiments(config_file: str = None):
    """Executes the experiment runner for either single or batch configurations."""
    print("🚀 Running experiments...")

    # Configure arguments based on whether a specific config file or a directory is used
    if config_file:
        args = ["--config", config_file]
    else:
        # Automatically inject --all flag when running a batch directory
        args = ["--all", "--config_dir", str(CONFIG_DIR)]

    run_script("run_experiment.py", args)
    print("✅ Experiments completed.")


def collect_data():
    """Triggers the data aggregation and summary analysis script."""
    print("📊 Collecting experiment results...")
    run_script("build_summary.py")
    print("✅ Data collection completed.")


def clear_all():
    """Clears all generated data to ensure a fresh experiment environment."""
    print("🧹 Clearing generated configurations, runs, and summaries...")

    target_dirs = [CONFIG_DIR, RUNS_DIR, SUMMARY_DIR]

    for path in target_dirs:
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
            print(f"Deleted: {path}")

    # Recreate the directory structure
    for path in target_dirs:
        path.mkdir(parents=True, exist_ok=True)

    print("✅ Clean-up completed.")


def main():
    """Main orchestrator for the S-DEED pipeline."""
    parser = argparse.ArgumentParser(
        description="S-DEED Experiment Pipeline Orchestrator"
    )
    parser.add_argument(
        "command",
        choices=["generate", "run", "collect", "clear"],
        help="The pipeline command to execute",
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Run a single specific configuration file",
    )

    args = parser.parse_args()

    # Route execution based on command
    if args.command == "generate":
        config_generator()
    elif args.command == "run":
        run_experiments(config_file=args.config)
    elif args.command == "collect":
        collect_data()
    elif args.command == "clear":
        clear_all()


if __name__ == "__main__":
    main()
