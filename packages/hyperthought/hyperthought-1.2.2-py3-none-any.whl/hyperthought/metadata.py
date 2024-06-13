"""
Miscellaneous  functionality relating to metadata.
"""

import collections
from copy import deepcopy
import datetime


def from_api_format(metadata):
    """Convert metadata list from API format to list of MetadataItems."""
    if (
        not isinstance(metadata, collections.abc.Sequence)
        or
        isinstance(metadata, str)
    ):
        raise ValueError("metadata must be a non-string sequence")

    return [
        MetadataItem.from_api_format(item)
        for item in metadata
    ]


def to_api_format(metadata):
    """Convert list of MetadataItems to API formatted metadata."""
    if not isinstance(metadata, list):
        raise ValueError("metadata must be a list")

    for item in metadata:
        if not isinstance(item, MetadataItem):
            raise ValueError(
                "every element of metadata must be a MetadataItem")

    return [
        item.to_api_format()
        for item in metadata
    ]


class MetadataItem:
    """
    Convenience class for working with a metadata element.

    Parameters
    ----------
    key : str
        The key for the metadata item.
    value : various
        The value for the metadata item.
    units : str or None
        The units associated with the metadata item.
    annotation : str or None
        An annotation (comment) associated with the metadata item.
    type_ : str or None
        The type of value.  Must be one of self.VALID_TYPES.
    children : list of MetadataItem
        A list of items nested under the present item.
    """
    # Non-link types will be based on XML types.
    VALID_TYPES = {
        'link', 'string', 'boolean', 'decimal', 'integer', 'dateTime'
    }
    DEFAULT_TYPE_FOR_NONE_VALUES = 'string'
    DATE_CLASSES = {datetime.datetime, datetime.date, datetime.time}

    # Reference:  https://numpy.org/doc/stable/user/basics.types.html
    NUMPY_INT_CLASS_NAMES = {
        'short', 'ushort',
        'intc', 'uintc',
        'int_', 'uint',
        'longlong', 'ulonglong',
        'int8', 'int16', 'int32', 'int64',
        'uint8', 'uint16', 'uint32', 'uint64',
        'intp', 'uintp',
    }
    NUMPY_FLOAT_CLASS_NAMES = {
        'half', 'float16', 'single', 'double', 'longdouble', 'csingle',
        'cdouble', 'clongdouble',
        'float32', 'float64', 'float_'
    }
    # NOTE:  Complex numbers currently not parseable.
    NUMPY_STRING_CLASSES = {
        'byte', 'ubyte', 'str_',
    }
    NUMPY_BOOL_CLASS = 'bool_'

    # Map Python to XML (metadata) types.
    # This mapping must follow conversion from numpy types.
    TYPE_MAP = {
        'str': {
            'default': 'string',
            'all': ('link', 'string',)
        },
        'bool': {
            'default': 'boolean',
            'all': ('boolean',),
        },
        'int': {
            'default': 'integer',
            'all': ('integer', 'number', 'numeric'),
        },
        'float': {
            'default': 'decimal',
            'all': ('decimal', 'float', 'double', 'number', 'numeric'),
        },
        'date': {
            'default': 'date',
            'all': ('date',),
        },
        'time': {
            'default': 'time',
            'all': ('time',),
        },
        'datetime': {
            'default': 'dateTime',
            'all': ('dateTime',),
        },
    }

    def __init__(self, key, value=None, type_=None, units=None,
                 annotation=None, children=None):
        # data members
        self._key = None
        self._value = None
        self._type = None
        self._units = None
        self._annotation = None
        self._children = None

        if children is None:
            children = []

        # Set values using property setters.
        self.key = key
        self.set_value_and_type(value, type_)
        self.units = units
        self.annotation = annotation
        self.children = children

    def set_value_and_type(self, value, type_):
        """
        Set value and type simultaneously.

        This will minimize automatic type correction, as might happen
        if value and type are set in sequence, and preserve the original
        intention for the type.

        For example:

        # Original value = 123, type = "integer".
        item.type = "link"
        # Internally, item.type is reset to "integer", since the value, 123,
        # is an int.
        item.value = "/files/filesystementry/[FILE_ID]"
        # Internally, item.type changes from "integer" to "string"
        # But we wanted type to be "link"!
        item.set_value_and_type("/files/etc", "link")
        # item.type is "link", as desired.
        """
        # Use default type where no type has been specified and no type can
        # be inferred.
        if value is None and type_ is None:
            self._value = value
            self._type = self.DEFAULT_TYPE_FOR_NONE_VALUES
            return

        # Allow any valid type for a None value.
        # Default as needed if the type is not valid.
        if value is None and type_ is not None:
            self._value = value
            self._type = (
                type_ if type_ in self.VALID_TYPES
                else self.DEFAULT_TYPE_FOR_NONE_VALUES
            )
            return

        value_type_name = type(value).__name__

        # Convert from Numpy types.
        # NOTE:  Use value, not self.value, since the former will be used to
        #        determine the type.
        if value_type_name in self.NUMPY_INT_CLASS_NAMES:
            value = int(value)
        elif value_type_name in self.NUMPY_FLOAT_CLASS_NAMES:
            value = float(value)
        elif value_type_name in self.NUMPY_STRING_CLASSES:
            value = str(value)
        elif value_type_name == self.NUMPY_BOOL_CLASS:
            value = bool(value)

        # Reset value_type_name after (possibly) casting from a numpy type.
        value_type_name = type(value).__name__

        # Make sure value_type_name is allowed.
        if value_type_name not in self.TYPE_MAP:
            raise ValueError(f"Invalid value: {value}")

        # If type_ is None, reset to a default value.
        if type_ is None:
            if value_type_name == 'int':
                type_ = 'integer'
            elif value_type_name == 'float':
                type_ = 'decimal'
            elif value_type_name == 'str':
                type_ = 'string'
            elif value_type_name == 'bool':
                type_ = 'boolean'
            elif type(value) in self.DATE_CLASSES:
                type_ = 'dateTime'
            else:
                raise ValueError(f"Unknown value type: {value_type_name}")

            self._value = value
            self._type = type_
            return

        # At this point, neither value nor type_ is None.
        # Make sure the type matches the value_type.
        if type_ not in self.TYPE_MAP[value_type_name]['all']:
            type_ = self.TYPE_MAP[value_type_name]['default']

        self._value = value
        self._type = type_

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError("key must be a non-empty string")

        self._key = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.set_value_and_type(value, self._type)

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("units must be None or a string")

        self._units = value

    @property
    def annotation(self):
        return self._annotation

    @annotation.setter
    def annotation(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("annotation must be None or a string")

        self._annotation = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self.set_value_and_type(value=self._value, type_=value)

    @property
    def children(self):
        return [deepcopy(item) for item in self._children]

    @children.setter
    def children(self, value):
        if not isinstance(value, collections.abc.Sequence):
            raise ValueError("The value for children must be a sequence.")

        for element in value:
            if not isinstance(element, MetadataItem):
                raise ValueError(
                    "All elements of children must have type MetadataItem")

        self._children = [deepcopy(item) for item in value]

    def add_child(self, child):
        """Add a metadata item to the list of children."""
        if not isinstance(child, MetadataItem):
            raise ValueError("child must be a MetadataItem")

        self._children.append(child)

    def to_api_format(self):
        """
        Translate item data to the format expected by the API.

        Returns
        -------
        A dict that can be appended to a list of metadata items and passed to
        an endpoint.
        """

        def convert_value():
            if self.value.__class__ in self.DATE_CLASSES:
                return self.value.isoformat()
            else:
                return self.value

        output = {
            'keyName': self.key,
            'value': {
                'type': self.type,
                'link': convert_value(),
            }
        }

        if self.units is not None:
            # 'unit' should be singular per the API.
            output['unit'] = self.units

        if self.annotation is not None:
            output['annotation'] = self.annotation

        if self._children:
            output["children"] = to_api_format(self._children)

        return output

    @classmethod
    def from_api_format(cls, api_metadata_item):
        """
        Translate item data from API format to object of class.

        Parameters
        ----------
        api_metadata_item : dict
            Metadata item as returned by HyperThought REST API.

        Returns
        -------
        MetadataItem object representing the same data.
        """
        # Validate api_metadata_item.

        if not isinstance(api_metadata_item, collections.abc.Mapping):
            raise ValueError(
                "api_metadata_item must be a dict or other mapping")

        if "keyName" not in api_metadata_item:
            raise ValueError("api_metadata_item must have a 'keyName' key")

        kwargs = {
            "key": api_metadata_item["keyName"],
        }

        if "value" in api_metadata_item:
            if "link" not in api_metadata_item["value"]:
                raise ValueError(
                    "api_metadata_item['value'] must have a 'link' key")

            if "type" not in api_metadata_item["value"]:
                raise ValueError(
                    "api_metadata_item['value'] must have a 'type' key")

            kwargs["value"] = api_metadata_item["value"]["link"]

            # Allow the constructor to infer the type.
            # Exception:  object links (type == 'link').
            if api_metadata_item["value"]["type"] == "link":
                kwargs["type_"] = "link"

        if "annotation" in api_metadata_item:
            kwargs["annotation"] = api_metadata_item["annotation"]

        if "unit" in api_metadata_item:
            kwargs["units"] = api_metadata_item["unit"]

        if "children" in api_metadata_item:
            kwargs["children"] = from_api_format(api_metadata_item["children"])

        return cls(**kwargs)
