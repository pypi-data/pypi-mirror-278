# Image Downloader
A Python package to download images from given URLs and save them with unique filenames. This package is especially useful for batch downloading and saving images while avoiding filename conflicts.

## Features
- Downloads images from a list of URLs.
- Saves images to a specified directory.
- Ensures unique filenames using timestamps.
- Handles filename conflicts interactively.
- Displays progress using a dynamic progress bar in Jupyter Notebook.

## Installation
You can install the package using pip:
```bash
pip install download_images_1
```
## Usage
### Basic Usage
```python
from download_images_1 import download_images
# List of image URLs
urls = [
    'https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg?auto=compress&cs=tinysrgb&w=1440',
    'https://images.pexels.com/photos/104827/cat-pet-animal-domestic-104827.jpeg?auto=compress&cs=tinysrgb&w=1440'
]
# Destination directory
destination_directory = 'data/cat'
# Base name for the images
image_name = 'cat'
# Download images
download_images(urls, destination_directory, image_name)
```
### Handling Filename Conflicts
If a file with the same name already exists, you will be prompted to either skip the file, modify the filename, or use a unique timestamp.


# Example usage
```python
urls = [
    'https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg?auto=compress&cs=tinysrgb&w=1440',
    'https://images.pexels.com/photos/104827/cat-pet-animal-domestic-104827.jpeg?auto=compress&cs=tinysrgb&w=1440'
]
destination_directory = 'data/cat'  # Use a relative path for compatibility
image_name = 'cat'
download_images(urls, destination_directory, image_name)
```
%ls
