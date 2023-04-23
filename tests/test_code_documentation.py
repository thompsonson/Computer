import os
import subprocess
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.sql.code_documentation import (
    Base,
    GitProject,
    PythonModule,
    SourceFile,
    CodeClass,
    CodeFunction,
    Argument,
    Import,
)
from controllers.indexes.code_documentation import CodeDocumentation

# Update this with the appropriate test database URL
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def temp_db_session():
    """Fixture to create a test database session."""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


@pytest.fixture
def temp_python_module(tmpdir):
    module_path = tmpdir / "temp_module.py"
    module_path.write_text(
        "import math\n\ndef add(a: int, b: int) -> int:\n    return a + b\n\nclass Calculator:\n    def multiply(self, x: int, y: int) -> int:\n        return x * y\n",
        encoding="utf-8",
    )
    # Initialize a Git repository in the temporary directory
    subprocess.run(["git", "init"], cwd=tmpdir, check=True)
    # Set a dummy Git remote URL (origin)
    subprocess.run(
        ["git", "remote", "add", "origin", "https://example.com/dummy.git"],
        cwd=tmpdir,
        check=True,
    )
    return str(module_path)


def test_code_documentation(temp_db_session, temp_python_module):
    # Initialize the CodeDocumentation class
    code_doc = CodeDocumentation(
        folder_path=os.path.dirname(temp_python_module),
        module_name="temp_module",
        session=temp_db_session,
    )

    # Analyze the directory
    code_doc.analyze_directory()

    # Assert that the expected data was stored in the database
    assert temp_db_session.query(GitProject).count() == 1
    assert temp_db_session.query(PythonModule).count() == 1
    assert temp_db_session.query(SourceFile).count() == 1
    assert temp_db_session.query(CodeClass).count() == 1
    # Print the names of the CodeFunction entries in the database
    for code_function in temp_db_session.query(CodeFunction).all():
        print(code_function.name)
    assert temp_db_session.query(CodeFunction).count() == 2
    assert temp_db_session.query(Argument).count() == 4
    assert temp_db_session.query(Import).count() == 1

    # Assert that the function names are as expected
    functions = temp_db_session.query(CodeFunction).all()
    function_names = [func.name for func in functions]
    assert "add" in function_names
    assert "multiply" in function_names

    # Assert that the class name is as expected
    code_class = temp_db_session.query(CodeClass).first()
    assert code_class.name == "Calculator"
