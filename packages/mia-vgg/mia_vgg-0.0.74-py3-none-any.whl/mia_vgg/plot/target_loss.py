import pickle
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
import os

def plot():
    font = {'family' : 'serif',
            'weight' : 'normal',
            'size'   : 18}
    matplotlib.rc('font', **font)
    color = {"real":"blue",
             "synth":"orange",
             }
    lab = {"real":"Real images",
           "synth":"Synthetic images",
           }
    for fold in range(5):
        for dtype in ["real", "synth"]:
            path = Path("result", "target", dtype, str(fold), "loss_train.pickle")
            with open(path, "rb") as f:
                loss = pickle.load(f)
            if fold == 0:
                plt.plot(loss, color[dtype], label=lab[dtype])
            else:
                plt.plot(loss, color[dtype])
    plt.legend()
    plt.ylabel("Loss")
    plt.xlabel("SGD step")
    save_path = Path("plot", "loss")
    os.makedirs(save_path, exist_ok=True)
    save_path = Path(save_path, "target_loss.pdf")
    plt.savefig(save_path, bbox_inches="tight")

if __name__=="__main__":
    plot()
