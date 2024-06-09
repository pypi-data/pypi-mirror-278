"""
Main Module

This module contains the main application logic.
"""

import argparse

from opencf_core.converter_app import BaseConverterApp
from opencf_core.logging_config import logger_config

from opencf.converters.document import PDFToImageExtractorwithPymupdf

from .converters import (
    CSVToXMLConverter,
    ImageToPDFConverterWithPillow,
    ImageToPDFConverterWithPyPdf,
    ImageToVideoConverterWithOpenCV,
    ImageToVideoConverterWithPillow,
    MergePDFswithPypdf,
    PDFToDocxConvertorwithPdf2docx,
    PDFToDocxWithAspose,
    PDFToImageConverterwithPymupdf,
    PDFToImageExtractorwithPypdf,
    TextToTextConverter,
    VideoToGIFConverter,
    XLSXToCSVConverter,
    XMLToJSONConverter,
)


class ConverterApp(BaseConverterApp):
    """
    Application for file conversion.
    """

    converters = [
        XMLToJSONConverter,
        CSVToXMLConverter,
        TextToTextConverter,
        XLSXToCSVConverter,
        ImageToPDFConverterWithPyPdf,
        ImageToPDFConverterWithPillow,
        PDFToImageConverterwithPymupdf,
        PDFToImageExtractorwithPypdf,
        PDFToImageExtractorwithPymupdf,
        ImageToVideoConverterWithPillow,
        ImageToVideoConverterWithOpenCV,
        VideoToGIFConverter,
        PDFToDocxWithAspose,
        PDFToDocxConvertorwithPdf2docx,
        MergePDFswithPypdf,
    ]


def main() -> None:
    """
    Main function to run the file conversion application.
    """
    parser = argparse.ArgumentParser(description="File BaseConverter App")
    parser.add_argument("files", nargs="+", type=str, help="Paths to the input files")
    parser.add_argument(
        "-t", "--input-file-type", type=str, help="Type of the input file"
    )
    parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        default="",
        help="Path to the output file (optional)",
    )
    parser.add_argument(
        "-ot", "--output-file-type", type=str, help="Type of the output file (optional)"
    )
    parser.add_argument(
        "-l",
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Log level for the application. Default is INFO.",
    )

    args = parser.parse_args()

    input_file_paths: str = args.files
    input_file_type: str = args.input_file_type
    output_file_path: str = args.output_file
    output_file_type: str = args.output_file_type
    log_level: str = args.log_level

    logger_config.set_log_level_str(level=log_level)

    app = ConverterApp(
        input_file_paths, input_file_type, output_file_path, output_file_type
    )
    app.run()


if __name__ == "__main__":
    main()
