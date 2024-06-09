"""
File: img_opencv.py
Author: Hermann Agossou
Description: This module provides classes for reading and writing images using OpenCV.
"""

from pathlib import Path

import cv2
import numpy as np
from opencf_core.io_handler import Reader, Writer


class ImageToOpenCVReader(Reader):
    """
    Reads an image file and returns an OpenCV image object.
    """

    # input_format = np.ndarray

    def _check_input_format(self, content: np.ndarray) -> bool:
        """
        Validates if the provided content is an OpenCV image object.

        Args:
            content (opencv_image): The content to be validated.

        Returns:
            bool: True if the content is an OpenCV image object, False otherwise.
        """
        return isinstance(content, np.ndarray) and content.ndim == 3

    def _read_content(self, input_path: Path) -> np.ndarray:
        """
        Reads and returns the content from the given input path as an OpenCV image object.

        Args:
            input_path (Path): The path to the input image file.

        Returns:
            opencv_image: The OpenCV image object read from the input file.
        """
        return cv2.imread(str(input_path))


class OpenCVToImageWriter(Writer):
    """
    Writes an OpenCV image object to an image file.
    """

    def _check_output_format(self, content) -> bool:
        """
        Validates if the provided content is an OpenCV image object.

        Args:
            content: The content to be validated.

        Returns:
            bool: True if the content is an OpenCV image object, False otherwise.
        """
        return isinstance(content, np.ndarray) and content.ndim == 3

    def _write_content(self, output_path: Path, output_content):
        """
        Writes the provided OpenCV image object to the given output path as an image file.

        Args:
            output_path (Path): The path to the output image file.
            output_content: The OpenCV image object to be written to the output file.
        """
        cv2.imwrite(str(output_path), output_content)  # Write image using OpenCV
