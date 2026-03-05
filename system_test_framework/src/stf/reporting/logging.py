from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

class JsonLineFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        return json.dumps(payload)

def setup_file_logger(log_path: Path, level: str = "INFO", json_lines: bool = True) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger("stf")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.handlers.clear()  # Clear existing handlers


    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    if json_lines:
        fmt = JsonLineFormatter()
    else:
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)

    logger.addHandler(fh)

    
    return logger

