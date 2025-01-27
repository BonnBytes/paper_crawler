import pickle
import matplotlib.pyplot as plt
import numpy as np

from collections import Counter


if __name__ == "__main__":

    file_ids = ['ICLR.cc_2024_Conference', 'icml2024', 'icml2023']
    pids = ["ICML-2024", "ICML-2023", "ICLR-2024"]
    counter_dict = {}

    for fid, pid in zip(file_ids, pids):
        with open(f"./storage/stored_counters_{fid}.pkl", "rb") as f:
            id_counters = pickle.load(f)
            counter_dict[pid] = id_counters


    # restructure data
    software_keys = []
    software_keys.extend(counter_dict[pids[0]]['files'].keys())
    software_keys.extend(counter_dict[pids[0]]['folders'].keys())
    software_keys.extend(counter_dict[pids[0]]['language'].keys())

    def find_key(counters, data_key):
        for counter in counters.values():
            test = list(filter(lambda ftuple: data_key == ftuple[0], counter.items()))
            if test:
                return test[0][1]
        raise KeyError("Key not found.")


    data_dict_by_feature = {}
    for conf_key in pids:
        for data_key in software_keys:
            if data_key in data_dict_by_feature.keys():
                data_dict_by_feature[data_key][conf_key] = find_key(counter_dict[conf_key], data_key)
            else:
                data_dict_by_feature[data_key] = {}
                key_val = find_key(counter_dict[conf_key], data_key)
                data_dict_by_feature[data_key][conf_key] = key_val


    data_dict_by_conf = {}
    for pid in pids:
        data_dict_by_conf[pid] = {}
    for software_feature_key, conf_dict in data_dict_by_feature.items():
        for pid in pids:
            data_dict_by_conf[pid][software_feature_key] = conf_dict[pid]

    x = np.arange(len(software_keys))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for conf_key, conf_values in data_dict_by_conf.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, list((round((conf_values[key] / counter_dict[conf_key]['page_total'])*100., 2) for key in software_keys)), width, label=conf_key)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('share')
    ax.set_title('Software by conference')
    ax.set_xticks(x + width, (sk[0] for sk in software_keys))
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, 100)

    plt.show()
    pass