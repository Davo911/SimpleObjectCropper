# SimpleObjectCropper
Small script to crop images for photogrammetry purposes

# Prerequisites
Python, OpenCV

# Usage
`python3 Cropper.py <path to folder with jpg/png> [(-f) || (-g)}`

# Parameters
-f --> Use FloodFill
-g --> Use GrabCut

eg.
python Cropper.py ./ExampleSet/ -g
