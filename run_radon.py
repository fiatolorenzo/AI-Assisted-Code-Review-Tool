"""
Executes Radon complexity analysis on a Python file and
returns normalized cyclomatic complexity findings.

Part of the AI-assisted code review pipeline.
"""

from analyzer.runner import run_cmd, get_full_code_context
import sys
import json

def run_radon_on_path(file_path):
    radon_code, radon_stdout, radon_stderr = run_cmd([
        sys.executable, "-m", "radon", "cc", "-s", "-j", file_path
    ])


    if radon_code != 0:
        return [], radon_code, radon_stderr, radon_stdout

    radon_findings = []


    try:
        parsed = json.loads(radon_stdout) if radon_stdout else {}
    except json.JSONDecodeError:
        return [], radon_code, radon_stderr, radon_stdout

    results = []
    if isinstance(parsed, dict):
        for v in parsed.values():
            if isinstance(v, list):
                results.extend(v)
            elif isinstance(v, dict):
                results.append(v)
            else:
                continue
    elif isinstance(parsed, list):
        results.extend(parsed)
    else:
        return [], radon_code, radon_stderr, radon_stdout

    for r in results:
        if not isinstance(r, dict):
            continue
        line = r.get("lineno") or r.get("line") or 0
        rank = r.get("rank")
        complexity = r.get("complexity")
        typ = r.get("type") or "<unknown>"
        name = r.get("name") or "<unknown>"
        
        normalized_id = f"CC_{rank}2"
        
        if rank in ("A", "B"):
            severity = "LOW"
        elif rank == "C":
            severity = "MEDIUM"
        else:
            severity = "HIGH"

        radon_findings.append({
            "line": line,
            "message-id": normalized_id,
            "symbol": "cyclomatic_complexity",
            "message": f"Cyclomatic complexity {complexity} (rank {rank}) in {typ} {name}",
            "severity": severity,
            "raw": r,
            "code_context": get_full_code_context(file_path, line or 0, radius=100)
        })

    return radon_findings, radon_code, radon_stderr, radon_stdout
