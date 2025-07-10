"""Plot the numbers computed by the other scripts."""

import pickle
from collections import Counter
from typing import Any, Union

import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib as tikz

# tikzplotlib backwards compatability
# we need to load an old version of matplotlib.
# https://github.com/nschloe/tikzplotlib/issues/605
np.Inf = np.inf  # type: ignore
np.float_ = np.float64  # type: ignore


def re_structure(
    pids: list[str], counter_dict: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    """Restructure counter dictionaries remove the top layer.

    Args:
        pids (list[str]): A list of plot-conference IDs to process.
        counter_dict (dict): A dictionary containing counters
            for different software features.
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

        # merge environment
        env_val = data_dict_by_conf[conf_key].pop(
            ("environment.yml", True), 0
        ) + data_dict_by_conf[conf_key].pop(("environment.yaml", True), 0)
        data_dict_by_conf[conf_key][("environment", True)] = env_val

        # merge make
        make_val = (
            data_dict_by_conf[conf_key].pop(("makefile", True), 0)
            + data_dict_by_conf[conf_key].pop(("Makefile", True), 0)
            + data_dict_by_conf[conf_key].pop(("GNUmakefile", True), 0)
        )
        data_dict_by_conf[conf_key][("Makefile", True)] = make_val

        # merge docs
        docval = data_dict_by_conf[conf_key].pop(("doc", True), 0) + data_dict_by_conf[
            conf_key
        ].pop(("docs", True), 0)
        data_dict_by_conf[conf_key][("docs", True)] = docval

        # merge tests and test folder
        testfolderval = (
            data_dict_by_conf[conf_key].pop(("test", True), 0)
            + data_dict_by_conf[conf_key].pop(("tests", True), 0)
            + data_dict_by_conf[conf_key].pop(("src/test", True), 0)
            + data_dict_by_conf[conf_key].pop(("src/tests", True), 0)
            + data_dict_by_conf[conf_key].pop(("package/test", True), 0)
            + data_dict_by_conf[conf_key].pop(("package/tests", True), 0)
        )
        data_dict_by_conf[conf_key][("test-folder", True)] = testfolderval

        data_dict_by_conf[conf_key]["page_total"] = counter_dict[conf_key]["page_total"]  # type: ignore

    return data_dict_by_conf


def plot_data(data_dict_by_conf: dict[str, Any], plot_prefix: str) -> None:
    """Generate and display multiple plots showing adoption rates.

    data_dict_by_conf (dict):
        As generated by the re_structure function.
    plot_prefix (str):
        Prefix used for naming the output plot files.

    Side Effects:
        - Displays plots using matplotlib.
        - Saves plots as TikZ/LaTeX files in the './plots/' directory
          if a filename is provided.
        - Prints warnings if expected keys are missing in the data.
    """

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
                    data.append((dat / data_dict[label]["page_total"]) * 100)
                plt.plot(labels, data, ".-", label=conf)
            plt.title(key[0])
            plt.legend()
            # plt.ylim(0, 105)
            plt.grid()
            plt.ylabel("adoption [\%]")  # noqa: W605
            plt.xlabel("conference year")

            if filename:
                save_key = key[0].replace(".", "_").replace("/", "_")
                tikz.save(f"./plots/{filename}_{save_key}.tex", standalone=True)
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
    keys = [
        ("requirements.txt", True),
        ("environment", True),
        ("uv.lock", True),
        ("Pipfile.lock", True),
        ("poetry.lock", True),
        ("pixi.lock", True),
    ]
    _set_up_plot(keys, f"{plot_prefix}_requirements")

    # packaging
    keys = [
        ("src", True),
        ("setup.py", True),
        ("setup.cfg", True),
        ("pyproject.toml", True),
        ("hatch.toml", True),
        ("pixi.toml", True),
    ]
    _set_up_plot(keys, f"{plot_prefix}_packaging")

    # Tests and container
    keys = [
        ("test-folder", True),
        ("tox", True),
        ("noxfile.py", True),
        (".pre-commit-config.yaml", True),
        (".github/workflows", True),
        ("docs", True),
        ("Makefile", True),
    ]
    _set_up_plot(keys, f"{plot_prefix}_tests")


if __name__ == "__main__":
    # PLOT ICML stats.
    file_ids = [f"icml20{year}" for year in range(17, 25)] + ["ICML.cc_2025_Conference"]
    pids = [f"{year}" for year in range(17, 26)]
    icml_counter_dict = {}

    for fid, pid in zip(file_ids, pids):
        with open(f"./storage/{fid}_stored_counters.pkl", "rb") as f:
            id_counters = pickle.load(f)
            icml_counter_dict[pid] = id_counters

    structured_icml_dict = re_structure(pids, icml_counter_dict)

    # PLOT aistats stats.
    file_ids = [f"aistats20{year}" for year in range(17, 26)]
    pids = [f"{year}" for year in range(17, 26)]
    aistats_counter_dict = {}

    for fid, pid in zip(file_ids, pids):
        with open(f"./storage/{fid}_stored_counters.pkl", "rb") as f:
            id_counters = pickle.load(f)
            aistats_counter_dict[pid] = id_counters

    structured_aistats_dict = re_structure(pids, aistats_counter_dict)

    # PLOT Neurips stats
    file_ids = [f"nips20{year}" for year in range(17, 25)]
    pids = [f"{year}" for year in range(17, 25)]
    neurips_counter_dict = {}

    for fid, pid in zip(file_ids, pids):
        with open(f"./storage/{fid}_stored_counters.pkl", "rb") as f:
            id_counters = pickle.load(f)
            neurips_counter_dict[pid] = id_counters

    structured_neurips_dict = re_structure(pids, neurips_counter_dict)

    # PLOT ICLR
    file_ids = (
        ["iclr2016"]
        + ["ICLR.cc_2017_conference"]
        + ["iclr2018"]
        + ["iclr2019"]
        + [f"ICLR.cc_20{year}_Conference" for year in range(20, 26)]
    )
    pids = [f"{year}" for year in range(17, 26)] + ["25"]
    iclr_counter_dict = {}

    for fid, pid in zip(file_ids, pids):
        with open(f"./storage/{fid}_stored_counters.pkl", "rb") as f:
            id_counters = pickle.load(f)
            iclr_counter_dict[pid] = id_counters

    structured_iclr_dict = re_structure(pids, iclr_counter_dict)

    # PLOT TMLR
    def _bar_plots(conf: str) -> None:
        file_ids = [conf]
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
        readmecount = sum(
            [counter_dict["files"][(rmd, True)] for rmd in readme_file_types]
        )
        file_total = float(counter_dict["page_total"])

        dependencies_counter = sum(
            [
                counter_dict["files"][(deb, True)]
                for deb in [
                    "requirements.txt",
                    "environment.yml",
                    "environment.yaml",
                    "uv.lock",
                ]
            ]
        )
        packaged_counter = sum(
            [
                counter_dict["files"][(deb, True)]
                for deb in ["setup.py", "pyproject.toml", "hatch.toml"]
            ]
        )
        test_folder = sum(
            [
                counter_dict["folders"][(deb, True)]
                for deb in [
                    "test",
                    "tests",
                    "package/test",
                    "package/tests",
                    "src/test",
                    "src/tests",
                ]
            ]
        )

        doc_folder = sum(
            [
                counter_dict["folders"][(deb, True)]
                for deb in [
                    "doc",
                    "docs",
                ]
            ]
        )
        return {
            "README": readmecount / file_total,
            "file_total": file_total,
            "dependencies": dependencies_counter / file_total,
            "packaged": packaged_counter / file_total,
            "tests": test_folder / file_total,
            "docs": doc_folder / file_total,
            "python": counter_dict["language"]["uses_python", True] / file_total,
            "LICENSE": counter_dict["files"]["LICENSE", True] / file_total,
        }

    tmlr_data = _bar_plots("tmlr")

    # plot jmlr-mloss
    mloss_data = _bar_plots("mloss")

    tmlr_and_mloss = {"tmlr": tmlr_data, "mloss": mloss_data}

    xticks = [
        "README",
        "LICENSE",
        "python",
        "dependencies",
        "packaged",
        "tests",
        "docs",
    ]
    x = np.arange(len(xticks))
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout="constrained")
    for venue, adoption_rates in tmlr_and_mloss.items():
        offset = width * multiplier
        plt.bar(
            x + offset,
            [adoption_rates[tick] * 100.0 for tick in xticks],
            width=width,
            label=venue,
        )
        multiplier += 1
    ax.set_xticks(x + width, xticks)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Adoption [\%]")
    ax.set_title("Estimated adoption")
    ax.grid()
    ax.legend(loc="upper right", ncol=2)  # noqa: F541
    tikz.save(f"./plots/bar_plot.tex")
    plt.show()

    confs = {
        "icml": structured_icml_dict,
        "aistats": structured_aistats_dict,
        "iclr": structured_iclr_dict,
        "neurips": structured_neurips_dict,
    }

    plot_data(confs, "line_plots")
