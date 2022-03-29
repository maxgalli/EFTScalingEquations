import sys
import yaml
import json


def main():
    """
    """
    if len(sys.argv) != 2:
        print("Usage: eft2obs_to_channels.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    with open(input_file, "r") as f:
        channel_file = yaml.safe_load(f)

    output_dict = {}

    for channel, file in channel_file.items():
        output_dict[channel] = {}
        with open(file, "r") as f:
            eft2obs_dct = json.load(f)
        edges_list = eft2obs_dct["edges"]
        bins = eft2obs_dct["bins"]
        for edges, deviations in zip(edges_list, bins):
            bin_name = "{}_{}".format(
                str(edges[0]).replace(".", "p"), str(edges[1]).replace(".", "p")
            )
            output_dict[channel][bin_name] = {}
            for dev in deviations:
                val = dev[0]
                unc = dev[1]
                pars = dev[2:]
                if len(pars) == 1:
                    output_dict[channel][bin_name]["A_{}".format(pars[0])] = val
                    output_dict[channel][bin_name]["u_A_{}".format(pars[0])] = unc
                elif len(pars) == 2:
                    if pars[0] == pars[1]:
                        output_dict[channel][bin_name]["B_{}_2".format(pars[0])] = val
                        output_dict[channel][bin_name]["u_B_{}_2".format(pars[0])] = unc
                    else:
                        output_dict[channel][bin_name][
                            "B_{}_{}".format(pars[0], pars[1])
                        ] = val
                        output_dict[channel][bin_name][
                            "u_B_{}_{}".format(pars[0], pars[1])
                        ] = unc

    with open("channels.json", "w") as f:
        json.dump(output_dict, f, indent=4)


if __name__ == "__main__":
    main()
