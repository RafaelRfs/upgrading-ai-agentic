import os
import subprocess
from typing import Any


_processes: dict[int, subprocess.Popen] = {}


def run_command(
    cmd: str,
    args: list[str],
    cwd: str,
    async_mode: bool = False,
) -> dict[str, Any]:

    if not os.path.isdir(cwd):
        raise ValueError(f"Invalid directory: {cwd}")

    command = [cmd, *args]
    command_string = subprocess.list2cmdline(command)

    if async_mode:
        proc = subprocess.Popen(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=(
                subprocess.CREATE_NEW_PROCESS_GROUP
                if os.name == "nt"
                else 0
            ),
        )

        process_id = proc.pid

        _processes[process_id] = proc

        return {
            "mode": "async",
            "process_id": process_id,
            "command": command_string,
            "cwd": cwd,
            "status": "started",
        }

    proc = subprocess.run(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    return {
        "mode": "sync",
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "exit_code": proc.returncode,
        "command": command_string,
        "cwd": cwd,
        "status": "completed",
    }


def get_process_status(process_id: int) -> dict[str, Any]:

    proc = _processes.get(process_id)

    if proc is None:
        raise ValueError(
            f"Process {process_id} is not managed by scriptos."
        )

    exit_code = proc.poll()

    if exit_code is None:
        return {
            "process_id": process_id,
            "pid": process_id,
            "status": "running",
        }

    stdout, stderr = proc.communicate()

    _processes.pop(process_id, None)

    return {
        "process_id": process_id,
        "pid": process_id,
        "status": "completed",
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": stderr,
    }


def stop_process(process_id: int) -> dict[str, Any]:

    proc = _processes.get(process_id)

    if proc is None:
        raise ValueError(
            f"Process {process_id} is not managed by scriptos."
        )

    if proc.poll() is not None:
        stdout, stderr = proc.communicate()

        _processes.pop(process_id, None)

        return {
            "process_id": process_id,
            "pid": process_id,
            "status": "already_stopped",
            "exit_code": proc.returncode,
            "stdout": stdout,
            "stderr": stderr,
        }

    if os.name == "nt":
        result = subprocess.run(
            [
                "taskkill",
                "/PID",
                str(process_id),
                "/T",
                "/F",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        stdout, stderr = proc.communicate(timeout=5)

        _processes.pop(process_id, None)

        return {
            "process_id": process_id,
            "pid": process_id,
            "status": "stopped",
            "exit_code": proc.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "kill_output": result.stdout,
            "kill_error": result.stderr,
        }

    proc.terminate()

    try:
        stdout, stderr = proc.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()

    _processes.pop(process_id, None)

    return {
        "process_id": process_id,
        "pid": process_id,
        "status": "stopped",
        "exit_code": proc.returncode,
        "stdout": stdout,
        "stderr": stderr,
    }
