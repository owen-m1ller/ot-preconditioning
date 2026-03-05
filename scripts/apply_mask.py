import cv2
import os
import numpy as np

input_directory = "../data/video_frames/jogging" 
mask_directory = "../data/video_frames/jogging-mask"
output_directory = "../data/video_frames/masked-jogging"

os.makedirs(output_directory, exist_ok=True)

frames = sorted([f for f in os.listdir(input_directory) if f.endswith('.png')])

for filename in frames:
    original = cv2.imread(os.path.join(input_directory, filename), cv2.IMREAD_GRAYSCALE)
    mask = cv2.imread(os.path.join(mask_directory, filename), cv2.IMREAD_GRAYSCALE)
    
    if original is None or mask is None: continue
    
    masked_img = cv2.bitwise_and(original, original, mask=mask)
    masked_img[mask == 0] = 255
    
    cv2.imwrite(os.path.join(output_directory, filename), masked_img)
    print(f"Masked: {filename}")