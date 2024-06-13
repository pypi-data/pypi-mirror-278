import re
from importlib import import_module

from sqlglot import exp, parse_one
from sqlglot.dialects.postgres import Postgres
from sqlglot.optimizer.qualify import qualify
from sqlglot.optimizer.scope import Scope, build_scope

from fastdto.common import dto
from fastdto.common.enums import PythonTypeEnum
from fastdto.core.dsl.schema.base import Base


def parse_query(query: str) -> dto.ParseResultDTO:
    """Parse query and returns declarative DTO.

    Parse query to:
    - What columns are fetched
    - From which tables

    Args:
        query (str): Raw SQL query

    Returns:
        dto.ParseResultDTO: DTO of ParsedQuery.
    """
    ast = parse_one(query)
    import_module(".dbschema", package="dbschema")  # TODO change for robust
    qualify(
        expression=ast,
        schema=Base.schema(),
        expand_alias_refs=False,
        validate_qualify_columns=False,
        quote_identifiers=False,
        identify=False,
        dialect=Postgres,
    )
    result_query = ast.sql(
        dialect=Postgres,
    )
    qualify(
        expression=ast,
        schema=Base.schema(),
        dialect=Postgres,
    )
    root = build_scope(ast)

    result_columns = []
    if root:
        result_columns = _get_columns_from_scope(scope=root)
    parameters = _parse_parameters(query=query)
    return dto.ParseResultDTO(
        sql_query=result_query,
        result_columns=result_columns,
        parameters=parameters,
    )


def _parse_parameters(query: str) -> list[dto.ParameterDTO]:
    """Parse query and extract anme and types of parameters.

    Args:
        query (str): Raw sql query.

    Returns:
        list[dto.ParameterDTO]: Parsed parameters.
    """
    pattern = r"@(\w+):(\w+)"
    parameters = []

    matches = re.findall(pattern, query)

    for p_name, p_type in matches:
        parameters.append(
            dto.ParameterDTO(
                name=p_name,
                parameter_type=p_type,
            )
        )
    return parameters


def _get_column_type(
    scope: Scope,
    column: exp.Expression,
) -> PythonTypeEnum:
    """Get pythonic column type from scope.

    Args:
        root (Scope): Current column Scope.
        column (exp.Expression): Current column expression.
        root_sql (exp.Expression): Current root sql query.

    Returns:
        PythonTypeEnum: Resulting python Enum.
    """
    match column:
        case exp.Column():
            column_source = scope.sources.get(column.table)
            match column_source:
                case exp.Table():
                    return PythonTypeEnum(
                        Base.schema(pythonic=True)
                        .get(column_source.name, {})  # type: ignore
                        .get(column.name, "any"),
                    )
                case Scope():
                    return next(
                        filter(
                            lambda scope_column: scope_column.name == column.name,
                            _get_columns_from_scope(scope=column_source),
                        ),
                        dto.ColumnDTO(name="", python_type=PythonTypeEnum.ANY),
                    ).python_type
                case _:
                    raise Exception  # TODO
        case exp.Count():
            return PythonTypeEnum.INT
        case exp.Avg():
            return PythonTypeEnum.FLOAT
        case exp.LogicalAnd() | exp.LogicalOr():
            return PythonTypeEnum.BOOL
        case exp.Concat() | exp.Upper() | exp.Lower():
            return PythonTypeEnum.STR
    return PythonTypeEnum.ANY


def _get_columns_from_scope(scope: Scope) -> list[dto.ColumnDTO]:
    """Get all columns that was selected in scope with their types.

    Types of columns based on schema that User defines in dbschema.py file.

    Args:
        scope (Scope): Current SQL expression scope.

    Returns:
        list[dto.ColumnDTO]: List of all selected columns dtos.
    """
    result = []
    parent_node = next(scope.walk())
    match parent_node:
        case exp.Select():
            for column_exp in parent_node.selects:
                column: exp.Expression = column_exp.this
                python_type = _get_column_type(
                    column=column,
                    scope=scope,
                )
                result.append(
                    dto.ColumnDTO(
                        name=column_exp.alias_or_name,
                        python_type=python_type,
                    )
                )
        case exp.Union() | exp.Except() | exp.Intersect():
            left_scope = build_scope(parse_one(parent_node.left.sql()))
            for column_exp in parent_node.selects:
                column: exp.Expression = column_exp.this
                python_type = _get_column_type(
                    column=column,
                    scope=left_scope,
                )
                result.append(
                    dto.ColumnDTO(
                        name=column_exp.alias_or_name,
                        python_type=python_type,
                    )
                )
        case _:
            return []
    return result
