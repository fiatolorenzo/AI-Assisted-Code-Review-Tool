"""
Executes Pylint on a target Python file and returns
normalized static analysis findings.

Part of the AI-assisted code review pipeline.
"""
import sys
import os
import json
from run_pylint import run_pylint_on_path
from run_bandit import run_bandit_on_path
from run_radon import run_radon_on_path

pylint_findings = []
pylint_code = 0
pylint_stderr = ""
pylint_stdout = ""

bandit_findings = []
bandit_code = 0
bandit_stderr = ""
bandit_stdout = ""

radon_findings = []
radon_code = 0
radon_stderr = ""
radon_stdout = ""


def _write_match(finding, tool_name, ef, file_path):
    out = {
        "tool": tool_name,
        "file": file_path,
        "line": finding.get("line"),
        "message-id": finding.get("message-id"),
        "symbol": finding.get("symbol"),
        "message": finding.get("message"),
        "severity": finding.get("severity"),
        "code_context": finding.get("code_context")
    }
    ef.write(json.dumps(out, ensure_ascii=False) + "\n")

def _finding_message_id(finding):
    raw = finding.get("raw")
    if isinstance(raw, dict):
        mid = raw.get("message-id")
        if mid:
            return mid
    if finding.get("message-id"):
        return finding.get("message-id")
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_review.py <path_to_python_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    export_file = None

    if "--export" in sys.argv:
        index = sys.argv.index("--export")
        export_file = sys.argv[index + 1]

    if not os.path.exists(file_path):
        print(f"Error: file '{file_path}' does not exist.")
        sys.exit(2)

    if os.path.isdir(file_path):
        print(f"Error: '{file_path}' is a directory. Pass a .py file.")
        sys.exit(2)

    if not file_path.endswith(".py"):
        print(f"Warning: '{file_path}' does not end with .py — continuing anyway.")

    pylint_findings, pylint_code, pylint_stderr, pylint_stdout = run_pylint_on_path(file_path)
    bandit_findings, bandit_code, bandit_stderr, bandit_stdout = run_bandit_on_path(file_path)
    radon_findings, radon_code, radon_stderr, radon_stdout = run_radon_on_path(file_path)

    if export_file:

        expected_code = os.path.splitext(os.path.basename(file_path))[0]
        with open(export_file, "a", encoding="utf-8") as ef:
            all_tool_findings = [
                ("pylint", pylint_findings),
                ("bandit", bandit_findings),
                ("radon", radon_findings),
            ]

        matched_count = 0
        for tool_name, findings in all_tool_findings:
            for finding in findings:
                mid = _finding_message_id(finding)
                if mid == expected_code:
                    _write_match(finding, tool_name, ef)
                    matched_count += 1

        if matched_count == 0:
            print(f"WARNING: No findings matched expected code {expected_code} — "
                  f"check filename or tool output.")
        elif matched_count > 1:
            print(f"WARNING: {matched_count} findings matched {expected_code};"
                  f" appended all matches.")

    print("-------------------------------------------------")

    print("Pylint: ")
    if not pylint_findings:
        print("No findings")
    else:
        for finding in pylint_findings:
            print(f"Line {finding['line']}: {finding['message-id']} - {finding['symbol']} -"
                f" {finding['message']} ({finding.get('severity')})")

    print("-------------------------------------------------")

    print("Bandit: ")
    if not bandit_findings:
        print("No findings")
    else:
        for finding in bandit_findings:
            print(f"Line {finding['line']}: {finding['message-id']} - {finding['symbol']} -"
                  f" {finding['message']} ({finding.get('severity')})")

    print("-------------------------------------------------")

    print("Radon: ")
    if not radon_findings:
        print("No findings")
    else:
        for finding in radon_findings:
            print(f"Line {finding['line']}: CC - {finding['symbol']} - {finding['message']} -"
                  f" ({finding.get('severity')})")

    print("-------------------------------------------------")

if __name__ == "__main__":
    main()