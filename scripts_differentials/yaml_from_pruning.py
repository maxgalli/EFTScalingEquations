"""
Run with python3

Get the relevant WCs from production JSON files from all the available channels and decay JSON file.
All the WCs with values above the thrshold that are found in AT LEAST ONE of the JSON files are kept.
Run from inside EFTScalingEquations.
The output is a YAML file that can be used for the fits in either chi_square_fitter.py or combine. Note that the min and max value will have to be calibrated by hand.

Example call:
python scripts_differentials/yaml_from_pruning.py --prediction-dir equations/CMS-prelim-SMEFT-topU3l_22_05_05 --output-file /work/gallim/DifferentialCombination_home/DifferentialCombinationRun2/metadata/SMEFT/221117Prune.yml
"""
import argparse
from pathlib import Path
import yaml
import json
import os


def parse_arguments():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--prediction-dir", type=str, required=True)
    parser.add_argument("--output-file", type=str, required=True)
    parser.add_argument(
        "--observables", nargs="+", type=str, required=False, default=["pt"], help=""
    )
    parser.add_argument(
        "--production-modes",
        nargs="+",
        type=str,
        required=False,
        default=["ggH"],
        help="",
    )
    parser.add_argument("--threshold", type=float, default=0.0001)
    parser.add_argument("--skip-quadratic", action="store_true", default=False)
    parser.add_argument("--new-dir", action="store_true", default=False)

    return parser.parse_args()


def main(args):
    file_names = {
        "pt": {
            "ggH": {
                "hgg": "{}/differentials/hgg/ggH_SMEFTatNLO_pt_gg.json",
                "hzz": "{}/differentials/hzz/ggH_SMEFTatNLO_pt_h.json",
                "htt": "{}/differentials/htt/ggH_SMEFTatNLO_pt_h.json",
                "hww": "{}/differentials/hww/ggH_SMEFTatNLO_pt_h.json",
                "hbbvbf": "{}/differentials/hbbvbf/ggH_SMEFTatNLO_pt_h.json",
                "httboost": "{}/differentials/httboost/ggH_SMEFTatNLO_pt_h.json",
            }
        }
    }
    good_coeffs = []
    all_files_to_open = [f"{args.prediction_dir}/decay.json"]
    for obs in args.observables:
        for prod in args.production_modes:
            for chan in file_names[obs][prod]:
                full_path = file_names[obs][prod][chan].format(args.prediction_dir)
                if Path(full_path).is_file():
                    all_files_to_open.append(full_path)
    print(all_files_to_open)

    # YAML file
    for file_name in all_files_to_open:
        with open(file_name, "r") as f:
            dct = json.load(f)
            for edge in dct:
                for expression in dct[edge]:
                    if expression.startswith("A_"):
                        wc = expression.split("_")[1]
                        if (
                            abs(dct[edge][expression]) > args.threshold
                            and wc not in good_coeffs
                        ):
                            good_coeffs.append(wc)
                    elif (
                        expression.startswith("B")
                        and expression.endswith("2")
                        and not args.skip_quadratic
                    ):
                        wc = expression.split("_")[1]
                        if (
                            abs(dct[edge][expression]) > args.threshold
                            and wc not in good_coeffs
                        ):
                            good_coeffs.append(wc)
    print(good_coeffs)
    print(len(good_coeffs))

    dct_to_dump = {}
    for wc in good_coeffs:
        dct_to_dump[wc] = {"val": 0.0, "max": 10.0, "min": -10.0}

    with open(args.output_file, "w") as f:
        yaml.dump(dct_to_dump, f)

    # New directory
    if args.new_dir:
        print("New directory")
        new_prediction_dir = (
            args.prediction_dir + f"_pruned{str(args.threshold).replace('.', 'p')}"
        )

        for file_name in all_files_to_open:
            print(file_name)
            new_dct = {}
            with open(file_name, "r") as f:
                dct = json.load(f)
                for edge in dct:
                    new_dct[edge] = {}
                    for expression in dct[edge]:
                        if not expression.startswith("u_"):
                            if abs(dct[edge][expression]) > args.threshold:
                                new_dct[edge][expression] = dct[edge][expression]
            new_file_name = file_name.replace(args.prediction_dir, new_prediction_dir)
            Path("/".join(new_file_name.split("/")[:-1])).mkdir(
                parents=True, exist_ok=True
            )
            with open(new_file_name, "w") as f:
                json.dump(new_dct, f, indent=4)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
