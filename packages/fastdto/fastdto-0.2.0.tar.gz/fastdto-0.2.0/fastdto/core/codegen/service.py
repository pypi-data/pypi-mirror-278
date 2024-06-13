import os
import shutil
from io import StringIO
from pathlib import Path

import fastdto.common.errors as errors
from fastdto.common import dto
from fastdto.common.errors import FastDTOError
from fastdto.common.utils import append_stringio, to_camel_case, to_snake_case
from fastdto.core.dsl.parse.service import parse_query

INDENT = "    "


def init_project_structure(directory: str) -> None | FastDTOError:
    """Create directory and files for DB schema.

    Returns:
        None | FastDTOError: None if all good, Error if smth wrong
    """
    import fastdto

    package_dir = Path(os.path.abspath(os.path.dirname(fastdto.__file__)))
    templates_path = package_dir.joinpath("templates")
    if os.access(directory, os.F_OK) and os.listdir(directory):
        raise errors.DirectoryAlreadyExistsError(
            f"Directory {directory} already exists and not empty"
        )

    try:
        shutil.copytree(templates_path.joinpath("init"), directory)
    except Exception as exc:
        raise errors.DirectoryCreateError(
            "Something went wrong while creating directory"
        ) from exc


def generate_orm_code(filename: str, scripts_dir: str) -> None | FastDTOError:
    """Generates file that contains scripts with DTO mapping.

    Args:
        filename (str): Filename
        scripts_dir (str): Directory that has .sql files

    Returns:
        None | FastDTOError: None if all good, Error if smth wrong
    """
    buf = StringIO()
    optional_imports = set()
    for file_or_dir in Path(scripts_dir).iterdir():
        if not file_or_dir.exists():
            continue
        if file_or_dir.suffix.lower() == ".sql":
            with file_or_dir.open() as f:
                query = f.read()
            parsed_query = parse_query(query=query)
            optional_imports = _add_optional_import_for_query(
                parsed_query=parsed_query,
                optional_imports=optional_imports,
            )
            buf = _generate_func_for_query(
                name=file_or_dir.stem,
                buffer=buf,
                parsed_query=parsed_query,
            )
    buf = _generate_imports(
        buffer=buf,
        optional_imports=optional_imports,
    )
    with Path(scripts_dir).joinpath(filename + ".py").open("w") as f:
        f.write(buf.getvalue())


def _generate_imports(
    buffer: StringIO,
    optional_imports: set | None = None,
) -> StringIO:
    """Generates imports for codegen functions.

    Args:
        buffer (StringIO): Buffer to save current progress of generated file.

    Returns:
        StringIO: Writed buffer.
    """
    import_buffer = StringIO()
    if optional_imports:
        imports_list = sorted(optional_imports)
        for optionat_import in imports_list:
            print(optionat_import, file=import_buffer)
        print("", file=import_buffer)
    print("from fastdto.connection import IAsyncExecutor", file=import_buffer)
    print(
        "from fastdto.core.codegen.model import FastDTOModel",
        end="\n\n\n",
        file=import_buffer,
    )
    return append_stringio(target=import_buffer, to_append=buffer)


def _generate_func_for_query(
    name: str,
    buffer: StringIO,
    parsed_query: dto.ParseResultDTO,
) -> StringIO:
    """Generates function for specific query.

    Args:
        name (str): Name of file with query without file extenstion (without .sql).
        parsed_query (dto.ParseResultDTO): Parsed SQL query with metadata.
        buffer (StringIO): Buffer to save current progress of generated file.

    Returns:
        StringIO: Saved buffer.
    """
    buffer = _generate_dto_for_query(
        name=name,
        buffer=buffer,
        parsed_query=parsed_query,
    )
    buffer = _generate_func(
        name=name,
        buffer=buffer,
        parsed_query=parsed_query,
    )
    return buffer


def _generate_func(
    name: str,
    buffer: StringIO,
    parsed_query: dto.ParseResultDTO,
) -> StringIO:
    buffer = _generate_signature(
        name=name,
        buffer=buffer,
        parsed_query=parsed_query,
    )
    buffer = _generate_body(
        name=name,
        buffer=buffer,
        parsed_query=parsed_query,
    )
    return buffer


def _generate_body(
    name: str,
    buffer: StringIO,
    parsed_query: dto.ParseResultDTO,
) -> StringIO:
    print(f"{INDENT}result = await executor.execute(", file=buffer)
    print(f'{INDENT * 2}"""', file=buffer)
    print(f"{INDENT * 2}{parsed_query.sql_query.replace('@', ':')}", file=buffer)
    print(f'{INDENT * 2}""",', file=buffer)
    for parameter in parsed_query.parameters:
        print(f"{INDENT * 2}{parameter.name}={parameter.name},", file=buffer)
    print(f"{INDENT})", file=buffer)
    if parsed_query.result_columns:
        print(
            f"{INDENT}return [{to_camel_case(name)}Result.from_list(row) for row in result]",  # noqa:E501
            file=buffer,
        )
    print(end="\n\n", file=buffer)
    return buffer


def _generate_signature(
    name: str,
    buffer: StringIO,
    parsed_query: dto.ParseResultDTO,
) -> StringIO:
    print(f"async def {to_snake_case(name)}(", file=buffer)
    print(f"{INDENT}executor: IAsyncExecutor,", file=buffer)
    for parameter in parsed_query.parameters:
        print(f"{INDENT}{parameter.name}: {parameter.parameter_type},", file=buffer)

    if parsed_query.result_columns:
        print(f") -> list[{to_camel_case(name)}Result]:", file=buffer)
    else:
        print(") -> None:", file=buffer)
    return buffer


def _generate_dto_for_query(
    name: str,
    buffer: StringIO,
    parsed_query: dto.ParseResultDTO,
) -> StringIO:
    """Generates code for DTO object for query.

    Args:
        name (str): Name of query file.
        buffer (StringIO): Buffer with file content.
        parsed_query (dto.ParseResultDTO): DTO with parsed query and metadata.
    """
    if not parsed_query.result_columns:
        return buffer

    print(f"class {to_camel_case(name)}Result(FastDTOModel):", file=buffer)
    for column in parsed_query.result_columns:
        print(f"{INDENT}{column.name}: {column.python_type}", file=buffer)
    print(end="\n\n", file=buffer)
    return buffer


def _add_optional_import_for_query(
    parsed_query: dto.ParseResultDTO,
    optional_imports: set,
) -> set:
    """Add optional import for query if they needed.

    Args:
        parsed_query (dto.ParseResultDTO): DTO with parsed query metadata.
        optional_imports (set): Set with optional imports.

    Returns:
        set: Updated set with optional imports.
    """
    optional_imports = _add_imports_for_query_parameters(
        parsed_query=parsed_query,
        optional_imports=optional_imports,
    )
    optional_imports = _add_imports_for_resulted_columns(
        parsed_query=parsed_query,
        optional_imports=optional_imports,
    )
    return optional_imports


def _add_imports_for_query_parameters(
    parsed_query: dto.ParseResultDTO,
    optional_imports: set,
) -> set:
    """Add optional imports to existing ones if needed.

    Based on query parameter types.

    Args:
        parsed_query (dto.ParseResultDTO): DTO with parsed query metadata.
        optional_imports (set): Set with optional imports.

    Returns:
        set: Updated set with optional imports.
    """
    if not parsed_query.parameters:
        return optional_imports

    for parameter in parsed_query.parameters:
        optional_imports.add(parameter.parameter_type.needed_import)
    return optional_imports


def _add_imports_for_resulted_columns(
    parsed_query: dto.ParseResultDTO,
    optional_imports: set,
) -> set:
    """Adds optional imports to existing ones if needed.

    Based on types of resulting colmuns of query.

    Args:
        parsed_query (dto.ParseResultDTO): DTO with parsed query metadata.
        optional_imports (set): Set with optional imports.

    Returns:
        set: Updated set with optional imports.
    """
    if not parsed_query.result_columns:
        return optional_imports
    for column in parsed_query.result_columns:
        optional_imports.add(column.python_type.needed_import)
    return optional_imports
