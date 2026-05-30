import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import argparse

from src.batch_runner import BatchRunner

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--config", type=str)
    parser.add_argument("--config_dir", type=str, default="configs/generated")
    args = parser.parse_args()

    cfg_files = (
        [Path(args.config)]
        if args.config
        else sorted(Path(args.config_dir).glob("*.yaml"))
    )
    BatchRunner(cfg_files).run_all()
