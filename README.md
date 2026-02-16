# Introduction

This project explores preconditioning methods for finding optimal transport maps. We focus on applications for video editing: color transfer and image/video blending.

# Organization

```
├── pixi.toml              # holds the list of dependencies for the project
├── pixi.lock              # an exact recursive record of all Python libraries used in the project
└── scripts                # scripts for setup and optimal transport methods. allows you to try our methods from the CLI.
└── data                   # pulled from cloudflare R2 instance using scripts/data_install.sh
│  └── images              # png files to test color transfer on 
│  └── raw_videos          # mp4 files of videos used 
│  └── video_frames        # folders of frames for each video listed in raw_videos
│  │  └── forest_light     # contains frames for the forest_light video
│  │  │  ├── frame_0001.png
│  │  │  ├── ...
│  │  └── waterfall        # contains frames for the waterfall video
│  │  └── ...              # folders of frames for other videos
└── notebooks              # ipynbs walking through an entire example pipeline
└── output-frames          # a folder for output frames after running a video-processing script
└── output                 # a folder for you to store mp4 videos (built from the frames in output-frames) or output images in
```

# Getting Started
