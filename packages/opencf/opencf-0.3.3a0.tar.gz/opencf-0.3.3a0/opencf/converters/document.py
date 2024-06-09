"""
Conversion Handlers - Document

This module provides classes for converting between document different file formats. It includes concrete implementations of conversion classes for various file types (pdf, docx, epub, ...).
"""

from typing import List

import aspose.words as aw
import fitz
from opencf_core.base_converter import WriterBasedConverter
from opencf_core.filetypes import FileType
from pdf2docx import Converter as pdf2docxConverter
from PIL import Image as PillowImage
from pypdf import PdfReader, PdfWriter

from ..io_handlers import ImageToPillowReader, PdfToPyPdfReader, PyPdfToPdfWriter
from ..io_handlers.pdf import (
    AsposeReader,
    AsposeWriter,
    Pdf2DocxReader,
    Pdf2DocxWriter,
    PdfToPymupdfReader,
    PillowToPDFWriter,
    PillowToPDFWriterwithPypdf,
    PymupdfToImageExtractorWriter,
    PymupdfToImageWriter,
    PypdfToImageExtractorWriter,
)


class ImageToPDFConverterWithPyPdf(WriterBasedConverter):
    """
    Converts image files to PDF format using PyPDF.
    """

    file_reader = ImageToPillowReader()
    file_writer = PillowToPDFWriterwithPypdf()
    folder_as_output = False

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.IMG_RASTER

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.PDF

    def _convert(
        self, input_contents: List[PillowImage.Image], args: None
    ) -> List[PillowImage.Image]:
        return input_contents


# class ImageToPDFConverterWithImg2pdf(WriterBasedConverter):
#     """
#     Converts image files to PDF format using img2pdf.
#     """

#     file_reader = None
#     file_writer = None

#     @classmethod
#     def _get_supported_input_types(cls) -> FileType:
#         return FileType.IMG_RASTER

#     @classmethod
#     def _get_supported_output_types(cls) -> FileType:
#         return FileType.PDF

#     def _convert(self, input_contents: List[Path], outputfile: Path):
#         filepaths = input_contents
#         # Convert images to PDF using img2pdf
#         with open(output_file, "wb") as f:
#             f.write(img2pdf.convert(filepaths))


class ImageToPDFConverterWithPillow(WriterBasedConverter):
    """
    Converts img files to pdf format using pillow
    """

    file_reader = ImageToPillowReader()
    file_writer = PillowToPDFWriter()
    folder_as_output = False

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.IMG_RASTER

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.PDF

    def _convert(self, input_contents: List[PdfReader], args: None) -> List[PdfReader]:
        # Assuming you want to convert each page to an image
        return input_contents


# class ImageToPDFConverterwithPymupdf(WriterBasedConverter):
#     """
#     Converts img files to pdf format using pillow
#     """

#     file_reader = None
#     file_writer = PillowToPDFWriter()
#     folder_as_output = False

#     @classmethod
#     def _get_supported_input_types(cls) -> FileType:
#         return FileType.IMG_RASTER

#     @classmethod
#     def _get_supported_output_types(cls) -> FileType:
#         return FileType.PDF

#     def _convert(self, input_contents: List[Path], args: None) -> List[PdfReader]:
#         image_paths = input_contents
#         pdf_document = fitz.open()
#         for img_path in image_paths:
#             img = fitz.open(img_path)
#             pdf_document.insert_pdf(img)
#         pdf_document.save(output_pdf_path)


# class PDFToImageConverterWithPdf2image(WriterBasedConverter):
#     """
#     Converts PDF files to image format using pdf2image
#     """

#     file_reader = None
#     file_writer = None
#     folder_as_output = True

#     @classmethod
#     def _get_supported_input_types(cls) -> FileType:
#         return FileType.PDF

#     @classmethod
#     def _get_supported_output_types(cls) -> FileType:
#         return FileType.IMG_RASTER

#     def _convert(
#         self, input_contents: List[Path], args: None
#     ) -> List[fitz.Document]:
#         # Assuming you want to convert each page to an image
#         for pdf_path in input_contents
#             images = pdf2image.convert_from_path(pdf_path)
#         return input_contents


class PDFToImageConverterwithPymupdf(WriterBasedConverter):
    """
    Converts PDF files to image format using pymupdf
    """

    file_reader = PdfToPymupdfReader()
    file_writer = PymupdfToImageWriter()
    folder_as_output = True

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.PDF

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.IMG_RASTER

    def _convert(
        self, input_contents: List[fitz.Document], args: None
    ) -> List[fitz.Document]:
        # Assuming you want to convert each page to an image
        return input_contents


class PDFToImageExtractorwithPypdf(WriterBasedConverter):
    """
    Converts PDF files to image format using pypdf
    """

    file_reader = PdfToPyPdfReader()
    file_writer = PypdfToImageExtractorWriter()
    folder_as_output = True

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.PDF

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.IMG_RASTER

    def _convert(self, input_contents: List[PdfReader], args=None):
        return input_contents


class PDFToImageExtractorwithPymupdf(WriterBasedConverter):
    """
    Converts PDF files to image format.
    """

    file_reader = PdfToPymupdfReader()
    file_writer = PymupdfToImageExtractorWriter()
    folder_as_output = True

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.PDF

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.IMG_RASTER

    def _convert(
        self, input_contents: List[fitz.Document], args=None
    ) -> List[fitz.Document]:
        return input_contents


class PDFToDocxConvertorwithPdf2docx(WriterBasedConverter):
    """
    Converts PDF files to docx format using [pdf2docx](https://github.com/ArtifexSoftware/pdf2docx) as recommanded [here](https://stackoverflow.com/a/65932031/16668046)
    There s also a cli interface as presented in [their online](https://pdf2docx.readthedocs.io/en/latest/quickstart.cli.html)
    """

    file_reader = Pdf2DocxReader()
    file_writer = Pdf2DocxWriter()
    folder_as_output = False

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.PDF

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.DOCX

    def _convert(
        self, input_contents: List[pdf2docxConverter], args: None
    ) -> List[pdf2docxConverter]:
        all_documents = input_contents
        return all_documents


class PDFToDocxWithAspose(WriterBasedConverter):
    """
    Converts PDF files to docx format using Aspose.Words for Python.
    """

    file_reader = AsposeReader()
    file_writer = AsposeWriter()
    folder_as_output = False

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.PDF

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.DOCX

    def _convert(
        self, input_contents: List[aw.Document], args: None
    ) -> List[aw.Document]:
        return input_contents


class PDFToHTML(WriterBasedConverter):
    """
    i could use this [tool](https://linux.die.net/man/1/pdftohtml) to do it
    """


class MergePDFswithPypdf(WriterBasedConverter):
    """
    Merges multiple PDF files into a single PDF.
    """

    file_reader = PdfToPyPdfReader()
    file_writer = PyPdfToPdfWriter()
    folder_as_output = False

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.PDF

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.PDF

    def _convert(self, input_contents: List[PdfReader], args: None):
        pdf_writer = PdfWriter()

        for pdf_file_reader in input_contents:
            for page in pdf_file_reader.pages:
                pdf_writer.add_page(page)

        return pdf_writer
