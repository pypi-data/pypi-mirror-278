from pydantic import BaseModel

from fastdto.common.enums import PythonTypeEnum


class ColumnDTO(BaseModel):
    """DTO for parsed column from SQL query."""

    name: str
    python_type: PythonTypeEnum


class ParameterDTO(BaseModel):
    """DTO for parameter in query."""

    name: str
    parameter_type: PythonTypeEnum


class ParseResultDTO(BaseModel):
    """DTO for parsed query from SQL."""

    sql_query: str
    result_columns: list[ColumnDTO]
    parameters: list[ParameterDTO]
