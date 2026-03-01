"""
Executes Bandit security analysis on a Python file and
returns normalized vulnerability findings.

Part of the AI-assisted code review pipeline.
"""

from analyzer.runner import run_cmd, get_code_context
import sys
import json

def run_bandit_on_path(file_path):
    bandit_code, bandit_stdout, bandit_stderr = run_cmd([
        sys.executable, "-m", "bandit",
        file_path,
        "-f", "json"
    ])

    bandit_findings = []

    try:
        parsed = json.loads(bandit_stdout) if bandit_stdout else {}
    except json.JSONDecodeError:
        parsed = {}

    raw_results = parsed.get("results", [])

    for r in raw_results:
        bandit_findings.append({
            "line": r.get("line_number"),
            "message-id": r.get("test_id"),
            "symbol": r.get("test_name"),
            "message": r.get("issue_text"),
            "severity": r.get("issue_severity"),
            "confidence": r.get("issue_confidence"),
            "raw": r,
            "code_context": get_code_context(file_path, r.get("line_number") or 0, radius=1)
        })

    return bandit_findings, bandit_code, bandit_stderr, bandit_stdout
