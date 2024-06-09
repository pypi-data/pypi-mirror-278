"""
PDF File I/O Handlers

This module provides classes for reading and writing PDF files using the PyPDF library. It includes abstract base classes
and concrete implementations for converting between PDF files and PyPDF PdfReader objects.
"""

import io
from io import BytesIO
from pathlib import Path
from typing import Any, List

import aspose.words as aw
import fitz  # PyMuPDF
from opencf_core.io_handler import Reader, Writer
from pdf2docx import Converter as pdf2docxConverter
from PIL import Image
from PIL import Image as PillowImage
from pypdf import PdfReader, PdfWriter


class PdfToPyPdfReader(Reader):
    """
    Reads a PDF file and returns a [PyPDF PdfReader object](https://pypdf.readthedocs.io/en/4.2.0/modules/PdfReader.html).
    """

    # input_format = PdfReader

    def _check_input_format(self, content: PdfReader) -> bool:
        """
        Validates if the provided content is a PyPDF PdfReader object.

        Args:
            content (PdfReader): The content to be validated.

        Returns:
            bool: True if the content is a PyPDF PdfReader object, False otherwise.
        """
        return isinstance(content, PdfReader)

    def _read_content(self, input_path: Path) -> PdfReader:
        """
        Reads and returns the content from the given input path as a PyPDF PdfReader object.

        Args:
            input_path (Path): The path to the input PDF file.

        Returns:
            PdfReader: The PyPDF PdfReader object read from the input file.
        """
        pdf_reader = PdfReader(input_path)
        return pdf_reader


class PyPdfToPdfWriter(Writer):
    """
    Writes the provided [PyPDF PdfWriter object](https://pypdf.readthedocs.io/en/4.2.0/modules/PdfWriter.html)
    """

    # output_format = PdfWriter

    def _check_output_format(self, content: PdfWriter) -> bool:
        """
        Validates if the provided content is a PyPDF PdfWriter object.

        Args:
            content (PdfWriter): The content to be validated.

        Returns:
            bool: True if the content is a PyPDF PdfWriter object, False otherwise.
        """
        return isinstance(content, PdfWriter)

    def _write_content(self, output_path: Path, output_content: PdfWriter):
        """
        Writes the provided PyPDF PdfWriter object to the given output path as a PDF file.

        Args:
            output_path (Path): The path to the output PDF file.
            output_content (PdfWriter): The PyPDF PdfWriter object to be written to the output file.
        """
        with open(output_path, "wb") as output_pdf:
            output_content.write(output_pdf)


class PillowToPDFWriter(Writer):

    def _check_output_format(self, content: List[PillowImage.Image]) -> bool:
        """
        Validates if the provided content is a PyPDF PdfWriter object.

        Args:
            content (PdfWriter): The content to be validated.

        Returns:
            bool: True if the content is a PyPDF PdfWriter object, False otherwise.
        """
        return isinstance(content, list) and all(
            [isinstance(ct, PillowImage.Image) for ct in content]
        )

    def _write_content(
        self, output_path: Path, output_content: List[PillowImage.Image]
    ):
        """
        Writes the provided PillowImage.Image objects to the given output path as a PDF file.

        Args:
            output_path (Path): The path to the output PDF file.
            output_content (List[PillowImage.Image]): The PillowImage.Image objects to be written to the output file.
        """
        images = output_content
        output_file = output_path

        # Create a list of all the input images and convert them to RGB
        images = [img.convert("RGB") for img in images]

        # Save the PDF file
        images[0].save(output_file, save_all=True, append_images=images[1:])


class PillowToPDFWriterwithPypdf(Writer):
    """
    Writes a collection of Pillow images to a PDF file using PyPDF.
    """

    def _check_output_format(self, content: List[PillowImage.Image]) -> bool:
        """
        Checks if the provided content is a list of Pillow images.

        Args:
            content (List[PillowImage.Image]): The content to be checked.

        Returns:
            bool: True if the content is a list of Pillow images, False otherwise.
        """
        return all(isinstance(image, PillowImage.Image) for image in content)

    def _write_content(
        self, output_path: Path, output_content: List[PillowImage.Image]
    ):
        """
        Writes the provided list of Pillow images to the given PDF file path.

        Args:
            output_path (Path): The path to the PDF file.
            output_content (List[PillowImage.Image]): The list of Pillow images to be written to the file.
        """
        # Create a new PDF document
        pdf_writer = PdfWriter()

        for image in output_content:
            # Create a bytes buffer to hold the image data
            img_buffer = BytesIO()
            image.save(img_buffer, format="PDF")
            img_buffer.seek(0)

            # Add the image as a page to the PDF
            pdf_writer.add_page(img_buffer)

        # Save the PDF to the specified output path
        with open(output_path, "wb") as f:
            pdf_writer.write(f)


class PdfToPymupdfReader(Reader):
    """
    Reads content from a PDF file and returns it as a fitz.Document object.
    """

    def _check_input_format(self, content: Path) -> bool:
        """
        Checks if the provided content is a valid PDF file.

        Args:
            content (Path): The path to the PDF file to be checked.

        Returns:
            bool: True if the content is a valid PDF file, False otherwise.
        """
        return isinstance(content, fitz.Document)

    def _read_content(self, input_path: Path) -> fitz.Document:
        """
        Reads and returns the content from the given input path.

        Args:
            input_path (Path): The path to the input PDF file.

        Returns:
            fitz.Document: The content read from the input PDF file.
        """
        return fitz.open(str(input_path))


class PymupdfToImageWriter(Writer):
    """
    Writes PDF pages as images to a specified folder.
    """

    def _check_output_format(self, content: List[fitz.Page]) -> bool:
        """
        Checks if the provided content is a list of fitz Page objects.

        Args:
            content (List[fitz.Page]): The content to be checked.

        Returns:
            bool: True if the content is a list of fitz Page objects, False otherwise.
        """
        return all(isinstance(page, fitz.Document) for page in content)

    def _write_content(self, output_path: Path, output_content: List[fitz.Document]):
        """
        Writes the provided PDF pages as images to the specified folder.

        Args:
            output_path (Path): The path to the output folder.
            output_content (List[fitz.Page]): The list of PDF pages to be written as images.
        """
        output_folder = output_path
        output_folder.mkdir(parents=True, exist_ok=True)

        use_pillow = False

        for i, doc in enumerate(output_content):
            for pageNo in range(doc.page_count):
                page = doc.load_page(pageNo)
                zoom = 2  # zoom factor
                mat = fitz.Matrix(zoom, zoom)
                pix: fitz.Pixmap = page.get_pixmap(matrix=mat)
                img_path = output_folder / f"pdf{i+1}-page{pageNo+1}.png"
                if use_pillow:
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    img.save(img_path, "PNG")
                else:
                    pix.save(filename=img_path)


class PypdfToImageExtractorWriter(Writer):

    def _check_output_format(self, content: List[PdfReader]) -> bool:
        """
        Validates if the provided content is a PyPDF PdfReader object.

        Args:
            content (List[PdfReader]): The content to be validated.

        Returns:
            bool: True if the content is a list of PyPDF PdfReader objects, False otherwise.
        """
        return isinstance(content, list) and all(
            [isinstance(ct, PdfReader) for ct in content]
        )

    def _write_content(self, output_path: Path, output_content: List[PdfReader]):
        """
        Writes the provided PdfReader objects to the given output folder.

        read more [here](https://pypdf.readthedocs.io/en/4.2.0/user/extract-images.html)

        Args:
            output_path (Path): The path to the output folder.
            output_content (List[PdfReader]): The PdfReader objects to be written to the output folder.
        """

        output_folder = output_path
        output_path.mkdir(parents=True, exist_ok=True)

        assert (
            output_folder.is_dir()
        ), f"Output path {output_folder} is not a dir while a folder is required for this conversion"

        for i, pdf_document in enumerate(output_content):
            for page_num, page in enumerate(pdf_document.pages):
                for count, img in enumerate(page.images):
                    fpath = (
                        output_folder
                        / f"pdf{i+1}-page{page_num+1}-fig{count+1}-{img.name}"
                    )
                    with open(str(fpath), "wb") as fp:
                        fp.write(img.data)


class PymupdfToImageExtractorWriter(Writer):
    """
    Extracts images from a fitz.Document and saves them as image files.
    """

    def _check_output_format(self, content: List[fitz.Document]) -> bool:
        """
        Checks if the provided content matches the expected output format.

        Args:
            content (List[fitz.Page]): The content to be checked.

        Returns:
            bool: True if the content matches the expected output format, False otherwise.
        """
        return all(isinstance(page, fitz.Document) for page in content)

    def _write_content(self, output_path: Path, output_content: List[fitz.Document]):
        """
        Writes the provided content to the given output path.

        Args:
            output_path (Path): The path to the output file.
            output_content (List[fitz.Page]): The content to be written to the output file.
        """
        output_folder = output_path
        output_folder.mkdir(parents=True, exist_ok=True)

        for i, doc in enumerate(output_content):
            for pageNo in range(doc.page_count):
                # page = doc.load_page(pageNo)
                for img_index, img in enumerate(
                    doc.get_page_images(pno=pageNo, full=True)
                ):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    img_ext = base_image["ext"]
                    img_path = (
                        output_folder
                        / f"pdf{i+1}-page{pageNo+1}-fig{img_index+1}.{img_ext}"
                    )
                    with open(img_path, "wb") as img_file:
                        img_file.write(image_bytes)


class AsposeReader(Reader):
    """
    Reads content from a PDF file and returns it as an Aspose.Words Document.
    """

    def _check_input_format(self, content: aw.Document) -> bool:
        """
        Checks if the provided content is a aw.Document object.

        Args:
            content (aw.Document): The content to be checked.

        Returns:
            bool: True if the content is a aw.Document object, False otherwise.
        """
        return isinstance(content, aw.Document)

    def _read_content(self, input_path: Path) -> aw.Document:
        """
        Reads and returns the content from the given PDF file path.

        Args:
            input_path (Path): The path to the PDF file.

        Returns:
            aw.Document: The Aspose.Words Document object read from the PDF file.
        """
        doc = aw.Document(str(input_path))

        # Load the document from the disc.
        # doc = aw.Document()

        # # Use DocumentBuilder to add content to the document
        # builder = aw.DocumentBuilder(doc)
        # for paragraph in pdf_doc.get_child_nodes(aw.NodeType.PARAGRAPH, True):
        #     builder.write(paragraph.get_text())

        return doc


class AsposeWriter(Writer):
    """
    Writes content from an Aspose.Words Document to a DOCX file.
    """

    def _check_output_format(self, content: aw.Document) -> bool:
        """
        Checks if the provided content is an Aspose.Words Document.

        Args:
            content (aw.Document): The content to be checked.

        Returns:
            bool: True if the content is an Aspose.Words Document, False otherwise.
        """
        return isinstance(content, list) and all(
            [isinstance(ct, aw.Document) for ct in content]
        )

    def _write_content(self, output_path: Path, output_content: List[aw.Document]):
        """
        Writes the provided Aspose.Words Document to the given DOCX file path.

        Args:
            output_path (Path): The path to the DOCX file.
            output_content (aw.Document): The Aspose.Words Document to be written to the file.
        """
        doc = output_content[0]
        doc.save(str(output_path))


class Pdf2DocxReader(Reader):
    """
    Reads content from a PDF file and returns it as an pdf2docx Document.
    """

    def _check_input_format(self, content: Any) -> bool:
        """
        Checks if the provided content is a PDF file.

        Args:
            content (pdf2docx.Converter): The content to be checked.

        Returns:
            bool: True if the content is a PDF file, False otherwise.
        """
        return isinstance(content, pdf2docxConverter)

    def _read_content(self, input_path: Path) -> aw.Document:
        """
        Reads and returns the content from the given PDF file path.

        Args:
            input_path (Path): The path to the PDF file.

        Returns:
            pdf2docx.Converter: The pdf2Docx Document object read from the PDF file.
        """
        cv = pdf2docxConverter(pdf_file=input_path)
        return cv


class Pdf2DocxWriter(Writer):
    """
    Writes content from a PDF to DOCX using pdf2docx.
    """

    def _check_output_format(self, content: List[pdf2docxConverter]) -> bool:
        """
        Checks if the provided content isList[pdf2docx.Converter] objects.

        Args:
            content (List[pdf2docx.Converter]): The content to be checked.

        Returns:
            bool: True if the content is a pdf2docx.Converter object, False otherwise.
        """
        return isinstance(content, list) and all(
            [isinstance(ct, pdf2docxConverter) for ct in content]
        )

    def _write_content(
        self, output_path: Path, output_content: List[pdf2docxConverter]
    ):
        """
        Writes the first provided pdf2docx.Converter object to the given DOCX file path.

        Args:
            output_path (Path): The path to the DOCX file.
            output_content (List[pdf2docxConverter]): The pdf2docx.Converter objects to be written to the file.
        """
        cv = output_content[0]
        cv.convert(docx_filename=str(output_path), start=0, end=None)
        cv.close()
