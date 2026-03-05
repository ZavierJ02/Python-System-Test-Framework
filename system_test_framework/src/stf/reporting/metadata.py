from __future__ import annotations

import json
from pathlib import Path


def write_run_metadata(run_dir: Path) -> None:
    payload = {
        "run_dir": str(run_dir),
        "tests_dir": str(run_dir / "tests"),
    }
    (run_dir / "run_metadata.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")