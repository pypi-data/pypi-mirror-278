"""
images_to_video.py

A script to convert a sequence of images into a video file using OpenCV.

Dependencies:
- OpenCV (cv2): A computer vision library for image and video processing.
- pathlib: An object-oriented interface to filesystem paths.

Usage:
    $ python images_to_video.py <input_images> <output_video>

Arguments:
    input_images: List of input image files to be converted into a video file.
                  Example: image1.jpg image2.jpg
    output_video: Path to the output video file.
                  Example: output_video.avi

Example:
    $ python images_to_video.py image1.jpg image2.jpg output_video.avi

Author: Hermann Agossou
Date: Date of creation/modification
"""

from pathlib import Path
from typing import Tuple

import cv2
import numpy as np


def save_video_from_array_images(
    img_array: np.ndarray,
    size: Tuple[int, int],
    save_path: Path,
    fps: int = 15,
    label: str = "img",
):

    if img_array is None:
        print("img_array sould be set")
        return False

    if not len(img_array):
        print("No valid images found.")
        return False

    img_array = np.asarray(img_array)
    assert (
        img_array.ndim == 4
    )  # Ensure img_array is 4-dimensional (frames, height, width, channels)

    label = str(label)

    save_path = Path(save_path)
    suffix = save_path.suffix

    # Initialize video writer
    if suffix.lower() == ".avi":
        fourcc = cv2.VideoWriter_fourcc(*"DIVX")
    elif suffix.lower() == ".mp4":
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    else:
        ValueError(
            f"bad suffix for the videowriter. found suffix={suffix.lower()} instead of .avi or .mp4"
        )

    print("size = ", size)
    out = cv2.VideoWriter(str(save_path), fourcc, fps, size)

    # Write images to video
    print(f"writing {len(img_array)} {label}")
    for img in img_array:
        out.write(img)

    # Release video writer
    out.release()
    print(f"video save_path is {save_path}")

    return True


def save_video_from_image_files(image_files, output_path, fps=15):
    img_array = []
    size = None

    # Check if the output directory exists
    output_directory = Path(output_path).parent
    if not output_directory.exists():
        print(f"Output directory {output_directory} does not exist.")
        return False

    for img_filepath in image_files:
        img_filepath = Path(img_filepath)
        if not img_filepath.exists():
            print(f"File {img_filepath} not found.")
            return False

        img = cv2.imread(str(img_filepath))
        if img is None:
            print(f"Error reading image file: {img_filepath}")
            return False

        height, width, _ = img.shape
        size = (width, height)
        img_array.append(img)

    assert size is not None

    return save_video_from_array_images(img_array, size, output_path, fps=fps)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Convert images to a video file")
    parser.add_argument(
        "input_images",
        nargs="+",
        help="Input image files. Example: image1.jpg image2.jpg",
    )
    parser.add_argument(
        "output_video", help="Output video file. Example: output_video.avi"
    )
    args = parser.parse_args()

    input_images = args.input_images
    output_video = args.output_video

    success = save_video_from_image_files(input_images, output_video)
    if success:
        print("Video conversion successful!")
    else:
        print("Video conversion failed.")


if __name__ == "__main__":
    main()
