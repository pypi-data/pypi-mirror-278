"""
EIDS project parser.  Contains the EIDS parser that uses multiple parsing
methods to determine file type and metadata mostly based on regex matching.
"""

import re
import os

from ..parsers import BaseParser
from ..metadata import MetadataItem


class MultipleParserError(Exception):
    pass


class EIDS(BaseParser):
    """
    Parser for EIDS project files.

    Detects regex patterns in the filename to determine the file type
    and adds some basic metadata.
    """

    VALID_EXTENSIONS = {'txt', 'tiff', 'png', 'jpg'}

    def CT_parser(self, filename):
        """
        Match with CT Image Slice pattern and parse slice number.

        Example filesnames : '0001.tiff', '0002.tiff','0003.tiff'

        Parameters
        ----------
        filename : str
            The name of the file being parsed.

        Returns
        -------
        A list of MetadataItem or an empty list.
        """
        metadata = []
        # Matches digit of any length with '.tiff' at the end.
        CT_pattern = re.compile(r'\d+\.tiff')
        match = CT_pattern.fullmatch(filename)

        if match:
            # Matches digits of any length.
            digits_pattern = re.compile(r'\d+')
            number_match = digits_pattern.search(filename)
            ct_slice_number = int(number_match.group())
            metadata = [
                MetadataItem(
                    key='slice number',
                    value=ct_slice_number,
                ),
                MetadataItem(
                    key='image type',
                    value='CT reconstruction slice',
                )
            ]

        return metadata

    def EOS_recoat_parser(self, filename):
        """
        Parse metadata from EOS pre and post recoat images.

        Example filename : 'Sl74839205748392248_00112_730192837492047
                           .028432_Cam0_PowderbedExposureEnd.jpg'

        Parameters
        ----------
        filename : str
            The name of the file being parsed.

        Returns
        -------
        A list of MetadataItem or an empty list.
        """
        metadata = []
        # Matches if string contains: 'Cam[0-9]_Powderbed'
        EOS_recoat_pattern = re.compile(r'Cam\d_Powderbed')
        EOS_recoat_match = EOS_recoat_pattern.search(filename)

        if EOS_recoat_match:
            # Finds a number between underscores.
            layer_number_search = re.compile(r'_\d+_')
            layer_number = layer_number_search.search(filename)
            layer_number = int(layer_number.group().replace('_', ''))

            # Parse the processing state.
            # Matches 'ExposureEnd'.
            pre_coat_search = re.compile(r'ExposureEnd')
            # Matches 'RecoatingEnd'.
            post_coat_search = re.compile(r'RecoatingEnd')
            pre_coat = pre_coat_search.search(filename)
            post_coat = post_coat_search.search(filename)

            if pre_coat:
                processing_state = "pre recoat"

            elif post_coat:
                processing_state = 'post recoat'

            else:
                raise ValueError(
                    "Processing state not found in EOS recoat image filename."
                )

            metadata = [
                MetadataItem(
                    key='layer number',
                    value=f'{layer_number}',
                ),
                MetadataItem(
                    key='processing state',
                    value=f'{processing_state}',
                ),
                MetadataItem(
                    key='image type',
                    value='EOS recoat camera',
                )
            ]

        return metadata

    def AMSENSE_recoat_parser(self, filename):
        """
        Parses metadata from AMSENSE image files.

        Example file name: 'Recoat-Layer_1008-File_10700662.png'

        Parameters
        ----------
        filename : str
            The name of the file being parsed.

        Returns
        -------
        A list of MetadataItem or an empty list.
        """
        metadata = []
        # Check if entire string matches 'Rocoat-Layer_' + any length digit
        # + '-File_' + any length digit + case insensitive '.png'.
        AMSENSE_recoat_match = re.fullmatch(
            r'Recoat-Layer_\d+-File_\d+.[Pp][Nn][Gg]',
            filename)

        if AMSENSE_recoat_match:
            # Matches the number that appears between '-Layer_' and '-'.
            layer_number_search = re.compile(r'-Layer_(\d+)-')
            layer_number = layer_number_search.search(filename)
            layer_number = layer_number.group(1)

            metadata = [
                MetadataItem(
                    key='layer number',
                    value=layer_number,
                ),
                MetadataItem(
                    key='image type',
                    value='AMSENSE recoat camera',
                )
            ]

        return metadata

    def AMSENSE_thermal_parser(self, filename):
        """
        Parse metadata from AMSENSE thermal tomography pictures.

        Example filename: 'Layer000006.png'

        Parameters
        ----------
        filename : str
            Name of the file being parsed.

        Returns
        -------
        A list of MetadataItem or none.
        """
        metadata = []
        # Matches if entire string mathces 'Layer' + any length digit + '.png'
        AMSENSE_thermal_match = re.fullmatch(r'Layer\d+.png', filename)

        if AMSENSE_thermal_match:
            # matches any number
            layer_number_search = re.compile(r'\d+')
            layer_number = layer_number_search.search(filename)
            layer_number = int(layer_number.group())

            # create the metadata
            metadata = [
                MetadataItem(
                    key='layer number',
                    value=layer_number,
                ),
                MetadataItem(
                    key='image type',
                    value='AMSENSE thermal tomography',
                )
            ]

        return metadata

    def parse(self):
        """
        Iterate through all EIDS sub-parsers and attempt to parse metadata.
        If only one matches, add metadata to self. If metadata is returned
        from multiple parsers, raise an error.

        Sub parsers correspond to different file types in the workspace.
        A single file cannot be two different types so it should only match
        one parser.
        """
        filename = os.path.basename(self.file_path)
        parsers = [
            self.CT_parser,
            self.EOS_recoat_parser,
            self.AMSENSE_recoat_parser,
            self.AMSENSE_thermal_parser
        ]
        metadata = []

        for parser in parsers:
            parsed_metadata = parser(filename)

            if parsed_metadata:
                metadata.append(parsed_metadata)

        if not metadata:
            self.metadata = []
            return

        if len(metadata) > 1:
            raise MultipleParserError(
                "Filename matches patterns for multiple parsers. "
                "Contact parser developer or disable parser."
            )

        self.metadata = metadata[0]
