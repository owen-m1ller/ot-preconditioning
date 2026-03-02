import cv2
import os
import numpy as np

input_directory = "../data/video_frames/jogging"
output_directory = "../data/video_frames/jogging-mask" # saves a mask
history = 30 
dist_threshold = 500.0

backSub = cv2.createBackgroundSubtractorKNN(history=history, dist2Threshold=dist_threshold, detectShadows=False)

os.makedirs(output_directory, exist_ok=True)

frame_files = sorted([f for f in os.listdir(input_directory) if f.endswith('.png')])

for filename in frame_files:
    frame_path = os.path.join(input_directory, filename)
    frame = cv2.imread(frame_path)
    
    if frame is None: continue

    fgMask = backSub.apply(frame)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_OPEN, kernel)
    
    output_path = os.path.join(output_directory, filename)
    cv2.imwrite(output_path, fgMask)