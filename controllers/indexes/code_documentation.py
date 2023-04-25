import logging
import ast
import astunparse
import os
import subprocess
from typing import Optional

from sqlalchemy.orm import Session
from models.sql.code_documentation import (
    GitProject,
    PythonModule,
    SourceFile,
    Import,
    CodeClass,
    CodeFunction,
    Argument,
)
from utils.DBAdapter import DBAdapter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CodeDocumentationVisitor(ast.NodeVisitor):
    """A custom AST node visitor that extracts information about classes, functions,
    and their arguments from a Python source file and stores the information in a database.

    Attributes:
        session (Session): A SQLAlchemy session object for interacting with the database.
        source_file (SourceFile): The source file being analyzed.
    """

    def __init__(self, session: Session, source_file: SourceFile):
        """Initializes the CodeDocumentationVisitor with the specified session and source file.

        Args:
            session (Session): A SQLAlchemy session object for interacting with the database.
            source_file (SourceFile): The source file being analyzed.
        """
        self.session = session
        self.source_file = source_file

    def visit_ClassDef(self, node: ast.ClassDef):
        """Visits a class definition node in the AST.

        Args:
            node (ast.ClassDef): The class definition node being visited.
        """
        # Create a CodeClass entry for the class definition
        code_class = CodeClass(
            name=node.name,
            docstring=ast.get_docstring(node),
            source_file=self.source_file,
        )
        self.session.add(code_class)

        # Recursively visit the body of the class definition
        # and pass the name of the class as the parent_class argument
        for child_node in node.body:
            if isinstance(child_node, ast.FunctionDef):
                self.visit_FunctionDef(child_node, parent_class=node.name)

    def visit_FunctionDef(self, node: ast.FunctionDef, is_top_level: bool = False, parent_class: str = None):  # type: ignore
        """Visits a function definition node in the AST.

        Args:
            node (ast.FunctionDef): The function definition node being visited.
            parent_class (str, optional): The name of the parent class if the function is a method.
        """
        if parent_class is None and not is_top_level:
            return
        logger.debug(
            "Processing function '%s' as a method of class '%s'", node.name, parent_class
        )
        # Determine if the function is a method of a class
        code_class = None
        if parent_class:
            code_class = (
                self.session.query(CodeClass).filter_by(name=parent_class).first()
            )

        # Create a CodeFunction entry for the function definition
        function = CodeFunction(
            name=node.name,
            return_type=astunparse.unparse(node.returns).strip() if node.returns else None,
            docstring=ast.get_docstring(node), 
            source_file=self.source_file,
            code_class=code_class,
        )
        self.session.add(function)

        # Extract argument information for the function
        num_args_with_defaults = len(node.args.defaults)
        for i, arg in enumerate(node.args.args):
            # Skip the 'self' argument for class methods
            if parent_class is not None and arg.arg == "self":
                continue
            # Determine if the argument has a default value
            has_default = i >= len(node.args.args) - num_args_with_defaults
            default_value = (
                node.args.defaults[i - (len(node.args.args) - num_args_with_defaults)]
                if has_default
                else None
            )

            argument = Argument(
                name=arg.arg,
                arg_type=astunparse.unparse(arg.annotation).strip() if arg.annotation else None, # type: ignore
                optional=has_default,
                function=function,
            )
            self.session.add(argument)

    # Add a new method to handle top-level functions
    def visit_TopLevelFunctionDef(self, node: ast.FunctionDef):
        logger.debug("Processing function '%s' as a top-level function", node.name)
        self.visit_FunctionDef(node, is_top_level=True)


class CodeDocumentation:
    """A class that analyzes Python source code files in a specified directory
    and stores the analysis results in a database.
    """

    def __init__(
        self,
        folder_path: str,
        module_name: str,
        session: Optional[Session] = None,
    ) -> None:
        """Initializes the CodeDocumentation class with the specified folder path.

        Args:
            folder_path (str): The path to the directory containing the Python files to be analyzed.
            module_name (str): The name of the Python module.
            session (Session, optional): A SQLAlchemy session object for interacting with the database.
        """
        self._folder_path = folder_path
        self._session = session or DBAdapter().unmanaged_session()

        # Retrieve the Git origin URL from the folder
        try:
            git_origin_url = subprocess.check_output(
                ["git", "remote", "get-url", "origin"],
                cwd=folder_path,
                universal_newlines=True,
            ).strip()
        except subprocess.CalledProcessError:
            raise ValueError("The specified folder is not a valid Git repository.")

        # Create or retrieve the GitProject and PythonModule entries
        git_project = (
            self._session.query(GitProject)
            .filter_by(origin_url=git_origin_url)
            .one_or_none()
        )
        if git_project is None:
            git_project = GitProject(origin_url=git_origin_url)
            self._session.add(git_project)

        python_module = (
            self._session.query(PythonModule)
            .filter_by(name=module_name, git_project=git_project)
            .one_or_none()
        )
        if python_module is None:
            python_module = PythonModule(name=module_name, git_project=git_project)
            self._session.add(python_module)
        self._module = python_module

    def _analyze_module(self, file_path: str) -> None:
        """Analyzes a Python source code file and stores the analysis results in the database.

        The method extracts information about functions and classes defined in the file,
        including function name, arguments, annotations, and docstring. The analysis results
        are stored as instances of the AnalysisResult model in the database.

        Args:
            file_path (str): The path to the Python source code file to be analyzed.
        """
        # Read the source code from the file
        with open(file_path, "r", encoding="utf-8") as file:
            source_code = file.read()

        # Parse the source code into an abstract syntax tree
        tree = ast.parse(source_code)

        # Create a SourceFile entry
        source_file = SourceFile(
            file_name=os.path.basename(file_path),
            file_path=file_path,
            module=self._module,
        )
        self._session.add(source_file)

        # Create an instance of the custom visitor and visit the AST
        visitor = CodeDocumentationVisitor(self._session, source_file)
        visitor.visit(tree)

        def set_parent_attr(node, parent=None):
            """Recursively set the 'parent' attribute for each node in the AST."""
            for child in ast.iter_child_nodes(node):
                child.parent = node  # type: ignore
                set_parent_attr(child, parent=node)

        # Set the 'parent' attribute for each node in the AST
        set_parent_attr(tree)

        # Extract import information
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imp = Import(
                        import_name=alias.name,
                        source_file=source_file,
                    )
                    self._session.add(imp)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imp = Import(
                        import_name=f"{node.module}.{alias.name}",
                        source_file=source_file,
                    )
                    self._session.add(imp)
            # Extract function information (not within a class)
            elif isinstance(node, ast.FunctionDef):
                # Check if the parent node is a ClassDef node
                if not (
                    hasattr(node, "parent") and isinstance(node.parent, ast.ClassDef)  # type: ignore
                ):
                    visitor.visit_TopLevelFunctionDef(node)

        # Commit the changes to the database
        self._session.commit()

    def analyze_directory(self) -> None:
        """Analyzes all Python source code files in the specified directory.

        The method recursively walks through all files in the directory specified by
        self._folder_path. For each file with a .py extension, it calls the _analyze_module
        method to perform the analysis. The analysis results are stored in the database.
        """
        for root, _, files in os.walk(self._folder_path):
            for file_name in files:
                if file_name.endswith(".py"):
                    file_path = os.path.join(root, file_name)
                    self._analyze_module(file_path)
