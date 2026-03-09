import numpy as np
from PIL import Image
import os

SIZE = (160, 120)

def load_image_linear(path):
    try:
        img = Image.open(path).convert("RGBA")
        
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(bg, img).convert("L")
        img = img.resize(SIZE)
        
        arr = np.array(img, dtype=np.float64) / 255.0
        return arr
    except Exception:
        return None

def save_frame(arr, path):
    arr = np.clip(arr * 255.0, 0, 255).astype(np.uint8)
    Image.fromarray(arr).save(path)

os.makedirs("output_linear", exist_ok=True)
print("Starting Linear Cross-Dissolve...")

t = 0
for i in range(31, 51):
    path1 = f"../data/video_frames/masked_walking/frame_{i:04d}.png" # images to fade between
    path2 = f"../data/video_frames/masked-jogging/frame_{i:04d}.png"
    
    if not os.path.exists(path1): break
    
    img1 = load_image_linear(path1)
    img2 = load_image_linear(path2)
    
    t += .02
    
    result = (1 - t) * img1 + t * img2
    
    save_frame(result, f"output_linear/frame{i:04d}.png")
    
    if i % 5 == 0: print(f"Frame {i} done")
