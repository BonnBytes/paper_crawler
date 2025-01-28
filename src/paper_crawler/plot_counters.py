import pickle
import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib as tikz
import numpy as np

from collections import Counter

np.Inf = np.inf
np.float_ = np.float64


if __name__ == "__main__":
    ## PLOT ICML stats.
    file_ids = [f"icml20{year}" for year in range(14, 25)]
    pids = [f"{year}" for year in range(14, 25)]
    counter_dict = {}

    for fid, pid in zip(file_ids, pids):
        with open(f"./storage/stored_counters_{fid}.pkl", "rb") as f:
            id_counters = pickle.load(f)
            counter_dict[pid] = id_counters

    # restructure data
    software_keys = []
    software_keys.extend(counter_dict[pids[-1]]['files'].keys())
    software_keys.extend(counter_dict[pids[-1]]['folders'].keys())
    software_keys.extend(counter_dict[pids[-1]]['language'].keys())

    def find_key(counters, data_key):
        for counter in counters.values():
            if type(counter) is Counter:
                test = list(filter(lambda ftuple: data_key == ftuple[0], counter.items()))
                if test:
                    return test[0][1]
        raise KeyError("Key not found.")

    data_dict_by_feature = {}
    for conf_key in pids:
        for data_key in software_keys:
            if data_key in data_dict_by_feature.keys():
                try:
                    data_dict_by_feature[data_key][conf_key] = find_key(counter_dict[conf_key], data_key)
                except KeyError as e:
                    print(f"Key {data_key} not found.")
                    data_dict_by_feature[data_key][conf_key] = 0
            else:
                try:
                    data_dict_by_feature[data_key] = {}
                    key_val = find_key(counter_dict[conf_key], data_key)
                    data_dict_by_feature[data_key][conf_key] = key_val
                except KeyError as e:
                    print(f"Key {data_key} not found.")
                    data_dict_by_feature[data_key][conf_key] = 0

    data_dict_by_conf = {}
    for pid in pids:
        data_dict_by_conf[pid] = {}
    for software_feature_key, conf_dict in data_dict_by_feature.items():
        for pid in pids:
            data_dict_by_conf[pid][software_feature_key] = conf_dict[pid]

    # post-processing
    for conf_key in data_dict_by_conf.keys():
        # merge tox
        toxval = data_dict_by_conf[conf_key].pop(("tox.toml", True), 0) \
            + data_dict_by_conf[conf_key].pop(("tox.ini", True), 0)
        data_dict_by_conf[conf_key][("tox", True)] = toxval

        # merge readme
        rmdval = data_dict_by_conf[conf_key].pop(("README.md", True), 0) \
                    + data_dict_by_conf[conf_key].pop(("README.rst", True), 0)
        data_dict_by_conf[conf_key][("README", True)] = rmdval

        # merge tests and test folder
        testfolderval = data_dict_by_conf[conf_key].pop(("test", True), 0) \
                    + data_dict_by_conf[conf_key].pop(("tests", True), 0)
        data_dict_by_conf[conf_key][("test-folder", True)] = testfolderval

        # remove setup.cfg
        data_dict_by_conf[conf_key].pop(("setup.cfg", True))

    # software_keys = list(data_dict_by_conf['ICML-2024'].keys())
    software_keys = [('LICENSE', True),
                     ('README', True),
                     ('uses_python', True),
                     ('requirements.txt', True),
                     ('setup.py', True),
                     ('pyproject.toml', True),
                     ('test-folder', True),
                     ('tox', True),
                     ('noxfile.py', True),
                     ('.github/workflows', True)]
    
    def set_up_plot(keys: str, filename: str = None):
        x = np.arange(len(keys))  # the label locations
        width = 0.08  # the width of the bars
        multiplier = -4
        fig, ax = plt.subplots(layout='constrained')
        for conf_key, conf_values in data_dict_by_conf.items():
            offset = width * multiplier
            rects = ax.bar(x + offset, list((round((conf_values[key] / counter_dict[conf_key]['page_total'])*100., 1) for key in keys)),
                           width, label=conf_key)
            ax.bar_label(rects, padding=3)
            multiplier += 1

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel("adoption [%]")
        ax.set_xticks(x + width, (sk[0] for sk in keys))
        ax.legend(loc='best', ncol=3)
        ax.set_ylim(0, 119)

        if filename:
            tikz.save(f'./plots/{filename}.tex', standalone=True)
        plt.show()

    ## License and Readme
    keys = [("LICENSE", True),
            ("README", True)]
    set_up_plot(keys, "license_and_readme")

    ## Python
    keys = [("uses_python", True)]
    set_up_plot(keys, "uses_python")

    ## Requirements
    keys = [("requirements.txt", True)]
    set_up_plot(keys, "requirements")

    ## packaging
    keys = [("setup.py", True),
            ("pyproject.toml", True)]
    set_up_plot(keys, "packaging")

    ## Tests and container
    keys = [("test-folder", True),
            ("tox", True),
            ("noxfile.py", True),
            (".github/workflows", True)]
    set_up_plot(keys, "tests")
