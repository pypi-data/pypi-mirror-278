import pickle
import matplotlib.pyplot as plt
from pathlib import Path

def plot():
    for fold in range(5):
        color = {"Real images":"blue",
                 "Synthetic images":"orange",
                 }
        path = Path("result", "target", "real", str(fold), "loss.pickle")
        with open(path, "rb") as f:
            loss = pickle.load(f)
        if fold == 0:
            plt.plot(loss, color[fold], label="")

    plt.legend()
