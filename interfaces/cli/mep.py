import typer
from utils.DBAdapter import DBAdapter
from controllers.mep import MEPController

app = typer.Typer()


def get_mep_controller():
    """Create and return an MEPController instance."""
    db_adapter = DBAdapter()
    return MEPController(db_adapter)


@app.command("fetch-and-store")
def fetch_and_store():
    """
    Fetch MEPs data from the web, parse it, and store it in the database.
    """
    mep_controller = get_mep_controller()
    mep_controller.fetch_and_store_meps()
    typer.echo("Fetched and stored MEPs data.")


@app.command("get")
def get(mep_id: int):
    """
    Retrieve an MEP by their ID.

    Args:
        mep_id (int): The ID of the MEP to retrieve.
    """
    mep_controller = get_mep_controller()
    mep = mep_controller.get_mep(mep_id)
    typer.echo(f"MEP Details: {mep}")


@app.command("search")
def search(query: str):
    """
    Search for MEPs based on a query.

    Args:
        query (str): The search query to use for finding MEPs.
    """
    mep_controller = get_mep_controller()
    search_results = mep_controller.search_meps(query)
    if not search_results:
        typer.echo("No MEPs found for the given query.")
    else:
        for result in search_results:
            typer.echo(f"MEP: {result}")


@app.command("search-by-name")
def search_by_name(name: str):
    """
    Search for MEPs by name.

    Args:
        name (str): The name to search for.
    """
    mep_controller = get_mep_controller()
    search_results = mep_controller.search_meps_by_name(name)
    if not search_results:
        typer.echo("No MEPs found for the given name.")
    else:
        for result in search_results:
            typer.echo(f"MEP: {result}")


@app.command("search-by-affiliation")
def search_by_affiliation(affiliation: str):
    """
    Search for MEPs by political affiliation.

    Args:
        affiliation (str): The political affiliation to search for.
    """
    mep_controller = get_mep_controller()
    search_results = mep_controller.search_meps_by_affiliation(affiliation)
    if not search_results:
        typer.echo("No MEPs found for the given affiliation.")
    else:
        for result in search_results:
            typer.echo(f"MEP: {result}")


@app.command("search-by-involvement")
def search_by_involvement(involvement: str):
    """
    Search for MEPs by involvement in specific topics.

    Args:
        involvement (str): The involvement to search for.
    """
    mep_controller = get_mep_controller()
    search_results = mep_controller.search_meps_by_involvement(involvement)
    if not search_results:
        typer.echo("No MEPs found for the given involvement.")
    else:
        for result in search_results:
            typer.echo(f"MEP: {result}")


if __name__ == "__main__":
    app()
