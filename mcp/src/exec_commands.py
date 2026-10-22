import json
import logging
import os
import sys
import time

from fastmcp import FastMCP

from utils import (
    run_command,
    get_process_status,
    stop_process,
)


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | scriptos | %(message)s",
    stream=sys.stderr,
)

logger = logging.getLogger("scriptos")


# ---------------------------------------------------------------------------
# MCP
# ---------------------------------------------------------------------------

mcp = FastMCP("scriptos")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_json(result):
    return json.dumps(
        result,
        indent=4,
        ensure_ascii=False,
    )


def _format_command(cmd: str, args: list[str]) -> str:
    if not args:
        return cmd

    return " ".join([cmd, *args])


# ---------------------------------------------------------------------------
# Execute command
# ---------------------------------------------------------------------------

@mcp.tool(
    name="exec_commands",
    description=(
        "Execute an operating system command synchronously or asynchronously. "
        "Use async_mode=true for long-running processes such as ng serve, "
        "npm start, docker logs, development servers, etc. "
        "Asynchronous execution returns a process_id that must be used to "
        "monitor or stop the process later."
    ),
)
def exec_tool(
    cmd: str,
    args: list[str] | None = None,
    cwd: str | None = None,
    async_mode: bool = False,
):
    """
    Execute an operating system command.

    sync:
        Blocks until the command finishes.

    async:
        Starts the process and immediately returns a process_id.
    """

    started_at = time.perf_counter()

    if args is None:
        args = []

    if cwd is None:
        cwd = os.getcwd()

    command = _format_command(cmd, args)

    logger.info(
        "COMMAND_START | mode=%s | command=%s | cwd=%s",
        "async" if async_mode else "sync",
        command,
        cwd,
    )

    try:
        result = run_command(
            cmd=cmd,
            args=args,
            cwd=cwd,
            async_mode=async_mode,
        )

        duration_ms = round(
            (time.perf_counter() - started_at) * 1000,
            2,
        )

        if async_mode:
            logger.info(
                "COMMAND_STARTED | mode=async | pid=%s | "
                "command=%s | cwd=%s | duration_ms=%s",
                result.get("process_id"),
                command,
                cwd,
                duration_ms,
            )

        else:
            logger.info(
                "COMMAND_COMPLETED | mode=sync | "
                "exit_code=%s | command=%s | "
                "duration_ms=%s",
                result.get("exit_code"),
                command,
                duration_ms,
            )

            if result.get("stdout"):
                logger.info(
                    "COMMAND_STDOUT | command=%s | stdout=%s",
                    command,
                    result["stdout"].strip(),
                )

            if result.get("stderr"):
                logger.warning(
                    "COMMAND_STDERR | command=%s | stderr=%s",
                    command,
                    result["stderr"].strip(),
                )

        return _safe_json(result)

    except Exception as exc:
        duration_ms = round(
            (time.perf_counter() - started_at) * 1000,
            2,
        )

        logger.exception(
            "COMMAND_FAILED | command=%s | cwd=%s | "
            "duration_ms=%s | error=%s",
            command,
            cwd,
            duration_ms,
            exc,
        )

        return _safe_json({
            "status": "error",
            "command": command,
            "cwd": cwd,
            "error": str(exc),
            "duration_ms": duration_ms,
        })


# ---------------------------------------------------------------------------
# Process status
# ---------------------------------------------------------------------------

@mcp.tool(
    name="get_process_status",
    description=(
        "Check the status of a process previously started with "
        "exec_commands using async_mode=true. "
        "The process_id is the operating system PID."
    ),
)
def process_status(process_id: int):

    started_at = time.perf_counter()

    logger.info(
        "PROCESS_STATUS_START | pid=%s",
        process_id,
    )

    try:
        result = get_process_status(process_id)

        duration_ms = round(
            (time.perf_counter() - started_at) * 1000,
            2,
        )

        logger.info(
            "PROCESS_STATUS_RESULT | pid=%s | status=%s | "
            "exit_code=%s | duration_ms=%s",
            process_id,
            result.get("status"),
            result.get("exit_code"),
            duration_ms,
        )

        if result.get("stdout"):
            logger.info(
                "PROCESS_STDOUT | pid=%s | stdout=%s",
                process_id,
                result["stdout"].strip(),
            )

        if result.get("stderr"):
            logger.warning(
                "PROCESS_STDERR | pid=%s | stderr=%s",
                process_id,
                result["stderr"].strip(),
            )

        return _safe_json(result)

    except Exception as exc:
        logger.exception(
            "PROCESS_STATUS_FAILED | pid=%s | error=%s",
            process_id,
            exc,
        )

        return _safe_json({
            "status": "error",
            "process_id": process_id,
            "error": str(exc),
        })


# ---------------------------------------------------------------------------
# Stop process
# ---------------------------------------------------------------------------

@mcp.tool(
    name="stop_process",
    description=(
        "Stop a process previously started asynchronously with "
        "exec_commands. The process_id is the operating system PID. "
        "Use this for cleanup after tests."
    ),
)
def process_stop(process_id: int):

    started_at = time.perf_counter()

    logger.info(
        "PROCESS_STOP_START | pid=%s",
        process_id,
    )

    try:
        result = stop_process(process_id)

        duration_ms = round(
            (time.perf_counter() - started_at) * 1000,
            2,
        )

        logger.info(
            "PROCESS_STOP_RESULT | pid=%s | status=%s | "
            "exit_code=%s | duration_ms=%s",
            process_id,
            result.get("status"),
            result.get("exit_code"),
            duration_ms,
        )

        if result.get("stdout"):
            logger.info(
                "PROCESS_STOP_STDOUT | pid=%s | stdout=%s",
                process_id,
                result["stdout"].strip(),
            )

        if result.get("stderr"):
            logger.warning(
                "PROCESS_STOP_STDERR | pid=%s | stderr=%s",
                process_id,
                result["stderr"].strip(),
            )

        return _safe_json(result)
    except Exception as exc:
        logger.exception(
            "PROCESS_STOP_FAILED | pid=%s | error=%s",
            process_id,
            exc,
        )

        return _safe_json({
            "status": "error",
            "process_id": process_id,
            "error": str(exc),
        })
