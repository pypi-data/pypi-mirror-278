import pickle
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from tqdm import tqdm
import numpy as np
import os

from .mia import shuffle, split

def aia(fold, dtype):
    with open(Path("result", "target", dtype, str(fold), "aia.pickle"), 'rb') as f:
        data = pickle.load(f)
    data = shuffle(data)
    ba = []
    for k in range(5):
        train, test = split(data)
        clf = RandomForestClassifier()
        clf.fit(train["soft"], train["s"])

        s_hat = clf.predict(test["soft"])
        s = test["s"]
        balanced_accuracy = np.mean([np.mean(s_hat[s==ss]==ss) for ss in np.unique(s)])
        ba += [balanced_accuracy]
    return ba

if __name__=="__main__":
    path = Path("result", "aia")
    for dtype in ["real", "synth"]:
        ba = []
        for fold in tqdm(range(5)):
            for k in tqdm(range(100)):
                ba += aia(fold, dtype)
        os.makedirs(Path(path, dtype), exist_ok=True)
        with open(Path(path, dtype, "balanced_accuracy.pickle"), 'wb') as f:
            pickle.dump(ba, f)
