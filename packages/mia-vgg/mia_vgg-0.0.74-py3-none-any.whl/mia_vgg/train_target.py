"""In this module we use pytorch to train vgg16 on celebA."""

from torchvision import datasets, models
import matplotlib.pyplot as plt
from torch import nn
from torch.utils.data import random_split, DataLoader
import torch.optim as optim
from torchvision.transforms import PILToTensor, v2
import torch
import numpy as np
import os
import sys
from pathlib import Path
import pickle
from tqdm import tqdm
import torchvision.datasets as dset
import torchvision.transforms as transforms

from .synthetic_dataset import SyntheticCeleba


class Trgtsf:
    def __init__(self, task):
        """Transform a target.
        :param t: Target vector.
        :type t: Vector of size 40
        """
        self.task = task

    def __call__(self, t):
        return t[self.task]

def train(task, fold, dtype):
    """Train VGG16. Evaluate on 20% unseen data. Create a mia dataset of loss with member and non-member labeled.
    :param task: Classification task.
    :type task: int <= 40
    :fold: cross Validation step.
    :type fold: int <= 4
    :dtype: Use real or synthetic data.
    :type dtype: string "real" or "synth" """

    if not dtype in ["real", "synth"]:
        raise ValueError(f"Unknown dtype {dtype}, should be either \"real\" or \"synth\".")

   # transform = v2.Compose([PILToTensor(),
   #                        v2.ToDtype(torch.float32, scale=True)])
    image_size = 64
    batch_size = 100
    transform=transforms.Compose([
       transforms.Resize(image_size),
       transforms.CenterCrop(image_size),
       transforms.ToTensor(),
       transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
       ])
    
    trgtsf = Trgtsf(task)
    celeba = datasets.CelebA(root="data", download=True, target_transform=trgtsf, transform=transform, split="all")
    path = Path("data", "splits", str(fold))
    if dtype == "real":
        trgtsf = Trgtsf(task)
        with open(Path(path, "train.pickle"), 'rb') as f:
            train_ids = pickle.load(f)
        train_subsampler = torch.utils.data.SubsetRandomSampler(train_ids)
        trainloader = DataLoader(celeba, batch_size=batch_size, sampler=train_subsampler)

    if dtype == "synth":
        data = SyntheticCeleba(root=f"data/synthetic/{fold}", transform=transform)
        trainloader = DataLoader(data, batch_size=batch_size)


    with open(Path(path, "test.pickle"), 'rb') as f:
        test_ids = pickle.load(f)
    test_subsampler = torch.utils.data.SubsetRandomSampler(test_ids)
    testloader = DataLoader(celeba, batch_size=batch_size, sampler=test_subsampler)


    weights = models.VGG16_Weights
    model = models.vgg16(weights=weights)

    num_ftrs = model.classifier[len(model.classifier)-1].in_features

    model.classifier[len(model.classifier)-1] = nn.Linear(num_ftrs, 2)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    nombre_batch = 5
    epochs = 10
    loss_train = np.zeros(epochs).astype(float)
    for epoch in range(epochs):
        running_loss = 0
        for i,data in enumerate(trainloader):
            optimizer.zero_grad()
            x,y = data
            x = x.to(device)
            y = y.to(device)
            soft = model(x)
            loss = criterion(soft, y)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            if i>nombre_batch:
                break
        loss_train[epoch] = running_loss/nombre_batch

    path = Path("result", str(task), "target", dtype, str(fold))
    os.makedirs(path, exist_ok=True)
    with open(Path(path, "loss_train.pickle"), 'wb') as f:
        pickle.dump(loss_train, f)

    
    #Save trained model
    torch.save(model.state_dict(), f"result/target/{dtype}/{fold}/target_weights")

    #Evaluate on training set 
    values = {"y":np.empty(0), "yhat":np.empty(0)}
    with torch.no_grad():
        for i, data in enumerate(trainloader):
            x,y = data
            x = x.to(device)
            y = y.to(device)
            soft = model(x)
            loss = criterion(soft, y)
            _, yhat = torch.max(soft, 1)
            yhat = yhat.cpu().detach().numpy()
            y = y.cpu().detach().numpy()
            values["y"] = np.append(values["y"], y)
            values["yhat"] = np.append(values["yhat"], yhat)

            if i>nombre_batch:
                break

    y = values["y"]
    yhat = values["yhat"]
    metric = {}
    metric["accuracy"] = np.mean(y==yhat)
    metric["balanced_accuracy"] = np.mean([np.mean(yhat[y==yy]==yy) for yy in np.unique(y)])

    with open(Path(path, "metric_train.pickle"), 'wb') as f:
        pickle.dump(metric, f)


    #Evaluation on real data training set
    mia_size = min(batch_size*nombre_batch, int(0.2*len(celeba)))
    mia = {"loss":np.zeros(mia_size).astype(float),
           "soft":np.zeros([mia_size,2]).astype(float),
           "y":np.zeros(mia_size),
           "member":np.zeros(mia_size),
           }
    half = int(mia_size/2)
    mia["member"][:half] = 1
    index = 0
    #Compute loss 
    criterion = nn.CrossEntropyLoss(reduction='none')
    values = {"y":np.empty(0), "yhat":np.empty(0)}

    trgtsf = Trgtsf(task)
    splpath = Path("data", "splits", str(fold))
    with open(Path(splpath, "train.pickle"), 'rb') as f:
        train_ids = pickle.load(f)
    train_subsampler = torch.utils.data.SubsetRandomSampler(train_ids)
    trainloader = DataLoader(celeba, batch_size=batch_size, sampler=train_subsampler)

    with torch.no_grad():
        for i, data in enumerate(trainloader):
            x,y = data
            x = x.to(device)
            y = y.to(device)
            soft = model(x)
            loss = criterion(soft, y)
            _, yhat = torch.max(soft, 1)
            yhat = yhat.cpu().detach().numpy()
            y = y.cpu().detach().numpy()
            values["y"] = np.append(values["y"], y)
            values["yhat"] = np.append(values["yhat"], yhat)
            soft = soft.cpu().detach().numpy()
            loss = loss.cpu().detach().numpy()
            for j in range(len(loss)):
                if index > half-1:
                    break
                else:
                    mia["loss"][index] = loss[j]
                    mia["soft"][index] = soft[j]
                    mia["y"][index] = y[j]
                index += 1
            if index > half-1:
                break

    y = values["y"]
    yhat = values["yhat"]
    metric = {}
    metric["accuracy"] = np.mean(y==yhat)
    metric["balanced_accuracy"] = np.mean([np.mean(yhat[y==yy]==yy) for yy in np.unique(y)])

    with open(Path(path, "metric_real_train.pickle"), 'wb') as f:
        pickle.dump(metric, f)
                

    #Evaluation on real data testing set
    with torch.no_grad():
        values = {"y":np.empty(0), "yhat":np.empty(0)}
        for i, data in enumerate(testloader):
            x,y = data
            x = x.to(device)
            y = y.to(device)
            soft = model(x)
            _, yhat = torch.max(soft, 1)
            loss = criterion(soft, y)
            y = y.cpu().detach().numpy()
            yhat = yhat.cpu().detach().numpy()
            values["y"] = np.append(values["y"], y)
            values["yhat"] = np.append(values["yhat"], yhat)
            soft = soft.cpu().detach().numpy()
            loss = loss.cpu().detach().numpy()

            for j in range(len(loss)):
                index += 1
                if index > mia_size-1:
                    break
                else:
                    mia["loss"][index] = loss[j]
                    mia["soft"][index] = soft[j]
                    mia["y"][index] = y[j]
            if index > mia_size-1:
                break


        y = values["y"]
        yhat = values["yhat"]
    metric = {}
    metric["accuracy"] = np.mean(y==yhat)
    metric["balanced_accuracy"] = np.mean([np.mean(yhat[y==yy]==yy) for yy in np.unique(y)])

    with open(Path(path, "metric_test.pickle"), 'wb') as f:
        pickle.dump(metric, f)
    with open(Path(path, "values.pickle"), 'wb') as f:
        pickle.dump(values, f)
    with open(Path(path, "mia.pickle"), 'wb') as f:
        pickle.dump(mia, f)

        
if __name__=="__main__":
    #for task in range(40):
    #    train(task)
    #    print(f"{task} done")

    
    task = int(sys.argv[3])
    fold = int(sys.argv[1])
    dtype = sys.argv[2]

    print(f"fold={fold} dtype={dtype}")
    train(task, fold, dtype)
