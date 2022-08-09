# SimpleObjectCropper
Small script to crop images for photogrammetry purposes

# Prerequisites
Python, OpenCV

# Usage
`python3 Cropper.py <path to folder with jpg/png/tiff> [(-f) || (-g)}`

# Parameters
-f --> Use FloodFill on Background (Inaccurate, but fast)

-g --> Use GrabCut to seperate Fore- & Background (Accurate, but slow)

eg.
python Cropper.py ./ExampleSet/ -g
