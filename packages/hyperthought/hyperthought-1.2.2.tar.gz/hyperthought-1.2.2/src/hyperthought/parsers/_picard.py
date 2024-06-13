"""
Parsing for PiCARD data files.

Use class, Picard, to parse metadata from valid files. See method,
Picard.parse, for expected format and details of functionality.
"""

import re
import os

from datetime import datetime
from enum import IntEnum

from ..metadata import MetadataItem
from .base import BaseParser


class InvalidRowException(Exception):
    pass


class ExcelCellType(IntEnum):
    """
    Cell types from xlrd docs based on Excel types.
    https://xlrd.readthedocs.io/en/latest/api.html#xlrd.sheet.Cell
    """
    EMPTY = 0
    TEXT = 1
    NUMBER = 2
    DATE = 3
    BOOLEAN = 4
    ERROR = 5


class Picard(BaseParser):
    """
    A parser tailored to PiCARD test data files.

    Parameters
    ----------
    file_path : str
        A path to a PiCARD test file.
    """

    def __init__(self, file_path):
        self._file_path = file_path

        self.VALID_EXTENSIONS = {'.xls', '.xlsx', '.csv'}

    def parse(self):
        """
            Determines the file type of the file being parsed and sends it to
            the applicable parser for the format.
        """
        filename, file_extension = os.path.splitext(self._file_path)

        if file_extension not in self.VALID_EXTENSIONS:
            raise ValueError(
                "Unsupported file type. Supported types are: "
                f"{self.VALID_EXTENSIONS}"
            )

        if file_extension == ".xls":
            parser = XLSParser(self._file_path)
            parser.parse()
        elif file_extension == '.xlsx':
            parser = XLSXParser(self._file_path)
            if "Vishay" in filename.lower():
                parser.parse_xlsx()
        elif file_extension == ".csv":
            parser = CSVParser(self._file_path)
            if "liquid" in filename.lower():
                parser.parse_csv()


class XLSParser(Picard):
    """
        Iterate through each row in the "Details" sheet of an .xls
        excel file and parse metadata.

        Expected format:

        column 1            | column 2
        -------------------------------------------------
        Filename	        | example
        Geometry name	    | example
        Procedure name	    | Options
                            | example1
                            | Options
                            | example2
        [Parameters]        |
        Name	            | example
        Instrument type	    | example
        -------------------------------------------------

        Subsections titles (enclosed in brackets with empty column 2)
        are prepended to subsequent keys; there can be 0 to many subsections:
            {
                key='[Parameters]Name',
                value='example',
            }
            {
                key='[Parameters]Instrument type',
                value='example',
            }

        Options (found below a column 2 value of 'Option') are concatenated
        into a single value:
            {
                key='Procedure name'
                value='example1, example2'
            }
        """
    def __init__(self, file_path):

        self._file_path = file_path

        self.DATETIME_FORMAT = '%m/%d/%Y %H:%M:%S %p'

    def parse(self):
        # Import packages locally to avoid polluting global memory.
        import xlrd
        from xlrd import XLRDError

        workbook = xlrd.open_workbook(self._file_path)

        try:
            details_sheet = workbook.sheet_by_name('Details')
        except XLRDError:
            # 'Details' page not found
            self.metadata = []
            return

        # Matches any characters between brackets. E.g. '[Parameters]'
        subsection_pattern = re.compile(r'\[[^\]]*\]')

        subsection = ''
        options = False
        options_key = ''
        options_value = ''
        metadata = []

        for row in details_sheet.get_rows():
            if len(row) != 2:
                raise InvalidRowException(
                    f"Expected 2 cells, found {len(row)}"
                )

            key_cell, value_cell = row
            key_cell_type = ExcelCellType(key_cell.ctype)
            value_cell_type = ExcelCellType(value_cell.ctype)

            # --------------- Key parsing -------------
            # options is true if previous row's value == 'Options'
            if options:
                if key_cell_type == ExcelCellType.EMPTY:
                    if value_cell.value == 'Options':
                        continue

                    options_value += value_cell.value + ', '
                    continue
                else:
                    options = False
                    metadata.append(MetadataItem(
                        key=options_key,
                        value=options_value.strip(', ')
                    ))
                    options_key = ''
                    options_value = ''

            if value_cell.value == 'Options':
                if key_cell_type == ExcelCellType.EMPTY:
                    raise InvalidRowException(
                        "No key found for 'Options' value."
                    )
                options_key = key_cell.value
                options = True
                continue

            subsection_match = subsection_pattern.search(key_cell.value)

            if subsection_match:
                subsection = subsection_match.group()

                if value_cell_type != ExcelCellType.EMPTY:
                    raise InvalidRowException(
                        f"Subsection found with value {value_cell.value}"
                    )
                continue

            # ------------ Value Parsing -----------------
            units = None

            if value_cell_type == ExcelCellType.EMPTY:
                value = ''

            elif value_cell_type == ExcelCellType.TEXT:
                value_split = value_cell.value.split()
                if len(value_split) == 2:
                    try:
                        value = float(value_split[0])
                        units = value_split[1]
                    except ValueError:
                        value = value_cell.value
                else:
                    value = value_cell.value

            elif value_cell_type == ExcelCellType.NUMBER:
                value = value_cell.value

            elif value_cell_type == ExcelCellType.DATE:
                value = xlrd.xldate_as_datetime(
                    value_cell.value, 0
                    ).strftime(self.DATETIME_FORMAT)

            elif value_cell_type == ExcelCellType.BOOLEAN:
                if value_cell.value == 0:
                    value = 'False',
                elif value_cell.value == 1:
                    value = 'True'
                else:
                    raise ValueError(
                        "BOOLEAN must be 0 or 1. "
                        f"Found {value_cell.value}")

            elif value_cell_type == ExcelCellType.ERROR:
                # Convert to Excel error text
                value = xlrd.error_text_from_code[value_cell.value]

            metadata.append(MetadataItem(
                key=(subsection + key_cell.value),
                value=value,
                units=units
            ))

        if options:
            options = False
            metadata.append(MetadataItem(
                key=options_key,
                value=options_value.strip(', ')
            ))
            options_key = ''
            options_value = ''

        self.metadata = metadata


class XLSXParser(Picard):
    """
    Iterates through relevant summary data in XLSX format files, current
    functionality supports Vishay Summary files.
    """

    def __init__(self, file_path):
        self._file_path = file_path

        self.DATETIME_FORMAT = '%m/%d/%Y %H:%M:%S %p'

    def parse_xlsx(self):
        from openpyxl import load_workbook

        wb = load_workbook(
            filename=self._file_path,
            data_only=True
        )

        ws = wb.active

        keys = []
        val_list = []
        for col in ws.values:
            for value in col:
                if value is not None:
                    if isinstance(value, datetime):
                        val_list.append(value.strftime(self.DATETIME_FORMAT))
                    else:
                        val_list.append(value)
                    try:
                        if value.endswith(":"):
                            keys.append(value)
                    except Exception:
                        pass

        key_val_pairs = {}

        for idx, val in enumerate(val_list):
            if val in keys:
                curr_val = val
                next_val = val_list[(idx + 1)]
                key_val_pairs[curr_val] = next_val

        metadata = []
        for key, value in key_val_pairs.items():
            metadata.append(MetadataItem(key, value))

        self.metadata = metadata


class CSVParser:
    """
    Parser to filter relevant metadata out of csv format files. Current
    functionality supports "liquid cuvette" files.
    """
    def __init__(self, file_path):
        self._file_path = file_path
        self.DATETIME_FORMAT = '%m/%d/%Y %H:%M:%S %p'

    def parse_csv(self):
        import math
        import pandas as pd

        df = pd.read_csv(self._file_path, on_bad_lines="skip")

        cols = []
        for col in df.values:
            counter = 0
            for value in col:
                if isinstance(value, str) and math.isnan(value):
                    counter += 1
                    if col.tolist() not in cols:
                        if counter > 1:
                            cols.append(col.tolist())

        formatted_cols = []

        for col in cols:
            counter = 0
            for value in col:
                if isinstance(value, str) and math.isnan(value):
                    counter += 1
                if counter > 1:
                    formatted_cols.append(col[0].split('   '))

        pairs = []
        for col in formatted_cols:
            if len(col) > 1 and col not in pairs:
                new_col = [value for value in col if value != ""]
                pairs.append(new_col)

        formatted_pairs = []

        for pair in pairs:
            if pair not in formatted_pairs:
                if ":" not in pair[1]:
                    formatted_pairs.append(pair)

        metadata = []

        for pair in formatted_pairs:
            metadata.append(MetadataItem(pair[0], pair[1]))

        self.metadata = metadata
