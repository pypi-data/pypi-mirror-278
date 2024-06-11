import sys
import pickle
import torchvision.transforms as transforms
from torchvision import datasets, models
import torch
from torch.utils.data import DataLoader
import numpy as np
from pathlib import Path

def create_dataset(dtype, fold, task):
    """Create a dataset for AIA. 
    The dataste contains soft labels and yhat to infer the attribute defined in the task argument. 
    This attribute is the choosen sensitive attribute.

    :param dtype: Choose a target model trained on real (\"real\") or synthetic (\"synth\")data.
    :type dtype: string
    :param fold: Crosse validation step.
    :type fold: int<=4
    :param task: Sensitive attribute.
    :type task: int<=39
    """

    class Trgtsf:
        def __init__(self, task):
            """Transform a target.
            :param t: Target vector.
            :type t: Vector of size 40
            """
            self.task = task

        def __call__(self, t):
            return t[self.task]

    image_size = 64
    batch_size = 100
    transform=transforms.Compose([
       transforms.Resize(image_size),
       transforms.CenterCrop(image_size),
       transforms.ToTensor(),
       transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
       ])

    ngpu = 0
    device = torch.device("cuda:0" if (torch.cuda.is_available() and ngpu > 0) else "cpu")

    trgtsf = Trgtsf(task)
    celeba = datasets.CelebA(root="data", download=True, target_transform=trgtsf, transform=transform, split="all")
    model = models.vgg16()
    num_ftrs = model.classifier[len(model.classifier)-1].in_features
    model.classifier[len(model.classifier)-1] = torch.nn.Linear(num_ftrs, 2)
    if (device.type == 'cuda') and (ngpu > 1):
        model = torch.nn.DataParallel(model, list(range(ngpu)))
    model.load_state_dict(torch.load(f"result/target/{dtype}/{fold}/target_weights", map_location=torch.device(device) ))
    model.eval()

    
    with open(Path("data", "splits", str(fold), "test.pickle"), 'rb') as f:
        test_ids = pickle.load(f)
    test_subsampler = torch.utils.data.SubsetRandomSampler(test_ids)
    loader = DataLoader(celeba, batch_size=batch_size, sampler=test_subsampler)
    N = len(test_ids)
    nombre_batch = 1

    aia_size = min(batch_size*nombre_batch, N)
    aia = {"s":np.zeros(N).astype(float),
           "yhat":np.zeros(N).astype(float),
           "soft":np.zeros((N,2)).astype(float),
            }

    index = 0
    with torch.no_grad():
        for i,(x,s) in enumerate(loader):
            s = s.cpu().detach().numpy()
            soft = model(x)
            _, yhat = torch.max(soft, 1)
            soft = soft.cpu().detach().numpy()
            yhat = yhat.cpu().detach().numpy()

            for j,ss in enumerate(s):
                if index >aia_size:
                    break
                else:
                    aia["s"][index] = ss
                    aia["yhat"][index] = yhat[j]
                    aia["soft"][index] = soft[j]
                    index += 1
            if index >aia_size:
                break

    path = Path("result", "target", dtype, str(fold), "aia.pickle")
    with open(path, 'wb') as f:
        pickle.dump(aia, f)


if __name__=="__main__":
    dtype = sys.argv[1]
    fold = int(sys.argv[2])
    task = int(sys.argv[3])
    print(f"dtype:{dtype} fold:{fold} task:{task}")
    create_dataset(dtype, fold, task)


