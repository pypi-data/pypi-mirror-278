import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
from pathlib import Path


def boxplot():
    labels = ["Real images",
              "Synthetic images",
              ]
    path = Path("result", "aia", "real", "balanced_accuracy.pickle")
    with open(path, 'rb') as f:
        x_real = pickle.load(f)

    path = Path("result", "aia", "synth", "balanced_accuracy.pickle")
    with open(path, 'rb') as f:
        x_synth = pickle.load(f)

    x = [x_real, x_synth]

    save_path = Path("plot", "aia")
    os.makedirs(save_path, exist_ok=True)
    save_path = Path(save_path, "balanced_accuracy.pdf")

    font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 18}

    matplotlib.rc('font', **font)

    plt.boxplot(x, tick_labels=labels)
    plt.ylabel("Balanced accuracy of the AIA")
    #plt.xlabel("Data type")
    plt.savefig(save_path, bbox_inches="tight")

if __name__=="__main__":
    boxplot()
