"""Generate synthetic images with matching labels.
python -m mia_vgg.generate <fold> <task>
"""
from .train_generator import Generator, nz
import torch
import matplotlib.pyplot as plt
import torchvision.utils as vutils
import numpy as np
import sys
import pickle
import os
from pathlib import Path
from tqdm import tqdm
from PIL import Image


ngpu = 0
device = torch.device("cuda:0" if (torch.cuda.is_available() and ngpu > 0) else "cpu")

# Create the generator
netG = Generator(ngpu).to(device)

# Handle multi-GPU if desired
if (device.type == 'cuda') and (ngpu > 1):
    netG = torch.nn.DataParallel(netG, list(range(ngpu)))
fold = int(sys.argv[1])
task = int(sys.argv[2])
netG.load_state_dict(torch.load(f"result/gan/{task}/{fold}/gan_weights", map_location=torch.device(device) ))
netG.eval()


print("Generating images...")
fixed_noise = torch.randn(10000, nz, 1, 1, device=device)
with torch.no_grad():
    gen_lab = torch.randint(0, 2, (10000,))
    fakes = netG(fixed_noise, gen_lab).detach().cpu()
print("Done.")
print("Saving images...")
path_img = Path("data", "synthetic", str(task), str(fold), "images")
os.makedirs(path, exist_ok=True)
path = Path("data", "synthetic", str(task), str(fold), "attribute.csv")
    with open(path, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
    for i,fake in tqdm(enumerate(fakes)):
        writer.writerow([f"{str(i))}.png", gen_lab[i]])
        fake = np.transpose(fake, (1,2,0)).numpy()
        fake = (fake+1)/2*255
        fake = fake.astype(np.uint8)
        im = Image.fromarray(fake, 'RGB')
        im.save(Path(path_img, f"{str(i)}.png"), quality=100, subsampling=0)
    #with open(Path(path, str(i)), 'wb') as f:
    #    pickle.dump(np.transpose(fake, (1,2,0)),f)
print("Done.")


