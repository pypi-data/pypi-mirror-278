from typer import Argument, Typer

from fastdto.core.codegen.service import generate_orm_code, init_project_structure

app = Typer()


@app.command()
def init(directory: str = Argument(default="dbschema")):  # noqa: B008
    """Generates file structure for DB schema and scripts.

    Args:
        directory (str, optional): Specify directory of project.
            Defaults to "dbschema".
    """
    init_project_structure(directory=directory)


@app.command()
def generate(
    filename: str = Argument(default="__init__"),  # noqa: B008
    scripts_dir: str = Argument(default="dbschema/scripts"),  # noqa: B008
):
    """Generates file with ORM functions and Pydantic mapping.

    Args:
        filename (str, optional): Filename. Defaults to "__init__".
        scripts_dir (str, required): Directory with .sql scripts.
    """
    generate_orm_code(
        filename=filename,
        scripts_dir=scripts_dir,
    )
