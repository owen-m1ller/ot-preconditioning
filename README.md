# Introduction

This project explores preconditioning methods for finding optimal transport maps. We focus on applications for video editing: color transfer and image/video blending.

## Optimal transport primer

Optimal Transport is a study of trying to measure the difference in probability distributions $\mu$ and $\nu$ (we can 
imagine this as moving a sand pile on the beach and trying to transform it into a castle with minimum 'effort'):

$$
\inf_{T: T_{\\#}\mu = \nu} \int \left| T(x) - x \right| \mu d(x).
$$

The solution to the problem above is exactly the Wasserstein distance between the distibutions $\mu$ and $\nu$:

$$
W_p(\mu, \nu) = \inf_{\gamma \in \Gamma(\mu, \nu)} (\mathbb{E}_{(x, y) \sim \gamma} d(x, y)^p)^{1/p},
$$

where $\Gamma(\mu, \nu)$ is the set of all couplings between the two distributions $\mu$ and $\nu$. 
This is convenient when training point clouds, since we can model data representations in different times as discrete 
probability distributions evolving through time.
Often with real data, we are working in the space $\mathbb{R}^d$, and hence we can use the Euclidean norm as our distance 
metric in the Wasserstein distance:

$$
d(x, y) = \left| x - y \right|_2.
$$

Normally, finding the Wasserstein distance between two probability distributions $\mu$ and $\nu$ above is computationally 
expensive, but there are numerous results which could dramatically reduce the computational complexity (such as entropic 
regularization). We explore supplementary preprocessing steps to speed up the steps for creating a plan in this project.

## Optimal transport for color transfer

In the context of color transfer, the two probability distributions we are finding a coupling between are the distributions of color in each image.
For example, each pixel can be thought of a point in $\mathbb{R}^3$, [R,G,B]. We we each pixel equal mass and find a coupling between the color point clouds
of each image. We found better empirical results by embedding each pixel into LAB space, which is another three-dimensional space composed of a luminance channel and two color channels.

## Blending of images

The color transfer problem does not take into account where each pixel is within the image and what pixels are close to it. Another approach to optimal transport between two images
is to find a map between images as point clouds in (intensity, x, y)-space. This is a harder problem because we lose the standard tricks we can use to simplify the problem that we
have available in color-transfer problems.

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

## Dependencies
Dependencies are managed through [Pixi](https://pixi.sh/latest/) and listed in the `pixi.lock` file. The only dependency outside of python libraries is ffmpeg.Instructions for downloading Pixi are provided in the [Pixi documentation](https://pixi.sh/latest/installation/) and replicated below:

### Mac / Linux

Run the following command to install Pixi

```
curl -fsSL https://pixi.sh/install.sh | sh
```
and run

```
pixi install
```
to install the project dependencies.

### Windows

Download through [the installer](https://github.com/prefix-dev/pixi/releases/latest/download/pixi-x86_64-pc-windows-msvc.msi), making sure to select the option to add Pixi to your path.

Run
```
pixi install
```
to install the project dependencies.

## Downloading the data

The data (images, videos, frames of videos) is stored in a Cloudflare R2 instance. To access the data, enter the scripts directory and run the `data_install.sh` script.

