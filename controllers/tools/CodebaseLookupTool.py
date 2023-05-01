import os
import logging
import sys

from sqlalchemy.exc import OperationalError

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from typing import Optional, Type, Any
from pydantic import Field, root_validator

from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.tools import BaseTool
from langchain.llms.base import BaseLLM


def _get_default_sql_database():
    return SQLDatabase.from_uri("sqlite:///.db/database.db")


class CodebaseLookupTool(BaseTool):
    """Tool for searching the structured db version of the codebase."""

    name = "CodebaseLookup"
    description = """
Useful for when you need the  git_project, source_file, arguments, and/or docstring for a function or class (code_classes). 
Columns to ask for code_class and functions are docstring, for arguments it is name and arg_type.
to get the full source_file, use the source_file table with the id from functions or code_class. 
"""
    db: SQLDatabase = Field(default_factory=_get_default_sql_database)
    llm: Any = Field(default_factory=OpenAI(temperature=0))
    db_chain: Optional[str]

    @root_validator
    def resolve_db_chain(self, values: dict) -> dict:
        """Resolve the db_chain."""
        db_chain = values.get("db_chain")
        db = values.get("db")
        llm = values.get("llm")
        if db_chain is None:
            values["db_chain"] = SQLDatabaseChain(llm=llm, database=db, verbose=True)
        return values

    def _run(self, query: str) -> str:
        """Use the tool."""
        # TODO: catch sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) ambiguous column name: name
        # if it's caught, can the query be re-run with the table name prefixed?
        try:
            response = self.db_chain.run(query)  # type: ignore
        except OperationalError as exc:
            logging.error("OperationalError: %s", exc)
            query = f"this query had a join, use aliases in the select statement to avoid ambiguity on column names.\n{query}"
            response = self.db_chain.run(query)  # type: ignore
        return response

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("CodebaseLookupTool does not support async")
