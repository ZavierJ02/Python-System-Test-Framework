from __future__ import annotations

from datetime import datetime
from pathlib import Path

def make_run_dir(base_dir: str = "artifacts") -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = Path(base_dir) / f"run-{ts}"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir

def sanitize_test_name(nodeid: str) -> str:
    # Example nodeid: "tests/system/test_boot_sequence.py::test_boot_sequence_device_reaches_ready"
    name = nodeid.replace("::", "__").replace("/", "_").replace("\\", "_").replace(".py", "")
    # Keep it short-ish and filesystem-friendly
    return name

def make_test_dir(run_dir: Path, nodeid: str) -> Path:
    test_name = sanitize_test_name(nodeid)
    test_dir = run_dir / "tests" / test_name
    test_dir.mkdir(parents=True, exist_ok=True)
    return test_dir