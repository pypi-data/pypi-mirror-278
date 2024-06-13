from enum import Enum


ID_PATH_SEP = ','
PATH_SEP = '/'
FOLDER_TYPE = 'Folder'


class InvalidMetadataFormatException(Exception):
    pass


class Distribution(Enum):
    A = "Distribution A"
    B = "Distribution B"
    C = "Distribution C"
    D = "Distribution D"
    E = "Distribution E"
    F = "Distribution F"
    X = "Distribution X"
