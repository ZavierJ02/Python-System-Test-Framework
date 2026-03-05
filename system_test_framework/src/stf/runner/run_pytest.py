from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from stf.reporting.artifacts import make_run_dir


def main() -> int:
    run_dir = make_run_dir("artifacts")
    junit_path = run_dir / "junit.xml"
    html_path = run_dir / "report.html"

    env = os.environ.copy()
    env["STF_RUN_DIR"] = str(run_dir)

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        f"--junitxml={junit_path}",
        f"--html={html_path}",
        "--self-contained-html",
    ]
    print(f"Run dir: {run_dir}")
    result = subprocess.run(cmd, env=env)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())