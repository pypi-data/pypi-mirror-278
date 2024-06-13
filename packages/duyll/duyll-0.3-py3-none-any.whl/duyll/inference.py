import numpy as np
import os
import cv2

import torch
import torch.nn as nn
import torch.nn.functional as F
from .download import download_model
from .basicsr.models import create_model
from .basicsr.utils.options import parse
from skimage import img_as_ubyte
from torch.cuda.amp import autocast, GradScaler
download_model()
# Get the user's home directory
home_dir = os.path.expanduser("~")

# Define the .cache directory path
cache_dir = os.path.join(home_dir, ".cache/retouchsota")

# Create the .cache directory if it doesn't exist
os.makedirs(cache_dir, exist_ok=True)

# Define the output path for the downloaded file
model_path = os.path.join(cache_dir, "pytorch_model.pth")
output_path_yml = os.path.join(cache_dir, "model.yml")
def load_img(filepath):
    return cv2.cvtColor(cv2.imread(filepath), cv2.COLOR_BGR2RGB)
def save_img(filepath, img):
    cv2.imwrite(filepath, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
def self_ensemble(x, model):
    def forward_transformed(x, hflip, vflip, rotate, model):
        if hflip:
            x = torch.flip(x, (-2,))
        if vflip:
            x = torch.flip(x, (-1,))
        if rotate:
            x = torch.rot90(x, dims=(-2, -1))
        x = model(x)
        if rotate:
            x = torch.rot90(x, dims=(-2, -1), k=3)
        if vflip:
            x = torch.flip(x, (-1,))
        if hflip:
            x = torch.flip(x, (-2,))
        return x
    t = []
    for hflip in [False, True]:
        for vflip in [False, True]:
            for rot in [False, True]:
                t.append(forward_transformed(x, hflip, vflip, rot, model))
    t = torch.stack(t)
    return torch.mean(t, dim=0)


# Set GPU
gpu_list = ','.join(str(x) for x in '0')
os.environ['CUDA_VISIBLE_DEVICES'] = gpu_list
print('export CUDA_VISIBLE_DEVICES=' + gpu_list)

# Load YAML configuration
opt = parse(output_path_yml, is_train=False)
opt['dist'] = False
print(opt)

# Load model
model_restoration = create_model(opt).net_g
checkpoint = torch.load(model_path)
model_restoration.load_state_dict(checkpoint['params'])
print("===>Testing using weights: ", model_path)
model_restoration.cuda()
model_restoration = nn.DataParallel(model_restoration)
model_restoration.eval()


def process_image(inp_path, model_restoration, out_dir, factor=4):
    torch.cuda.ipc_collect()
    torch.cuda.empty_cache()

    img = np.float32(load_img(inp_path)) / 255.


    # Resize image to have height 1024px while maintaining aspect ratio
    max_height = 1024
    aspect_ratio = img.shape[1] / img.shape[0]
    new_width = int(max_height * aspect_ratio)
    img = cv2.resize(img, (new_width, max_height), interpolation=cv2.INTER_AREA)


    img = torch.from_numpy(img).permute(2, 0, 1)
    input_ = img.unsqueeze(0).cuda()

    # Padding in case images are not multiples of 4
    b, c, h, w = input_.shape
    H, W = ((h + factor) // factor) * factor, ((w + factor) // factor) * factor
    padh = H - h if h % factor != 0 else 0
    padw = W - w if w % factor != 0 else 0
    input_ = F.pad(input_, (0, padw, 0, padh), 'reflect')

    scaler = GradScaler()  # for mixed precision

    with autocast():  # enable mixed precision
        if h < 3000 and w < 3000:
            if 1 == 0:
                restored = self_ensemble(input_, model_restoration)
            else:
                restored = model_restoration(input_)
        else:
            # split and test
            input_1 = input_[:, :, :, 1::2]
            input_2 = input_[:, :, :, 0::2]
            if 1 == 0:
                restored_1 = self_ensemble(input_1, model_restoration)
                restored_2 = self_ensemble(input_2, model_restoration)
            else:
                restored_1 = model_restoration(input_1)
                restored_2 = model_restoration(input_2)
            restored = torch.zeros_like(input_)
            restored[:, :, :, 1::2] = restored_1
            restored[:, :, :, 0::2] = restored_2

        # Unpad images to original dimensions
        restored = restored[:, :, :h, :w]

    restored = torch.clamp(restored, 0, 1).cpu().detach().permute(0, 2, 3, 1).squeeze(0).numpy()


    if True:
       save_img(os.path.join(out_dir, os.path.splitext(os.path.split(inp_path)[-1])[0] + '.png'), img_as_ubyte(restored))


