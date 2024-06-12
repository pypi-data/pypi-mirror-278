import ast
import logging
import os

from t_bug_catcher.utils.common import strip_path

validation_logger = logging.getLogger("t_bug_catcher")

validation_logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s - %(name)s - %(message)s")
validation_logger.addHandler(console_handler)

EXCLUDED_DIRS = [".venv", "venv", "site-packages"]


class IncorrectTryBlockVisitor(ast.NodeVisitor):
    """A visitor that checks for incorrect try-except blocks."""

    def __init__(self):
        """Initializes the IncorrectTryBlockVisitor class."""
        self.errors = {}

    def visit_Try(self, node):
        """Visits the try-except block in the AST."""
        message = (
            "Error not handled: specify the error type or re-raise exception or "
            "report it with `t_bug_catcher.report_error()`"
        )
        for handler in node.handlers:
            if isinstance(handler.type, ast.Name) and handler.type.id == "Exception":
                if not self._contains_raise(handler.body) and not self._contains_correct_error_handling(handler.body):
                    self.errors[handler.lineno] = message
            elif handler.type is None:  # 'except:' that catches everything
                if not any(isinstance(x, ast.Raise) for x in handler.body):
                    self.errors[handler.lineno] = message
        self.generic_visit(node)

    @staticmethod
    def _contains_correct_error_handling(statements):
        for stmt in statements:
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                func = stmt.value.func
                if (isinstance(func, ast.Name) and func.id == "report_error") or (
                    isinstance(func, ast.Attribute) and func.attr == "report_error"
                ):
                    return True
        return False

    @staticmethod
    def _contains_raise(statements):
        return any(isinstance(stmt, ast.Raise) for stmt in statements)

    def get_errors(self):
        """Returns the errors found in the try-except blocks."""
        return self.errors


class BroadExceptionWarning:
    """A class to represent a broad exception warning."""

    def __init__(self, file_path: str, lineno: int, message: str, source_code: str):
        """Initializes the BroadExceptionWarning class."""
        self.lineno = lineno
        self.message = message
        self.__source_code_lines = source_code.split("\n")
        self.code_line = self.__source_code_lines[lineno - 1]
        self.code_lines = "\n".join(self.__source_code_lines[lineno - 3 : lineno + 2])
        self.file_path = strip_path(file_path)


class PreRunValidation:
    """A class to perform pre-run validation checks."""

    def __init__(self):
        """Initializes the PreRunValidation class."""
        self.broad_exception_warnings: list[BroadExceptionWarning] = []
        self.analyze_project(os.getcwd())
        self.log_warnings()

    def analyze_project(self, project_dir: str):
        """Analyzes the project directory for broad exception warnings."""
        for root, dirs, files in os.walk(project_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)

                    self.check_broad_exceptions(file_path)

    def check_broad_exceptions(self, filename):
        """Checks for broad exception warnings in the specified file."""
        with open(filename, "r", encoding="utf8") as source:
            source_code = source.read()
            try:
                tree = ast.parse(source_code, filename=filename)
            except SyntaxError:
                return
            except Exception as ex:
                validation_logger.error(f"Unable to validate: {filename} - {ex}")
                return

        visitor = IncorrectTryBlockVisitor()
        visitor.visit(tree)

        for line, message in visitor.get_errors().items():
            be_warn = BroadExceptionWarning(filename, line, message, source_code=source_code)
            self.broad_exception_warnings.append(be_warn)

    def log_warnings(self):
        """Logs the broad exception warnings."""
        for be_warn in self.broad_exception_warnings:
            validation_logger.warning(f"{be_warn.file_path}:{be_warn.lineno}: {be_warn.message}")

    @property
    def errors_count(self):
        """Property to define the number of errors. Used for pre-commit hook."""
        return len(self.broad_exception_warnings)


PRE_RUN_VALIDATION = PreRunValidation()
