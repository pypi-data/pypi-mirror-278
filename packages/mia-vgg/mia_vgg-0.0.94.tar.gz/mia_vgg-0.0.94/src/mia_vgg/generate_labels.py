import sys
import torch
from torchvision import models
import torchvision.transforms as transforms
import torchvision.datasets as dset
import matplotlib.pyplot as plt
import numpy as np
import csv
from pathlib import Path
from tqdm import tqdm

from .synthetic_dataset import SyntheticCeleba

fold = sys.argv[1]
image_size = 64
transform=transforms.Compose([
   transforms.Resize(image_size),
   transforms.CenterCrop(image_size),
   transforms.ToTensor(),
   transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
   ])
dataroot = f"data/synthetic/{fold}"

celeba = SyntheticCeleba(root=dataroot,
                         transform=transform,
                         no_lab=True,
                         )
trainloader = torch.utils.data.DataLoader(celeba, batch_size=100)

ngpu = 0
device = torch.device("cuda:0" if (torch.cuda.is_available() and ngpu > 0) else "cpu")

model = models.vgg16()
num_ftrs = model.classifier[len(model.classifier)-1].in_features
model.classifier[len(model.classifier)-1] = torch.nn.Linear(num_ftrs, 2)
if (device.type == 'cuda') and (ngpu > 1):
    model = torch.nn.DataParallel(model, list(range(ngpu)))
model.load_state_dict(torch.load(f"result/target/real/{fold}/target_weights", map_location=torch.device(device) ))
model.eval()

labels = np.empty(0)
with torch.no_grad():
    print("Generating labels")
    for i,data in tqdm(enumerate(trainloader)):
        soft = model(data)
        _, yhat = torch.max(soft, 1)
        yhat = yhat.cpu().detach().numpy()
        labels = np.concatenate([labels, yhat])

path = Path("data", "synthetic", str(fold), "attribute.csv")
with open(path, "w") as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    print("Writing csv file")
    for i,yy in tqdm(enumerate(labels)):
        writer.writerow([celeba.filename[i],yy])
