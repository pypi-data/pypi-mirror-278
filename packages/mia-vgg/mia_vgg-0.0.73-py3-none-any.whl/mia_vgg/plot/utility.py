import pickle
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
from pathlib import Path


def boxplot():
    labels = ["Real images",
              "Synthetic images",
              ]

    path = Path("result", "target", "real")
    x_real = []
    for fold in range(5):
        patht = Path(path, str(fold), "metric_test.pickle")
        with open(patht, 'rb') as f:
            x_real += [pickle.load(f)["balanced_accuracy"]]

    path = Path("result", "target", "synth")
    x_synth = []
    for fold in range(5):
        patht = Path(path, str(fold), "metric_test.pickle")
        with open(patht, 'rb') as f:
            x_synth += [pickle.load(f)["balanced_accuracy"]]

    x = [x_real, x_synth]

    save_path = Path("plot", "utility")
    os.makedirs(save_path, exist_ok=True)
    save_path = Path(save_path, "balanced_accuracy.pdf")
    font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 18}

    matplotlib.rc('font', **font)

    plt.boxplot(x, tick_labels=labels)
    plt.ylim([0.5,1])
    plt.ylabel("Balanced accuracy of the \ntarget model")
    #plt.xlabel("Data type")
    plt.savefig(save_path, bbox_inches="tight")

if __name__=="__main__":
    boxplot()
