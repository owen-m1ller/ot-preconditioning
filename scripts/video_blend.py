import torch
import ot
import numpy as np
from PIL import Image
import os
import glob

WIDTH = 160
HEIGHT = 120
REG_VAL = .01

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Running on: {device}")

def load_image_gpu(path, size=(WIDTH, HEIGHT)):
    img = Image.open(path).convert('L')
    img = img.resize(size)
    

    img_array = np.array(img, dtype=np.float64)
    t_img = torch.tensor(img_array, dtype=torch.float64, device=device)
    
    corners = torch.cat([t_img[0,0:5], t_img[0,-5:], t_img[-1,0:5], t_img[-1,-5:]])
    bg_color = torch.median(corners)
    
    t_img = torch.abs(t_img - bg_color)
    
    if torch.sum(t_img) > 0:
        t_img = t_img / torch.sum(t_img)
    
    return t_img.flatten()

    
def get_cost_matrix_gpu(width, height):
    x = torch.arange(width, dtype=torch.float64, device=device)
    y = torch.arange(height, dtype=torch.float64, device=device)
    
    Y, X = torch.meshgrid(y, x, indexing='ij') 
    
    coords = torch.stack((X.flatten(), Y.flatten()), dim=1)
    
    M = torch.cdist(coords, coords, p=2) ** 2
    M = M / M.max()
    return M

def save_ot_interpolated_image(gamma, t, output_path, size=(WIDTH, HEIGHT)):
    width, height = size
    
    nx = torch.arange(width, dtype=torch.float64, device=gamma.device)
    ny = torch.arange(height, dtype=torch.float64, device=gamma.device)
    grid_y, grid_x = torch.meshgrid(ny, nx, indexing='ij')
    coords = torch.stack((grid_x.flatten(), grid_y.flatten()), dim=1)

    threshold = gamma.max() * 1e-4 
    active_indices = torch.nonzero(gamma > threshold, as_tuple=True)
    
    source_idx = active_indices[0]
    target_idx = active_indices[1]
    weights = gamma[source_idx, target_idx]

    start_pos = coords[source_idx]
    end_pos = coords[target_idx]
    
    interp_pos = (1 - t) * start_pos + t * end_pos

    # bilinear splatting
    x0 = interp_pos[:, 0].floor().long()
    y0 = interp_pos[:, 1].floor().long()
    
    x0 = x0.clamp(0, width - 2)
    y0 = y0.clamp(0, height - 2)
    
    dx = interp_pos[:, 0] - x0
    dy = interp_pos[:, 1] - y0
    
    idx_TL = y0 * width + x0
    idx_TR = y0 * width + (x0 + 1)
    idx_BL = (y0 + 1) * width + x0
    idx_BR = (y0 + 1) * width + (x0 + 1)
    
    new_img = torch.zeros(width * height, dtype=torch.float64, device=gamma.device)
    
    new_img.index_add_(0, idx_TL, weights * (1 - dx) * (1 - dy))
    new_img.index_add_(0, idx_TR, weights * dx * (1 - dy))
    new_img.index_add_(0, idx_BL, weights * (1 - dx) * dy)
    new_img.index_add_(0, idx_BR, weights * dx * dy)

    result = new_img.reshape(height, width).cpu().numpy()
    
    if result.max() > 0:
        result = result / result.max()

    result = 1.0 - result
    
    img_out = (result * 255).clip(0, 255).astype(np.uint8)
    Image.fromarray(img_out).save(output_path)

M_gpu = get_cost_matrix_gpu(WIDTH, HEIGHT)


start_frame = 30

for i in range(1, 51): # set the range to interpolate over here
    t = 0
    t = .02 * i
    i = i + 30

    path1 = f"../data/video_frames/masked_walking/frame_{i:04d}.png" # starting frame for video 1
    path2 = f"../data/video_frames/masked-jogging/frame_{i:04d}.png" # starting frame for video 2

    d1 = load_image_gpu(path1, size=(WIDTH, HEIGHT))
    d2 = load_image_gpu(path2, size=(WIDTH, HEIGHT))

    gamma = ot.emd(d1, d2, M=M_gpu)

    save_ot_interpolated_image(gamma, t, f"output_gpu/frame_{i:04d}.png", size=(WIDTH, HEIGHT))
