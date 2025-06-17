"""Plot the numbers computed by the other scripts."""

import pickle
from collections import Counter
from typing import Any, Union

import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib as tikz

np.Inf = np.inf
np.float_ = np.float64


def re_structure(
    pids: list[str], counter_dict: dict[str, dict[str, Any]]
) -> None:
    """Restructure counter dictionaries remove the top layer.

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
        rmdval = (
            data_dict_by_conf[conf_key].pop(("README.md", True), 0)
            + data_dict_by_conf[conf_key].pop(("README.rst", True), 0)
            + data_dict_by_conf[conf_key].pop(("readme.md", True), 0)
            + data_dict_by_conf[conf_key].pop(("readme.rst", True), 0)
            + data_dict_by_conf[conf_key].pop(("Readme.md", True), 0)
            + data_dict_by_conf[conf_key].pop(("Readme.rst", True), 0)
        )
        data_dict_by_conf[conf_key][("README", True)] = rmdval

        # merge tests and test folder
        testfolderval = data_dict_by_conf[conf_key].pop(
            ("test", True), 0
        ) + data_dict_by_conf[conf_key].pop(("tests", True), 0)
        data_dict_by_conf[conf_key][("test-folder", True)] = testfolderval

        data_dict_by_conf[conf_key]['page_total'] = counter_dict[conf_key]['page_total']

    return data_dict_by_conf

def plot_data(data_dict_by_conf, plot_prefix):

    def _set_up_plot(
        keys: list[tuple[str, bool]], filename: Union[str, None] = None
    ) -> None:

        for key in keys:
            for conf in data_dict_by_conf.keys():
                data_dict = data_dict_by_conf[conf]
                labels = sorted(list(data_dict.keys()))
                data = []
                for label in labels:
                    try:
                        dat = data_dict[label][key]
                    except KeyError as e:
                        print(f"Key {label} not found, {e}.")
                        dat = 0
                    data.append(dat/data_dict[label]['page_total'])
                plt.plot(labels, data, label=conf)
            plt.title(key[0])
            plt.legend()
            
            if filename:
                tikz.save(f"./plots/{filename}_{key[0]}.tex", standalone=True)
            plt.show()
            plt.clf()


    # License
    keys = [("LICENSE", True)]
    _set_up_plot(keys, f"{plot_prefix}")

    # Readme
    keys = [("README", True)]
    _set_up_plot(keys, f"{plot_prefix}")

    # Python
    keys = [("uses_python", True)]
    _set_up_plot(keys, f"{plot_prefix}")

    # Requirements
    keys = [("requirements.txt", True), ("environment.yml", True), ("uv.lock", True), 
            ("Pipfile.lock", True), ("poetry.lock", True), ("pixi.lock", True)]
    _set_up_plot(keys, f"{plot_prefix}_requirements")

    # packaging
    keys = [
        ("setup.py", True),
        ("setup.cfg", True),
        ("pyproject.toml", True),
        ("hatch.toml", True),
        ("pixi.toml", True)
    ]
    _set_up_plot(keys, f"{plot_prefix}_packaging")

    # Tests and container
    keys = [
        ("test-folder", True),
        ("tox", True),
        ("noxfile.py", True),
        (".pre-commit-config.yaml", True),
        (".github/workflows", True),
    ]
    _set_up_plot(keys, f"{plot_prefix}_tests")


if __name__ == "__main__":
    # PLOT ICML stats.
    file_ids = [f"icml20{year}" for year in range(16, 25)]
    pids = [f"{year}" for year in range(16, 25)]
    icml_counter_dict = {}

    for fid, pid in zip(file_ids, pids):
        with open(f"./storage/{fid}_stored_counters.pkl", "rb") as f:
            id_counters = pickle.load(f)
            icml_counter_dict[pid] = id_counters

    structured_icml_dict = re_structure(pids, icml_counter_dict)

    # PLOT aistats stats.
    file_ids = [f"aistats20{year}" for year in range(17, 25)]
    pids = [f"{year}" for year in range(17, 25)]
    aistats_counter_dict = {}
    
    for fid, pid in zip(file_ids, pids):
        with open(f"./storage/{fid}_stored_counters.pkl", "rb") as f:
            id_counters = pickle.load(f)
            aistats_counter_dict[pid] = id_counters

    structured_aistats_dict = re_structure(pids, aistats_counter_dict)
     
    # PLOT Neurips stats
    file_ids = [f"nips20{year}" for year in range(16, 25)]
    pids = [f"{year}" for year in range(16, 25)]
    neurips_counter_dict = {}

    for fid, pid in zip(file_ids, pids):
        with open(f"./storage/{fid}_stored_counters.pkl", "rb") as f:
            id_counters = pickle.load(f)
            neurips_counter_dict[pid] = id_counters

    structured_neurips_dict = re_structure(pids, neurips_counter_dict)


    # PLOT ICLR
    file_ids = ["ICLR.cc_2017_conference"] + [f"ICLR.cc_20{year}_Conference" for year in range(20, 26)]
    pids = [f"{year}" for year in range(20, 26)] + ["25"]
    iclr_counter_dict = {}
    
    for fid, pid in zip(file_ids, pids):
        with open(f"./storage/{fid}_stored_counters.pkl", "rb") as f:
            id_counters = pickle.load(f)
            iclr_counter_dict[pid] = id_counters

    structured_iclr_dict = re_structure(pids, iclr_counter_dict)
    
    # PLOT TMLR
    file_ids = ["tmlr"]
    pids = ["all"]
    counter_dict = {}

    for fid, pid in zip(file_ids, pids):
        with open(f"./storage/{fid}_stored_counters.pkl", "rb") as f:
            id_counters = pickle.load(f)
            counter_dict[pid] = id_counters

    counter_dict = counter_dict["all"]

    readme_file_types = [
        "README.md",
        "Readme.md",
        "readme.md",
        "README.rst",
        "Readme.rst",
        "readme.rst",
    ]
    readmecout = sum([counter_dict["files"][(rmd, True)] for rmd in readme_file_types])
    file_total = counter_dict["page_total"]

    dependencies_counter = sum(
        [
            counter_dict["files"][(deb, True)]
            for deb in ["requirements.txt", "environment.yml", "uv.lock"]
        ]
    )
    packaged_counter = sum(
        [
            counter_dict["files"][(deb, True)]
            for deb in ["setup.py", "setup.cfg", "pyproject.toml", "hatch.toml"]
        ]
    )
    test_folder = sum(
        [counter_dict["folders"][(deb, True)] for deb in ["test", "tests"]]
    )

    plt.bar(
        ["README", "python", "LICENSE", "dependencies", "packaged", "test-folder"],
        [
            round(readmecout / file_total * 100, 1),
            round(counter_dict["language"]["uses_python", True] / file_total * 100, 1),
            round(counter_dict["files"]["LICENSE", True] / file_total * 100, 1),
            round(dependencies_counter / file_total * 100, 1),
            round(packaged_counter / file_total * 100, 1),
            round(test_folder / file_total * 100, 1),
        ],
    )
    plt.grid()
    plt.show()

    # TODO create line plots.
    confs = {"icml": structured_icml_dict, "aistats": structured_aistats_dict,
             "iclr": structured_iclr_dict, "neurips": structured_neurips_dict}
    counter_dict.keys()

    plot_data(confs, "line_plots")
    pass