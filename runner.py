"""Utilities for running external analysis tools and capturing their output"""
import subprocess
import sys
import typing
import shlex

def run_cmd(cmd: typing.Union[typing.List[str], str]) -> typing.Tuple[int, str, str]:
    """Runs an external command and captures its output
       cmd: the command to execute
       Returns (int, str, str)"""
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def get_code_context(file_path, lineno, radius=1):
    """
    Returns a list of source lines around `lineno` (1-based).
    radius=1 returns [line-1, line, line+1] when available.
    Returns [] on any error.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        idx = max(0, lineno - 1)
        start = max(0, idx - radius)
        end = min(len(lines), idx + radius + 1)
        return [lines[i].rstrip("\n") for i in range(start, end)]
    except Exception:
        return []

def get_full_code_context(file_path: str, lineno: int, radius: int = 3, full_file_threshold: int = 8):
    """
    Return a list of source lines to use as code_context.

    - If file length <= full_file_threshold: return entire file.
    - Else: return lines [lineno-radius .. lineno+radius] (1-based lineno).
    - Trim leading/trailing blank lines from the returned context.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [ln.rstrip("\n") for ln in f]
        n = len(lines)
        # convert to 0-based index, clamp
        idx = max(0, min(n - 1, lineno - 1))

        if n <= full_file_threshold:
            start, end = 0, n  # end is exclusive
        else:
            start = max(0, idx - radius)
            end = min(n, idx + radius + 1)

        context = lines[start:end]

        # Trim leading/trailing blank lines to avoid noisy empty strings
        while context and context[0].strip() == "":
            context.pop(0)
        while context and context[-1].strip() == "":
            context.pop()

        return context
    except Exception:
        return []
