import os

from .workitems import metadata, variables


class Config:
    """Config class for configuring the application."""

    class LIMITS:
        """Limits class for configuring the application."""

        MAX_ATTACHMENTS: int = 5
        MAX_ISSUE_ATTACHMENTS: int = 100
        MAX_DESCRIPTION_LENGTH: int = 250
        SUMMARY_LENGTH: int = 120
        STACK_SCOPE: int = 3
        STACK_ITEM_LENGTH: int = 100
        STACK_TEXT_LENGTH: int = 10000

    class TICKET_PRIORITIES:
        """Priorities class for configuring the application."""

        HIGHEST: str = "1"
        HIGH: str = "2"
        MEDIUM: str = "3"
        LOW: str = "4"
        LOWEST: str = "5"

    SUPPORT_BOARD = "AB"
    BC_BOARD = "BC"

    KEYS_TO_REMOVE = ["credential", "password"]
    BUILD_INFO_FILE = "commit_info.json"

    RC_RUN_LINK = (
        f"https://cloud.robocorp.com/organizations/{os.environ.get('RC_ORGANIZATION_ID')}"
        f"/workspaces/{os.environ.get('RC_WORKSPACE_ID')}/processes"
        f"/{os.environ.get('RC_PROCESS_ID')}/runs/{os.environ.get('RC_PROCESS_RUN_ID')}/"
        f"stepRuns/{os.environ.get('RC_ACTIVITY_RUN_ID')}/"
    )

    ENVIRONMENT = (
        "robocloud"
        if not variables.get("environment") and os.environ.get("RC_PROCESS_RUN_ID")
        else variables.get("environment", "local")
    )

    if ENVIRONMENT != "local":
        STAGE = metadata.get("process", dict()).get("implementationStage", "")
        ADMIN_CODE = metadata.get("process", dict()).get("adminCode", "")
        WORKER_NAME = metadata.get("process", dict()).get("name", "")
        EMPOWER_URL = metadata.get("process", dict()).get("processRunUrl") or variables.get("processRunUrl")
    else:
        STAGE = "test"
        ADMIN_CODE = ""
        WORKER_NAME = ""
        EMPOWER_URL = ""


CONFIG = Config()
