"""Generate cross validation idx."""
from sklearn.model_selection import KFold
import torch.utils.data
import torchvision.datasets as dset
import torchvision.transforms as transforms
import os
import pickle
from pathlib import Path

if __name__=="__main__":
    dataroot = "data/celeba"
    image_size = 64
    celeba = dset.ImageFolder(root=dataroot,
                               transform=transforms.Compose([
                                   transforms.Resize(image_size),
                                   transforms.CenterCrop(image_size),
                                   transforms.ToTensor(),
                                   transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
                               ]))

    kf = KFold(shuffle=True, n_splits=5, random_state=1)
    path = Path("data", "splits")
    for fold, (train_ids, test_ids) in enumerate(kf.split(celeba)):
        patht = Path(path,str(fold)) 
        os.makedirs(patht, exist_ok=True)
        with open(Path(patht,"train.pickle"), 'wb') as f:
            pickle.dump(train_ids,f)
        with open(Path(patht,"test.pickle"), 'wb') as f:
            pickle.dump(test_ids,f)
