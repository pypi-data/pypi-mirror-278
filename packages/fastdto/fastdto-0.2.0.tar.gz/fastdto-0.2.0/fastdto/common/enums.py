from enum import StrEnum, auto


class ColumnTypeEnum(StrEnum):
    """Enum for columns types in dsl."""

    BIGINT = auto()
    BIGSERIAL = auto()
    BIT = auto()
    BITVAR = auto()
    BOOLEAN = auto()
    BOX = auto()
    BYTEA = auto()
    CHAR = auto()
    VARCHAR = auto()
    CIDR = auto()
    CIRCLE = auto()
    DATE = auto()
    DOUBLE_PRECISION = auto()
    INET = auto()
    INTEGER = auto()
    INTERVAL = auto()
    JSON = auto()
    JSONB = auto()
    LINE = auto()
    LSEG = auto()
    MACADDR = auto()
    MONEY = auto()
    NUMERIC = auto()
    PATH = auto()
    PG_LSN = auto()
    PG_SNAPSHOT = auto()
    POINT = auto()
    POLYGON = auto()
    REAL = auto()
    SMALLINT = auto()
    SMALLSERIAL = auto()
    SERIAL = auto()
    TEXT = auto()
    TIME = auto()
    TIMESTAMP = auto()
    TSQUERY = auto()
    TSVECTOR = auto()
    TXID_SNAPSHOT = auto()
    UUID = auto()
    XML = auto()

    @classmethod
    def _missing_(cls, value: str):
        value = value.lower()
        for member in cls:
            if member == value:
                return member
        return None


class PythonTypeEnum(StrEnum):
    """Enum for declaring mappings and query parameter types."""

    STR = auto()
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    LIST = auto()
    TUPLE = auto()
    SET = auto()
    BYTES = auto()
    DATE = auto()
    DATETIME = auto()
    DICT = auto()
    UUID = auto()
    ANY = auto()

    def __str__(self) -> str:
        """Method for correct representing types in generated file.

        Returns:
            str: Correct string.
        """
        match self.value:
            case PythonTypeEnum.UUID:
                return self.value.upper()
            case PythonTypeEnum.ANY:
                return self.value.capitalize()
            case _:
                ...
        return self.value

    @property
    def needed_import(self) -> str:
        """If type requires some imports -> return string that contains it.

        Returns:
            str: String with needed import.
        """
        match self.value:
            case PythonTypeEnum.DATE:
                return "from datetime import date"
            case PythonTypeEnum.DATETIME:
                return "from datetime import datetime"
            case PythonTypeEnum.UUID:
                return "from uuid import UUID"
            case PythonTypeEnum.ANY:
                return "from typing import Any"
            case _:
                ...
        return ""
