import typer
from controllers.indexes.code_documentation import CodeDocumentation

app = typer.Typer()


@app.command()
def analyze_code(folder_path: str, module_name: str):
    """
    Analyze a Python code directory and store the results in a database.

    Args:

        folder_path (str): The path to the directory containing the Python code.
        module_name (str): The name of the Python module to analyze.
    """

    # Initialize the CodeDocumentation class
    code_doc = CodeDocumentation(folder_path=folder_path, module_name=module_name)

    # Analyze the directory
    code_doc.analyze_directory()

    typer.echo("Code analysis completed successfully.")


if __name__ == "__main__":
    app()
