from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
import pickle
import matplotlib.pyplot as plt
import numpy as np
import sys
from tqdm import tqdm
import os

def shuffle(data):
    """Shuffle dictionary of numpy array."""
    n = len(data[list(data.keys())[0]])
    idx = np.arange(n)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    for key in data.keys():
        data[key] = data[key][idx]
    return data


def split(data,k=0):
    """5-folding of dataset dictionary of numpy array.

    :param data: Dataset where each key maps to a numpy array.
    :type data: Dictionary
    :param k: (Optional) Indice of the fold, can be 0,1,2,3 or 4.
    :type k: int 
    :return: Dataset with train and test.
    :rtype: Dictionary
    """
    keys = list(data.keys())
    n = np.shape(data[keys[0]])[0]
    idx = np.linspace(0,n-1,n).astype(int)
    test = (idx[int(k*0.2*(n))]<=idx)&(idx<=idx[int((k+1)*0.2*(n-1))])
    train = ~test
    data_split = {"train":{},"test":{}}
    for key in keys:
        data_split["train"][key] = data[key][train]
        data_split["test"][key] = data[key][test]

    return data_split["train"],data_split["test"]
 
def mia(fold, dtype, task):
    path = Path("result", str(task), "target", dtype, str(fold), "mia.pickle")
    with open(path, 'rb') as f:
        data = pickle.load(f)
    data = shuffle(data)
    ba = []
    #print(len(data["loss"]))
    for k in range(5):
        train, test = split(data)
        clf = RandomForestClassifier()
        #clf.fit(train["loss"].reshape(-1,1), train["member"])
        x = np.concatenate([train["loss"].reshape(-1,1), train["soft"], train["y"].reshape(-1,1)], axis=1)
        clf.fit(x, train["member"])
        x = np.concatenate([test["loss"].reshape(-1,1), test["soft"], test["y"].reshape(-1,1)], axis=1)
        member_hat = clf.predict(x)
        member = test["member"]
        #print(np.unique(member))
        balanced_accuracy = np.mean([np.mean(member_hat[member==m]==m) for m in np.unique(member)])
        ba += [balanced_accuracy]
        #print(balanced_accuracy)

        #plt.plot(data["loss"], data["member"], 'bo')
        #plt.show()

    return ba

if __name__=="__main__":
    task = int(sys.argv[1])
    path = Path("result", "mia")

    for dtype in ["real", "synth"]:
        ba = []
        for fold in tqdm(range(5)):
            for k in range(10):
                ba += mia(fold, dtype)
        os.makedirs(Path(path, dtype), exist_ok=True)
        with open(Path(path, dtype, "balanced_accuracy.pickle"), 'wb') as f:
            pickle.dump(ba, f)
