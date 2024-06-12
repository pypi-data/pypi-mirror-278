"""Top-level package for t-bug-catcher."""

__author__ = """Thoughtful"""
__email__ = "support@thoughtful.ai"
# fmt: off
__version__ = '0.5.4'
# fmt: on

from .bug_catcher import (
    configure,
    report_error,
    attach_file_to_exception,
    install_sys_hook,
    uninstall_sys_hook,
)

__all__ = [
    "configure",
    "report_error",
    "attach_file_to_exception",
    "install_sys_hook",
    "uninstall_sys_hook",
]
