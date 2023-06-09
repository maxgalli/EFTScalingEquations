import matplotlib.pyplot as plt
import numpy as np
import json


input_files = [
    # "../equations/CMS-prelim-SMEFT-topU3l_22_05_05/differentials/decays/hzz/ggHZZ_SMEFTsim_topU3l_pt_h.json",
    # "../equations/CMS-prelim-SMEFT-topU3l_22_05_05/differentials/decays/hzz/HZZ_SMEFTsim_topU3l_pt_h.json",
    "../equations/CMS-prelim-SMEFT-topU3l_22_05_05/differentials/decays/hzz/ggHZZ_SMEFTsim_topU3l_pt_h.json",
    "../equations/CMS-prelim-SMEFT-topU3l_22_05_05/differentials/decays/hzz/ggHZZ_SMEFTsim_topU3l_pt_hc.json",
    "../equations/CMS-prelim-SMEFT-topU3l_22_05_05/differentials/decays/hzz/ggHZZ_SMEFTsim_topU3l_deltaphijj.json",
    "../equations/CMS-prelim-SMEFT-topU3l_22_05_05/differentials/decays/hww/ggHWW_SMEFTsim_topU3l_pt_h.json",
]

output_dirs = [
    # "/eos/home-g/gallim/www/plots/DifferentialCombination/CombinationRun2/Checks/230519_mattchecks",
    # "/eos/home-g/gallim/www/plots/DifferentialCombination/CombinationRun2/Checks/230601_mattchecks_deconly",
    "/eos/home-g/gallim/www/plots/DifferentialCombination/CombinationRun2/Checks/230605_mattchecks_morestats",
    "/eos/home-g/gallim/www/plots/DifferentialCombination/CombinationRun2/Checks/230605_mattchecks_morestats_pthc",
    "/eos/home-g/gallim/www/plots/DifferentialCombination/CombinationRun2/Checks/230605_mattchecks_deltaphijj",
    "/eos/home-g/gallim/www/plots/DifferentialCombination/CombinationRun2/Checks/230608_mattchecks_hww",
]

inclusive_pred_file = "../equations/CMS-prelim-SMEFT-topU3l_22_05_05_AccCorr/decay.json"

with open(inclusive_pred_file) as f:
    inclusive_pred_dct = json.load(f)

names = [f.split("/")[-1] for f in output_dirs]

max_diffs = {}

for name, input_file, output_dir in zip(names, input_files, output_dirs):
    print("Plotting {}".format(name))
    channel = "ZZ" if "ZZ" in input_file else "WW"

    differences = []

    with open(input_file) as f:
        coeff_dct = json.load(f)

    coeffs = []
    for bin in coeff_dct:
        bin_dct = coeff_dct[bin]
        for key in bin_dct:
            if key.startswith("A_"):
                if key not in coeffs:
                    coeffs.append(key)
            if key.startswith("B_") and key.endswith("_2"):
                if key not in coeffs:
                    coeffs.append(key)
    print(coeffs)

    for coeff in coeffs:
        # for coeff in coeffs[:2]:
        print("Plotting {}".format(coeff))
        # fig, (ax, rax) = plt.subplots(
        #    2, 1, figsize=(12, 10), gridspec_kw={"height_ratios": [3, 2]}, sharex=True
        # )
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        x = []
        vals = []
        uncs = []
        for bin in coeff_dct:
            bin_dct = coeff_dct[bin]
            try:
                coeff_unc = "u_" + coeff
                val = bin_dct[coeff]
                unc = bin_dct[coeff_unc]
                x.append(float(bin))
                vals.append(val)
                uncs.append(unc)
                print("bin: {}, val: {}, unc: {}".format(bin, val, unc))
            except KeyError:
                print(f"Key {key} not found in bin {bin}")
                pass
        ax.errorbar(x, vals, yerr=uncs, fmt="o")

        # draw a band
        try:
            central_value = inclusive_pred_dct[channel][coeff]
            unc = inclusive_pred_dct[channel]["u_" + coeff]
            ax.axhspan(central_value - unc, central_value + unc, alpha=0.2, color="red")
            ax.axhline(central_value, color="red", linestyle="--")
        except KeyError:
            print(f"Key {key} not found in inclusive prediction")
            pass

        ax.set_xlabel("pT [GeV]")
        ax.set_ylabel(coeff)
        ax.set_title(coeff)
        # ax.legend()

        mx = max(vals)
        mn = min(vals)
        # relative difference between max and min
        rel_diff = np.abs((mx - mn) / mx)
        differences.append((coeff, rel_diff))

        for ext in ["png", "pdf"]:
            fig.savefig("{}/{}.{}".format(output_dir, coeff, ext))
        plt.close(fig)

    # sort by relative difference
    differences.sort(key=lambda x: x[1], reverse=True)
    print(differences)

    max_diffs[name] = differences

# pretty print dictionary
print(json.dumps(max_diffs, indent=4))

# write to json file
with open("max_diffs.json", "w") as f:
    json.dump(max_diffs, f, indent=4)
