import warnings
from os import getenv

import numpy as np
import torch
from torch.serialization import SourceChangeWarning
from torchvision import transforms

warnings.filterwarnings("ignore", category=SourceChangeWarning)

IMG_HEIGHT = 224
IMG_WIDTH = 224
NUM_CHANNELS = 3
NORM_MEAN = [0.485, 0.456, 0.406]
NORM_STD = [0.229, 0.224, 0.225]
MODEL_PATH = getenv("MODEL_PATH")
LABELS = ["细菌性斑点病", "早疫病", "晚疫病", "叶霉病", "斑枯病", "二斑叶螨病", "轮斑病", "花叶病", "黄曲叶病", "健康"]

valid_transform = transforms.Compose(
    [
        transforms.Resize((IMG_HEIGHT, IMG_WIDTH)),
        transforms.ToTensor(),
        transforms.Normalize(NORM_MEAN, NORM_STD),
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
    with torch.no_grad():
        out = model(x)
        values, indices = torch.sort(out[0], descending=True)
        result = []
        for value, indice in zip(values, indices):
            result.append((indice.item(), LABELS[indice], value.item()))
        return result
