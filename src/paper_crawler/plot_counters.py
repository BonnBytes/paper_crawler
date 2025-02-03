"""Plot the numbers computed by the other scripts."""

import pickle
from collections import Counter
from typing import Any, Union

import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib as tikz

np.Inf = np.inf
np.float_ = np.float64


def structure_and_plot(
    pids: list[str], counter_dict: dict[str, dict[str, Any]], plot_prefix: str
) -> None:
    """Restructure counter dictionaries and generate bar plots for practice adoption.

    Args:
        pids (list[str]): A list of plot-conference IDs to process.
        counter_dict (dict): A dictionary containing counters
            for different software features.
        plot_prefix (str): A prefix to use for the plot filenames.
    """
    # restructure data
    software_keys: list[tuple[str, bool]] = []
    software_keys.extend(counter_dict[pids[-1]]["files"].keys())
    software_keys.extend(counter_dict[pids[-1]]["folders"].keys())
    software_keys.extend(counter_dict[pids[-1]]["language"].keys())

    def find_key(counters: dict[str, Any], data_key: tuple[str, bool]) -> Any:
        for counter in counters.values():
            if type(counter) is Counter:
                test = list(
                    filter(lambda ftuple: data_key == ftuple[0], counter.items())
                )
                if test:
                    return test[0][1]
        raise KeyError("Key not found.")

    data_dict_by_feature: dict[tuple[str, bool], dict[str, int]] = {}
    for conf_key in pids:
        for data_key in software_keys:
            if data_key in data_dict_by_feature.keys():
                try:
                    data_dict_by_feature[data_key][conf_key] = find_key(
                        counter_dict[conf_key], data_key
                    )
                except KeyError as e:
                    print(f"Key {data_key} not found: {e}")
                    data_dict_by_feature[data_key][conf_key] = 0
            else:
                try:
                    data_dict_by_feature[data_key] = {}
                    key_val = find_key(counter_dict[conf_key], data_key)
                    data_dict_by_feature[data_key][conf_key] = key_val
                except KeyError as e:
                    print(f"Key {data_key} not found: {e}.")
                    data_dict_by_feature[data_key][conf_key] = 0

    data_dict_by_conf: dict[str, dict[tuple[str, bool], int]] = {}
    for pid in pids:
        data_dict_by_conf[pid] = {}
    for software_feature_key, conf_dict in data_dict_by_feature.items():
        for pid in pids:
            data_dict_by_conf[pid][software_feature_key] = conf_dict[pid]

    # post-processing
    for conf_key in data_dict_by_conf.keys():
        # merge tox
        toxval = data_dict_by_conf[conf_key].pop(
            ("tox.toml", True), 0
        ) + data_dict_by_conf[conf_key].pop(("tox.ini", True), 0)
        data_dict_by_conf[conf_key][("tox", True)] = toxval

        # merge readme
        rmdval = data_dict_by_conf[conf_key].pop(
            ("README.md", True), 0
        ) + data_dict_by_conf[conf_key].pop(("README.rst", True), 0)
        data_dict_by_conf[conf_key][("README", True)] = rmdval

        # merge tests and test folder
        testfolderval = data_dict_by_conf[conf_key].pop(
            ("test", True), 0
        ) + data_dict_by_conf[conf_key].pop(("tests", True), 0)
        data_dict_by_conf[conf_key][("test-folder", True)] = testfolderval

        # remove setup.cfg
        data_dict_by_conf[conf_key].pop(("setup.cfg", True))

    # software_keys = list(data_dict_by_conf['ICML-2024'].keys())
    software_keys = [
        ("LICENSE", True),
        ("README", True),
        ("uses_python", True),
        ("requirements.txt", True),
        ("setup.py", True),
        ("pyproject.toml", True),
        ("test-folder", True),
        ("tox", True),
        ("noxfile.py", True),
        (".github/workflows", True),
        ("environment.yml", True),
    ]

    def _set_up_plot(
        keys: list[tuple[str, bool]], filename: Union[str, None] = None
    ) -> None:
        x = np.arange(len(keys))  # the label locations

        if filename and "icml" in filename:
            multiplier = -4
            width = 0.08  # the width of the bars
        else:
            multiplier = 0
            width = 0.25  # the width of the bars
        fig, ax = plt.subplots(layout="constrained")
        for conf_key, conf_values in data_dict_by_conf.items():
            offset = width * multiplier
            page_total = counter_dict[conf_key]["page_total"]
            rects = ax.bar(
                x + offset,
                list(
                    (
                        round(
                            (conf_values[key] / page_total) * 100.0,
                            1,
                        )
                        for key in keys
                    )
                ),
                width,
                label=conf_key,
            )
            ax.bar_label(rects, padding=3)
            multiplier += 1

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel("adoption [%]")
        ax.set_xticks(x + width, (sk[0] for sk in keys))
        ax.legend(loc="best", ncol=3)
        ax.set_ylim(0, 119)

        if filename:
            tikz.save(f"./plots/{filename}.tex", standalone=True)
        plt.show()

    # License and Readme
    keys = [("LICENSE", True), ("README", True)]
    _set_up_plot(keys, f"{plot_prefix}_license_and_readme")

    # Python
    keys = [("uses_python", True)]
    _set_up_plot(keys, f"{plot_prefix}_uses_python")

    # Requirements
    keys = [("requirements.txt", True), ("environment.yml", True)]
    _set_up_plot(keys, f"{plot_prefix}_requirements")

    # packaging
    keys = [("setup.py", True), ("pyproject.toml", True)]
    _set_up_plot(keys, f"{plot_prefix}_packaging")

    # Tests and container
    keys = [
        ("test-folder", True),
        ("tox", True),
        ("noxfile.py", True),
        (".github/workflows", True),
    ]
    _set_up_plot(keys, f"{plot_prefix}_tests")


if __name__ == "__main__":
    # PLOT ICML stats.
    file_ids = [f"icml20{year}" for year in range(14, 25)]
    pids = [f"{year}" for year in range(14, 25)]
    counter_dict = {}

    for fid, pid in zip(file_ids, pids):
        with open(f"./storage/stored_counters_{fid}.pkl", "rb") as f:
            id_counters = pickle.load(f)
            counter_dict[pid] = id_counters

    structure_and_plot(pids, counter_dict, "icml")

    # ML in 2024
    file_ids = ["icml2024", "ICLR.cc_2024_Conference", "NeurIPS.cc_2024_Conference"]
    pids = ["ICML", "ICLR", "NeurIPS"]
    counter_dict = {}

    for fid, pid in zip(file_ids, pids):
        with open(f"./storage/stored_counters_{fid}.pkl", "rb") as f:
            id_counters = pickle.load(f)
            counter_dict[pid] = id_counters

    structure_and_plot(pids, counter_dict, "ml_in_2024")
