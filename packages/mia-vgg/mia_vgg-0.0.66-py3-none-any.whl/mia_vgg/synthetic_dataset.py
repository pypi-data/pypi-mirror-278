import pickle
import csv
from torchvision.datasets import VisionDataset
from pathlib import Path
import os
import PIL
import numpy as np
import torch

class SyntheticCeleba(VisionDataset):
    def __init__(self, root, target_transform=None, transform=None, no_lab=False):
        super().__init__(root, transform=transform, target_transform=target_transform)
        self._load_filename()
        self.no_lab = no_lab
        if not no_lab:
            self._load_csv()

    def _load_csv(self):
        path = Path(self.root)
        self.attr = np.zeros(len(self))
        with open(Path(path, "attribute.csv")) as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            for i,row in enumerate(reader):
                if row[0]==self.filename[i]:
                    self.attr[i] = int(float(row[1]))
                else:
                    raise ValueError(f"At index {i} filename differ : {row[0]} -- {self.filename[i]}")

    def _load_filename(self):
        path = Path(self.root)
        if os.path.isfile(Path(path, "index_list")):
            self.filename = []
            with open(Path(path, "index_list")) as f:
                for line in f:
                    self.filename += [line[:-1]]
        else:
            self.filename = os.listdir(Path(path, "images"))
            with open(Path(path, "index_list"), 'w') as f:
                for name in self.filename:
                    f.write(name+"\n")

    def __getitem__(self, index):
        X = PIL.Image.open(Path(self.root, 
                                "images", 
                                self.filename[index]))
        if self.transform is not None:
            X = self.transform(X)
        if self.no_lab:
            return X
        else:
            target = torch.tensor(self.attr[index]).type(torch.LongTensor)
            if self.target_transform is not None:
                    target = self.target_transform(target)
            return X, target

    def __len__(self):
        return len(self.filename)
