import argparse
import logging

from experiments.runner import ExperimentRunner

logging.basicConfig(level=logging.INFO)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", type=str, default="experiments/configs/base.yaml")

    parser.add_argument("--override", nargs="*", help="format: key.subkey=value")

    parser.add_argument("--batch", type=str, default=None)

    return parser.parse_args()


def parse_overrides(override_list):
    if not override_list:
        return {}

    overrides = {}

    for item in override_list:
        key, value = item.split("=")

        # convert string "a.b.c" → nested dict
        keys = key.split(".")
        d = overrides

        for k in keys[:-1]:
            d = d.setdefault(k, {})

        # cast value (int/float/bool fallback)
        if value.isdigit():
            value = int(value)
        elif value.replace(".", "", 1).isdigit():
            value = float(value)
        elif value.lower() in ["true", "false"]:
            value = value.lower() == "true"

        d[keys[-1]] = value

    return overrides


def main():
    args = parse_args()

    if args.batch:
        logging.info("Batch mode not implemented yet")
        return

    overrides = parse_overrides(args.override)

    runner = ExperimentRunner(config_path=args.config, overrides=overrides)

    runner.run()


if __name__ == "__main__":
    main()
