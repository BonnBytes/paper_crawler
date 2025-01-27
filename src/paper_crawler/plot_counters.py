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
    keys = []
    keys.extend(counter_dict[pid[0].keys()])


    x = np.arange(len(pids))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for counter, conference in counter_dict.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Length (mm)')
    ax.set_title('Penguin attributes by species')
    ax.set_xticks(x + width, species)
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, 250)

    plt.show()