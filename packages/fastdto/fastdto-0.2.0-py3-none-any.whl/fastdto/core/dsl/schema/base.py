from fastdto.common.enums import PythonTypeEnum
from fastdto.core.dsl.schema.column import Column


class BaseMeta(type):
    """Metaclass for storing all schema in DB."""

    def __new__(cls, name, bases, namespace):
        """Common `__init__` for type class."""
        fields = {
            name: field
            for name, field in namespace.items()
            if isinstance(field, Column)
        }

        new_namespace = namespace.copy()

        for name in fields.keys():
            del new_namespace[name]

        new_namespace["_fields"] = fields

        return super().__new__(cls, name, bases, new_namespace)


class Base(metaclass=BaseMeta):
    """Base class for table declaration."""

    @classmethod
    def schema(
        cls,
        pythonic: bool = False,
    ) -> dict[str, dict[str, PythonTypeEnum | str]]:
        """Generates a schema based on table declaration.

        Returns:
            dict: Generated schema
        """
        if pythonic:
            return {
                table.__tablename__: {  # type: ignore
                    name: column.python_type
                    for name, column in table._fields.items()  # type: ignore
                }
                for table in cls.__subclasses__()
            }
        return {
            table.__tablename__: {  # type: ignore
                name: column.sql_type
                for name, column in table._fields.items()  # type: ignore
            }
            for table in cls.__subclasses__()
        }
