"""
Generic XML.

Used to parse XML files into a nested metadata structure.
"""
import re
import xml.etree.ElementTree as ET

from .base import BaseParser
from ..metadata import MetadataItem


class GenericXML(BaseParser):
    """
    Generic XML parser.  Will parse any XML content it for use
    in HyperThought.
    """
    VALID_EXTENSIONS = {'xml'}

    def _normalize_text(self, input_text: str):
        """
        Normalize the text value from an XML element.

        The method used to extract a text value from an XML element may
        return excessive whitespace and/or line breaks.  This method will
        remove them.

        Parameters
        ----------
        input_text : str
            Text extracted from an XML element.

        Returns
        -------
        Text extracted from an XML element with excess whitespace stripped
        and line breaks removed.
        """
        if input_text is None:
            return None

        output_text = re.sub('\n', '', input_text.strip())
        return output_text

    def _parse_xml(self, element: ET.Element) -> list:
        """
        Created a nested metadata structure based on an XML file.

        Parameters
        ----------
        element : ET.Element
            The root element of a parsed XML tree.

        Returns
        -------
        A nested MetadataItem.
        """
        value = self._normalize_text(element.text)

        children = [
            MetadataItem(
                key=attrib,
                value=element.attrib[attrib],
                type_=element.attrib[attrib],
                units=None,
                annotation=None,
                children = [],
            )
            for attrib in element.attrib
        ]
        children.extend([self._parse_xml(child) for child in element])

        return MetadataItem(
            key=element.tag,
            value=value,
            type_=type(value),
            units=None,
            annotation=None,
            children=children,
        )

    def parse(self) -> None:
        """
        Parse the file located at self.file_path, then set
        metadata to a list of MetadataItems
        """
        exception_message = (
            'Unable to open specified file. Is the content formatted as XML?')

        try:
            with open(self._file_path, 'r') as fh:
                tree = ET.parse(self.file_path)
                root = tree.getroot()
        except Exception as e:
            # Add exception message to error and re-raise.
            raise Exception('{}  Error: {}'.format(exception_message, str(e)))

        # Convert xml tree to nested dict
        self.metadata = [self._parse_xml(root)]
