from fastdto.common.enums import ColumnTypeEnum
from fastdto.common.mappings import TO_PYTHON


class Column:
    """Base class for column declaration in DSL file."""

    def __init__(
        self,
        column_type: ColumnTypeEnum,
    ):  # TODO extend parameters and change from str to Enum?
        self.column_type = column_type
        if isinstance(column_type, ColumnTypeEnum):
            self.python_type = TO_PYTHON[column_type]
        else:
            raise Exception  # TODO raise exception if type is not good

    @property
    def sql_type(self):
        """Returns type for sqlglot lib.

        Returns:
            _type_: _description_  # TODO typing
        """
        return self.column_type

    @property
    def dto_type(self):
        """# TODO typing."""
        return self.python_type
