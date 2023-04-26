""" sqlalchemy classes for the code documentation controller """

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class GitProject(Base):
    __tablename__ = "git_projects"
    id = Column(Integer, primary_key=True)
    origin_url = Column(String, nullable=False)
    modules = relationship("PythonModule", back_populates="git_project")

    def __repr__(self):
        return f"<GitProject(id={self.id}, origin_url='{self.origin_url}')>"

    def __init__(self, origin_url: str):
        """Represents a Git project.

        Attributes:
            origin_url (str): The origin upstream URL of the Git project.
            modules (List[PythonModule]): A list of Python modules within the Git project.
        """
        self.origin_url = origin_url


class PythonModule(Base):
    __tablename__ = "python_modules"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    git_project_id = Column(Integer, ForeignKey("git_projects.id"))
    git_project = relationship("GitProject", back_populates="modules")
    files = relationship("SourceFile", back_populates="module")

    def __repr__(self):
        return f"<PythonModule(id={self.id}, name='{self.name}', git_project_id={self.git_project_id})>"

    def __init__(self, name: str, git_project: GitProject):
        """Represents a Python module within a Git project.

        Attributes:
            name (str): The name of the Python module.
            git_project (GitProject): The Git project to which the module belongs.
            files (List[SourceFile]): A list of source code files within the module.
        """
        self.name = name
        self.git_project = git_project


class SourceFile(Base):
    __tablename__ = "source_files"
    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    module_id = Column(Integer, ForeignKey("python_modules.id"))
    module = relationship("PythonModule", back_populates="files")
    imports = relationship("Import", back_populates="source_file")
    classes = relationship("CodeClass", back_populates="source_file")
    functions = relationship("CodeFunction", back_populates="source_file")

    def __repr__(self):
        return f"<SourceFile(id={self.id}, file_name='{self.file_name}', file_path='{self.file_path}', module_id={self.module_id})>"

    def __init__(self, file_name: str, file_path: str, module: PythonModule):
        """Represents a source code file within a Python module.

        Attributes:
            file_name (str): The name of the source code file.
            file_path (str): The file path of the source code file.
            module (PythonModule): The Python module to which the file belongs.
            imports (List[Import]): A list of imports within the file.
            classes (List[CodeClass]): A list of classes defined in the file.
            functions (List[CodeFunction]): A list of functions defined in the file.
        """
        self.file_name = file_name
        self.file_path = file_path
        self.module = module


class Import(Base):
    __tablename__ = "imports"
    id = Column(Integer, primary_key=True)
    import_name = Column(String, nullable=False)
    source_file_id = Column(Integer, ForeignKey("source_files.id"))
    source_file = relationship("SourceFile", back_populates="imports")

    def __repr__(self):
        return f"<Import(id={self.id}, import_name='{self.import_name}', source_file_id={self.source_file_id})>"

    def __init__(self, import_name: str, source_file: SourceFile):
        """Represents an import statement within a source code file.

        Attributes:
            import_name (str): The name of the imported module or package.
            source_file (SourceFile): The source code file in which the import appears.
        """
        self.import_name = import_name
        self.source_file = source_file


class CodeClass(Base):
    __tablename__ = "code_classes"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    docstring = Column(String)
    source_file_id = Column(Integer, ForeignKey("source_files.id"))
    source_file = relationship("SourceFile", back_populates="classes")
    methods = relationship("CodeFunction", back_populates="code_class")

    def __repr__(self):
        return f"<CodeClass(id={self.id}, name='{self.name}', source_file_id={self.source_file_id})>"

    def __init__(self, name: str, docstring: str, source_file: SourceFile):
        """Represents a class defined in a source code file.

        Attributes:
            name (str): The name of the class.
            docstring (str): The docstring of the class.
            source_file (SourceFile): The source code file in which the class is defined.
            methods (List[CodeFunction]): A list of methods within the class.
        """
        self.name = name
        self.docstring = docstring
        self.source_file = source_file


class CodeFunction(Base):
    __tablename__ = "functions"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    return_type = Column(String)
    is_top_level = Column(Boolean, default=False)
    source_file_id = Column(Integer, ForeignKey("source_files.id"))
    source_file = relationship("SourceFile", back_populates="functions")
    code_class_id = Column(Integer, ForeignKey("code_classes.id"), nullable=True)
    code_class = relationship("CodeClass", back_populates="methods")
    docstring = Column(String, nullable=True)
    valid_docstring = Column(Boolean, nullable=True)
    arguments = relationship("Argument", back_populates="function")

    def __repr__(self):
        return f"<CodeFunction(id={self.id}, name='{self.name}', return_type='{self.return_type}', source_file_id={self.source_file_id}, code_class_id={self.code_class_id})>"

    def __init__(
        self,
        name: str,
        return_type: str,
        docstring: str,
        valid_docstring: bool,
        source_file: SourceFile,
        code_class: CodeClass = None,
    ):
        """Represents a function or method within a source code file or class.

        Attributes:
            name (str): The name of the function or method.
            return_type (str): The return type of the function or method.
            return_value (str): The return value of the function or method.
            source_file (SourceFile): The source code file in which the function or method is defined.
            code_class (CodeClass): The class to which the method belongs (if any).
            arguments (List[Argument]): A list of arguments for the function or method.
        """
        self.name = name
        self.return_type = return_type
        self.source_file = source_file
        self.code_class = code_class
        self.docstring = docstring
        self.valid_docstring = valid_docstring


class Argument(Base):
    __tablename__ = "arguments"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    arg_type = Column(String)
    optional = Column(Boolean, default=False)
    function_id = Column(Integer, ForeignKey("functions.id"))
    function = relationship("CodeFunction", back_populates="arguments")

    def __repr__(self):
        return f"<Argument(id={self.id}, name='{self.name}', arg_type='{self.arg_type}', optional={self.optional}, function_id={self.function_id})>"

    def __init__(
        self, name: str, arg_type: str, optional: bool, function: CodeFunction
    ):
        """Represents an argument of a function or method.

        Attributes:
            name (str): The name of the argument.
            arg_type (str): The type of the argument.
            optional (bool): Whether the argument is optional (default=False).
            function (CodeFunction): The function or method to which the argument belongs.
        """
        self.name = name
        self.arg_type = arg_type
        self.optional = optional
        self.function = function
