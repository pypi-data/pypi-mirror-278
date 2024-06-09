"""
Conversion Handlers - Structured

This module provides classes for converting between stuctured different file formats. It includes concrete implementations of conversion classes for various file types (xml, json, xlsx, csv, ...).
"""

import xml.etree.ElementTree as ET
from typing import Any, Dict, List

from opencf_core.base_converter import WriterBasedConverter
from opencf_core.filetypes import FileType
from opencf_core.io_handler import (
    CsvToDictReader,
    DictToCsvWriter,
    DictToJsonWriter,
    TreeToXmlWriter,
    XmlToTreeReader,
)

from ..io_handlers.spreadsheet import DictToXlsxWriter, XlsxToDictReader


class XMLToJSONConverter(WriterBasedConverter):
    """
    Converts XML files to JSON format.
    """

    file_reader: XmlToTreeReader = XmlToTreeReader()
    file_writer: DictToJsonWriter = DictToJsonWriter()

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.XML

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.JSON

    def _convert(self, input_contents: List[ET.Element], args=None) -> Dict[str, Any]:
        def parse_element(element: ET.Element) -> Dict[str, Any]:
            """
            Recursively parses an XML element and converts it to a dictionary.
            """
            parsed_data: Dict[str, Any] = {}
            if element:
                for child in element:
                    if len(child) > 0:
                        parsed_data[child.tag] = parse_element(child)
                    else:
                        parsed_data[child.tag] = child.text
            else:
                parsed_data[element.tag] = element.text
            return parsed_data

        json_data: Dict[str, Any] = {}

        for root in input_contents:
            json_data[root.tag] = parse_element(root)

        return json_data


class CSVToXMLConverter(WriterBasedConverter):
    """
    Converts CSV files to XML format.
    """

    file_reader: CsvToDictReader = CsvToDictReader()
    file_writer: TreeToXmlWriter = TreeToXmlWriter()

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.CSV

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.XML

    def _convert(self, input_contents: List[Dict[str, Any]], args=None) -> ET.Element:
        """
        Converts the list of dictionaries to an XML ElementTree element.

        Args:
            input_contents (List[Dict[str, Any]]): The list of dictionaries to convert.
            args (optional): Additional arguments for the conversion process.

        Returns:
            ET.Element: The resulting XML ElementTree element.
        """

        def dict_to_xml(tag: str, d: Dict[str, Any]) -> ET.Element:
            """
            Converts a dictionary to an XML element.

            Args:
                tag (str): The tag name for the root element.
                d (Dict[str, Any]): The dictionary to convert.

            Returns:
                ET.Element: The resulting XML element.
            """
            elem = ET.Element(tag)
            for key, val in d.items():
                child = ET.SubElement(elem, key)
                child.text = str(val)
            return elem

        root = ET.Element("root")
        for item in input_contents:
            item_elem = dict_to_xml("item", item)
            root.append(item_elem)

        return root


class XLSXToCSVConverter(WriterBasedConverter):
    """
    Converts XLSX files to CSV format.
    """

    file_reader: XlsxToDictReader = XlsxToDictReader()
    file_writer: DictToCsvWriter = DictToCsvWriter()

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.XLSX

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.CSV

    def _convert(
        self, input_contents: List[Dict[str, Any]], args=None
    ) -> List[Dict[str, Any]]:
        """
        Converts the list of dictionaries from XLSX to the format suitable for CSV.

        Args:
            input_contents (List[Dict[str, Any]]): The list of dictionaries to convert.
            args (optional): Additional arguments for the conversion process.

        Returns:
            List[Dict[str, Any]]: The resulting list of dictionaries for CSV.
        """
        return input_contents


class CSVToXLSXConverter(WriterBasedConverter):
    """
    Converts CSV files to XLSX format.
    """

    file_reader: CsvToDictReader = CsvToDictReader()
    file_writer: DictToXlsxWriter = DictToXlsxWriter()

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.CSV

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.XLSX

    def _convert(
        self, input_contents: List[Dict[str, Any]], args=None
    ) -> List[Dict[str, Any]]:
        return input_contents
