from os import getenv

import numpy as np
import torch
from torchvision import transforms

IMG_HEIGHT = 224
IMG_WIDTH = 224
NUM_CHANNELS = 3
norm_mean = [0.485, 0.456, 0.406]
norm_std = [0.229, 0.224, 0.225]

MODEL_PATH = getenv("MODEL_PATH")

valid_transform = transforms.Compose(
    [
        transforms.Resize((IMG_HEIGHT, IMG_WIDTH)),
        transforms.ToTensor(),
        transforms.Normalize(norm_mean, norm_std),
    ]
)


model = torch.load(MODEL_PATH, map_location=torch.device("cpu"))
device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")
model.to(device)

model.eval()


def recognize(im):
    im = valid_transform(im)
    np_im = np.array(im)
    np_im = np.array([np_im])
    x = torch.tensor(np_im)
    x = x.to(device)
    # return 1
    with torch.no_grad():
        out = model(x)
        prediction1 = torch.max(out, 1)[1]
        print(prediction1.item())
        return prediction1.item()
