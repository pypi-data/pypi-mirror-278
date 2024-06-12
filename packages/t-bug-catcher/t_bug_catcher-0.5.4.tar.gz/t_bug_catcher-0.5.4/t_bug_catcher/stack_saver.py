import inspect
import json
import linecache
import re
import sys
from datetime import datetime
from pathlib import Path
from types import FunctionType, ModuleType
from typing import Optional

import whispers

from .config import CONFIG
from .utils import logger
from .utils.common import Encoder, convert_keys_to_primitives, strip_path


class StackSaver:
    """A class to save the stack trace."""

    def __init__(self):
        """Initializes the StackSaver class."""
        pass

    def serialize_frame_info(self, frame_info: dict) -> dict:
        """A static method to serialize the frame info.

        Args:
            frame_info (dict): The frame info to be serialized.

        Returns:
            dict: The serialized frame info.
        """
        run_locals = convert_keys_to_primitives(frame_info["locals"]) if frame_info["locals"] else {}
        run_args = convert_keys_to_primitives(frame_info["args"]) if frame_info["args"] else {}
        serializable_frame_info = {
            "filename": frame_info["filename"],
            "function_name": frame_info["function_name"],
            "line_number": frame_info["line_number"],
            "line": frame_info["line"],
            "locals": run_locals,
            "args": run_args,
        }
        return serializable_frame_info

    @staticmethod
    def filter_variables(variables: dict) -> dict:
        """A static method to filter the variables.

        Args:
            variables (dict): The variables to be filtered.

        Returns:
            dict: The filtered variables.
        """
        if not isinstance(variables, dict):
            return variables
        else:
            local_variables = {}
            for var_name, var in variables.items():
                if re.match(r"^__\w+__$", var_name):
                    continue
                if isinstance(var, (ModuleType, FunctionType)):
                    continue
                local_variables[str(var_name)] = var
            return local_variables

    def mask_credentials(self, file_path: str) -> None:
        """A method to mask the credentials in the file.

        Args:
            file_path (str): The path of the file to be masked.

        Raises:
            Exception: If the masking fails.

        Returns:
            None
        """
        with open(file_path, "r") as f:
            filedata = f.readlines()

        config_path = Path(__file__).parent.resolve().as_posix() + "/resources/whispers_config.yml"

        args = f"-c {config_path} {file_path}"

        secrets = [secret for secret in whispers.secrets(args)]

        for index, line in enumerate(filedata):
            if not secrets:
                break

            for secret in secrets:
                if secret.key in line and secret.value in line:
                    filedata[index] = line.replace(secret.value, secret.value[:1] + "***")
                    secrets.pop(secrets.index(secret))
                    break

        if secrets:
            logger.warning("Failed to mask credentials")
            raise Exception("Failed to mask credentials")

        with open(file_path, "w") as file:
            file.writelines(filedata)

    def save_stack_trace(self, exception: Optional[Exception] = None):
        """A method to save the stack trace.

        Args:
            exception (Exception, optional): The exception to be saved. Defaults to None.

        Returns:
            Optional[str]: The path of the saved stack trace.
        """
        try:
            frames = []
            stack_details_json = []
            seen_frames = set()
            tb = exception.__traceback__ if exception else sys.exc_info()[2]
            while tb is not None:
                frame = tb.tb_frame
                if frame.f_code.co_name in seen_frames:
                    tb = tb.tb_next
                    continue
                seen_frames.add(frame.f_code.co_name)
                if "site-packages" in frame.f_code.co_filename:
                    tb = tb.tb_next
                    continue
                frames.append(frame)
                tb = tb.tb_next
            frames = frames[-CONFIG.LIMITS.STACK_SCOPE :]

            for frame in frames:
                frame_info = {
                    "filename": strip_path(frame.f_code.co_filename),
                    "function_name": frame.f_code.co_name,
                    "line_number": frame.f_lineno,
                    "line": linecache.getline(frame.f_code.co_filename, frame.f_lineno).strip(),
                    "locals": self.filter_variables(frame.f_locals),
                    "args": self.filter_variables(inspect.getargvalues(frame)[3]),
                }
                stack_details_json.append(self.serialize_frame_info(frame_info))

            file_path = f"stack_details_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"

            with open(file_path, "w") as f:
                json.dump(stack_details_json, f, indent=4, cls=Encoder)

            self.mask_credentials(file_path)

            return file_path
        except Exception as e:
            logger.warning(f"Failed to save stack trace: {e}")
            return
