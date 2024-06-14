import ast
import logging

from t_bug_catcher.utils.common import strip_path

validation_logger = logging.getLogger("t_bug_catcher")

validation_logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s - %(name)s - %(message)s")
validation_logger.addHandler(console_handler)


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


class ValidationWarning:
    """Base class to represent any type of validation warning."""

    def __init__(self, file_path: str, lineno: int, message: str, source_code: str):
        """Initializes the ValidationWarning class."""
        self.lineno = lineno
        self.message = message
        self.__source_code_lines = source_code.split("\n")
        self.code_line = self.__source_code_lines[lineno - 1]
        self.code_lines = "\n".join(self.__source_code_lines[lineno - 3 : lineno + 2])
        self.file_path = strip_path(file_path)


class BroadExceptionWarning(ValidationWarning):
    """A class to represent a broad exception warning."""

    def __init__(self, file_path: str, lineno: int, message: str, source_code: str):
        """Initializes the BroadExceptionWarning class."""
        super().__init__(file_path, lineno, message, source_code)
        self.warning_code = "TBC002"


class ConfigWarning(ValidationWarning):
    """A class to represent a config warning."""

    def __init__(self, file_path: str, lineno: int, message: str, source_code: str):
        """Initializes the ConfigWarning class."""
        super().__init__(file_path, lineno, message, source_code)
        self.warning_code = "TBC001"


class PreRunValidation:
    """A class to perform pre-run validation checks."""

    def __init__(self):
        """Initializes the PreRunValidation class."""
        self.warnings: list[ValidationWarning] = []

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
            self.warnings.append(be_warn)

    def check_configuration_exceptions(self, filename):
        """Checks for configurations warnings in the specified file."""
        pass

    def validate_file(self, filename):
        """Checks for warnings in the specified file."""
        self.check_broad_exceptions(filename)
        self.check_configuration_exceptions(filename)
