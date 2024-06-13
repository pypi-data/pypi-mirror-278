"""
Generic JSON.

Used to parse json files into a nested metadata structure.
"""
import json
from typing import Dict
from typing import List
from typing import Union

from .base import BaseParser
from ..metadata import MetadataItem


class GenericJson(BaseParser):
    """
    Generic JSON parser.  Will parse any JSON content for use
    in HyperThought.
    """
    VALID_EXTENSIONS = {'json', 'norms'}

    def _parse_json(
        self,
        input: Union[List, Dict],
        prefix: str = '',
    ) -> List[MetadataItem]:
        """
        Create a nested structure of MetadataItems

        Parameters
        ----------
        input : dict
            A dictionary of generic data.

        Returns
        -------
        A nested list of MetadataItems.  Nestedness will be expressed through
        the `children` attribute of a MetadataItem.
        """
        output = []

        if isinstance(input, list):
            for element in input:
                return self._parse_json(input=element)
        else:
            for key in input:
                # Item will collect parameter values then
                # will be used to instantiate a MetadataItem.
                item = {'key': f'{prefix}{key}'}

                if not (
                    isinstance(input[key], dict)
                    or
                    isinstance(input[key], list)
                ):
                    # If not a dict and not a list, data[key] is a value.
                    item['value'] = input[key]
                elif isinstance(input[key], dict):
                    # When presented a dict, recursively process it.
                    item['children'] = self._parse_json(input=input[key])
                elif isinstance(input[key], list):
                    # When presented a list, iterate through it
                    # recursively and append a counter to key.
                    item['children'] = []

                    for index, element in enumerate(input[key]):
                        if isinstance(element, dict):
                            item['children'].extend(self._parse_json(
                                input=element)
                            )
                        else:
                            # If the element is not a dict then
                            # construct a dict that will return
                            # a MetadataItem.
                            item['children'].extend(self._parse_json(
                                input={f"{key}_{index}": element})
                            )

                output.append(MetadataItem(**item))

            return output

    def parse(self) -> None:
        """
        Parse the file located at self.file_path, then set
        metadata to a list of MetadataItems
        """
        exception_message = (
            'Unable to open specified file. Is the content formatted as JSON?')

        try:
            with open(self._file_path, 'r') as fh:
                data = json.load(fh)
        except Exception as e:
            # Add exception message to error and re-raise.
            raise Exception('{}  Error: {}'.format(exception_message, str(e)))

        # Create a nested metadata structure.
        self.metadata = self._parse_json(input=data)
