"""
Dump decay.json file with coefficients taken from analytic parametrization pag.28 in https://arxiv.org/pdf/1906.06949.pdf
"""
import argparse
import json


def parse_args():
    parser = argparse.ArgumentParser(description="Dump decay.json file")
    parser.add_argument("--out", dest="out", required=True, help="Output directory")
    return parser.parse_args()


def main(args):
    dct = {"hgg": {}, "tot": {"A_cdp": 1.83, "A_cpg": 50.6}}

    with open("{}/decay.json".format(args.out), "w") as f:
        json.dump(dct, f, indent=4)


if __name__ == "__main__":
    args = parse_args()
    main(args)
