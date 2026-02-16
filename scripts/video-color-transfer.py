import ot
import numpy as np
import cv2
from sklearn.neighbors import KNeighborsRegressor
import time
import os
import sys

def train_color_transfer(style_img, content_img, n_samples=2000):
    
    s_lab = cv2.cvtColor(style_img, cv2.COLOR_BGR2LAB).astype(np.float32)
    c_lab = cv2.cvtColor(content_img, cv2.COLOR_BGR2LAB).astype(np.float32)

    s_ab = s_lab[:, :, 1:].reshape(-1, 2)
    c_ab = c_lab[:, :, 1:].reshape(-1, 2)
    
    np.random.seed(42)
    idx_s = np.random.choice(s_ab.shape[0], n_samples, replace=False)
    idx_c = np.random.choice(c_ab.shape[0], n_samples, replace=False)
    
    s_batch = s_ab[idx_s]
    c_batch = c_ab[idx_c]

    M = ot.dist(c_batch, s_batch, metric='sqeuclidean')
    M /= M.max()
    
    reg = 0.05
    plan = ot.sinkhorn(np.ones(n_samples)/n_samples, np.ones(n_samples)/n_samples, M, reg)
    
    mapped_batch = (plan @ s_batch) * n_samples

    knn = KNeighborsRegressor(n_neighbors=10, weights='distance', n_jobs=-1)
    knn.fit(c_batch, mapped_batch)
    
    return knn

def apply_map(img, knn, lut_size=33):

    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
    h, w, _ = img_lab.shape
    
    L_channel = img_lab[:, :, 0]
    ab_channel = img_lab[:, :, 1:]
    
    ab_flat = ab_channel.reshape(-1, 2)
    
    pred_ab = knn.predict(ab_flat)
    
    pred_lab = np.zeros_like(img_lab)
    pred_lab[:, :, 0] = L_channel
    pred_lab[:, :, 1:] = pred_ab.reshape(h, w, 2)
    
    pred_lab = np.clip(pred_lab, 0, 255).astype(np.uint8)
    return cv2.cvtColor(pred_lab, cv2.COLOR_LAB2BGR)

if __name__ == "__main__":
    start_time = time.perf_counter()

    style = sys.argv[1]   # path to reference
    content_folder = sys.argv[2] # path to content folder

    target_frame1 = sys.argv[2]
    if sys.argv[3]:
        n_samples = sys.argv[3]
    else:
        n_samples = 2000

    n_frames = -1 # to account for the gitkeep file
    with os.scandir(content_folder) as files:
        for file in files:
            if file.is_file():
                n_frames += 1

    frame1_path = content_folder + "frame_0001.png"
    knn = train_color_transfer(style, cv2.imread(frame1_path), n_samples)
    
    for i in range(n_frames):
        path = f"wf_frames/frame_{i + 1:04d}.png"
        content = cv2.imread(path)
                    
        out = apply_map(content, knn)
        cv2.imwrite(f'vid-out/frame_{i+1:04d}.png', out)
        print(f"frame {i+1} completed")

    end_time = time.perf_counter()
    elapsed = end_time - start_time
    print(f"Execution time: {elapsed:.4f} seconds")
