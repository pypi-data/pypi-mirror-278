"""
Conversion Handlers - Video

This module provides classes for converting between different video file formats. It includes concrete implementations of conversion classes for various file types (images, mp4, avi, gif, ...).
"""

from typing import List

import numpy as np
from cv2.typing import MatLike
from opencf_core.base_converter import WriterBasedConverter
from opencf_core.filetypes import FileType
from PIL import Image as PillowImage

from ..io_handlers import (
    FramesToGIFWriterWithImageIO,
    ImageToOpenCVReader,
    ImageToPillowReader,
    VideoArrayWriter,
    VideoToFramesReaderWithOpenCV,
)


class ImageToVideoConverterWithPillow(WriterBasedConverter):
    """
    Converts image files to video format.
    """

    file_reader = ImageToPillowReader()
    file_writer = VideoArrayWriter()

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.IMG_RASTER

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.VIDEO

    def _convert(self, input_contents: List[PillowImage.Image], args: None):
        """
        Converts a list of image files to a video file.

        Args:
            input_contents (List[PillowImage.Image]): List of input images.
            output_file (Path): Output video file path.
        """
        # Convert Pillow images to numpy arrays
        image_arrays = [np.array(img) for img in input_contents]

        # Convert list of numpy based opencv images to numpy array
        image_arrays = np.asarray(input_contents)

        return image_arrays


class ImageToVideoConverterWithOpenCV(WriterBasedConverter):
    """
    Converts image files to video format.
    """

    file_reader = ImageToOpenCVReader()
    file_writer = VideoArrayWriter()

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.IMG_RASTER

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.VIDEO

    def _convert(self, input_contents: List[np.ndarray], args: None):
        """
        Converts a list of image files to a video file.

        Args:
            input_contents (List[np.ndarray]): List of input images.
            output_file (Path): Output video file path.
        """
        # Convert list of numpy based opencv images to numpy array
        image_arrays = np.asarray(input_contents)

        return image_arrays


class VideoToGIFConverter(WriterBasedConverter):
    """
    Converts a video file to GIF format.
    """

    file_reader = VideoToFramesReaderWithOpenCV()
    file_writer = FramesToGIFWriterWithImageIO()

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.VIDEO

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.GIF

    def _convert(self, input_contents: List[List[MatLike]], args: None):
        """
        Converts a list of video frames to a GIF.

        Args:
            input_contents (List[MatLike]): List of video frames.

        Returns:
            bytes: The converted GIF content.
        """
        video_frames = input_contents[0]
        # Write video frames to GIF
        return video_frames
