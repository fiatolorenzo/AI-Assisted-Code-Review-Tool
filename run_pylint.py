"""
Executes Pylint on a target Python file and returns
normalized static analysis findings.

Part of the AI-assisted code review pipeline.
"""

from analyzer.runner import run_cmd, get_code_context, get_full_code_context
import sys
import json

def run_pylint_on_path(file_path):
    pylint_code, pylint_stdout, pylint_stderr = run_cmd([
        sys.executable, "-m", "pylint",
        "--init-hook", "import sys; sys.path.insert(0, r'.')",
        file_path,
        "--output-format=json"
    ])

    pylint_findings = []

    if pylint_stdout:
        first_bracket = pylint_stdout.find("[")
        last_bracket = pylint_stdout.rfind("]")

        if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
            try:
                parsed = json.loads(pylint_stdout[first_bracket:last_bracket + 1])
            except json.JSONDecodeError:
                parsed = []
        else:
            parsed = []
    else:
        parsed = []

    severity_map = {
        "convention": "LOW",
        "refactor": "LOW",
        "warning": "MEDIUM",
        "error" : "HIGH",
        "fatal" : "HIGH"
    }

    for r in parsed:
        pylint_findings.append({
            "line": r.get("line"),
            "message-id": r.get("message-id"),
            "symbol": r.get("symbol"),
            "message": r.get("message"),
            "severity": severity_map.get(r.get("type")),
            "raw": r,
            "code_context": get_full_code_context(file_path, r.get("line") or 0, radius=1)
        })

    return pylint_findings, pylint_code, pylint_stderr, pylint_stdout
