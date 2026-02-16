#!/bin/bash

# NOTE: only run this script from the scripts directory

# clear the data directory

# install images

image_names=("cow-icon.png" "dragon-icon.png" "forest-lake.jpg" "forest.jpg" "lakes-sunset.jpg" "mountains.png")
image_path="data/images"

for item in "${image_names[@]}"; do
    curl https://pub-753cbd3506414678a87262edde600418.r2.dev/$image_path/$item -o ../$image_path/$item
done

# install videos and extract them into frames

video_names=("forest-light.mp4" "jogging.mp4" "walking.mp4" "library.mp4" "waterfall.mp4")
video_path="data/raw_video"
frames_path="data/video_frames"

for item in "${video_names[@]}"; do
    curl https://pub-753cbd3506414678a87262edde600418.r2.dev/$video_path/$item -o ../$video_path/$item
    ffmpeg -i ../$video_path/$item ../$frames_path/${item%.*}/frame_%04d.png
done

# install image subfolders


image_path="data/images/blue"

for i in {1..20}; do
    curl https://pub-753cbd3506414678a87262edde600418.r2.dev/$image_path/$i.jpg -o ../$image_path/$i.jpg
done

image_path="data/images/few"

for i in {1..10}; do
    curl https://pub-753cbd3506414678a87262edde600418.r2.dev/$image_path/$i.jpg -o ../$image_path/$i.jpg
done

image_path="data/images/many"

for i in {1..10}; do
    curl https://pub-753cbd3506414678a87262edde600418.r2.dev/$image_path/$i.jpg -o ../$image_path/$i.jpg
done

image_path="data/images/red"

for i in {1..10}; do
    curl https://pub-753cbd3506414678a87262edde600418.r2.dev/$image_path/$i.jpg -o ../$image_path/$i.jpg
done

image_names=("day_ocean.jpg" "nion.jpg" "ocean_day.jpg" "ocean_sunset.jpg" "red_leaf.jpg")
image_path="data/images/images"
for item in "${image_names[@]}"; do
    curl https://pub-753cbd3506414678a87262edde600418.r2.dev/$image_path/$item -o ../$image_path/$item
done
