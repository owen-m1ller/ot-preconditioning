import ot
import numpy as np
import cv2
from sklearn.neighbors import KNeighborsRegressor
import time

def color_transfer_ab(style_img, content_img, n_samples=2000):

    s_lab = cv2.cvtColor(style_img, cv2.COLOR_BGR2LAB).astype(np.float32)
    c_lab = cv2.cvtColor(content_img, cv2.COLOR_BGR2LAB).astype(np.float32)

    s_ab = s_lab[:, :, 1:].reshape(-1, 2)
    c_ab = c_lab[:, :, 1:].reshape(-1, 2)

    np.random.seed(2)
    
    n_samples = min(n_samples, s_ab.shape[0], c_ab.shape[0])
    
    idx_s = np.random.choice(s_ab.shape[0], n_samples, replace=False)
    idx_c = np.random.choice(c_ab.shape[0], n_samples, replace=False)
    
    s_batch = s_ab[idx_s]
    c_batch = c_ab[idx_c]

    M = ot.dist(c_batch, s_batch, metric='sqeuclidean')
    
    M = M / M.max()
    
    reg = 0.05
    ot_time_st = time.perf_counter()

    plan = ot.sinkhorn(np.ones(n_samples)/n_samples, np.ones(n_samples)/n_samples, M, reg)
    
    mapped_batch = (plan @ s_batch) * n_samples

    ot_time_end = time.perf_counter()

    ot_time = ot_time_end - ot_time_st

    print(f"ot time: {ot_time:.4f}")

    knn_train_st = time.perf_counter()

    # knn = KNeighborsRegressor(n_neighbors=10, weights='distance', n_jobs=-1)

    knn = KNeighborsRegressor(n_neighbors=10, weights='distance')

    knn.fit(c_batch, mapped_batch)

    knn_train_end = time.perf_counter()

    knn_time = knn_train_end - knn_train_st
    
    print(f"knn train time: {knn_time:.4f}")

    knn_pred_st = time.perf_counter()

    pred_ab = knn.predict(c_ab)

    knn_pred_end = time.perf_counter()

    knn_pred_time = knn_pred_end - knn_pred_st
    
    print(f"knn inference time: {knn_pred_time:.4f}")

    h, w, _ = c_lab.shape
    pred_ab_img = pred_ab.reshape(h, w, 2)
    
    original_l = c_lab[:, :, 0]
    
    result_lab = np.dstack([original_l, pred_ab_img])
    
    result_lab = np.clip(result_lab, 0, 255).astype(np.uint8)
    
    return cv2.cvtColor(result_lab, cv2.COLOR_LAB2BGR)

if __name__ == "__main__":
    style = cv2.imread("for-lake.jpg")
    start_time = time.perf_counter()
    
    for i in range(312):
        path = f"for-light/frame_{i + 1:04d}.png"
        content = cv2.imread(path)
        
        if content is None: continue
            
        out = color_transfer_ab(style, content)
        
        cv2.imwrite(f'vid-out/frame_{i+1:04d}.png', out)
        print(f"frame {i+1} completed")
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    print(f"Execution time: {elapsed:.4f} seconds")
