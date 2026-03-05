# Legacy CLI runner

from __future__ import annotations

import argparse
from pathlib import Path
import yaml

from src.stf.interfaces.simulated_device import SimulatedDevice

def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
    
def main() -> None:
    parser = argparse.ArgumentParser(description="System Test Framework (Day 1)")
    parser.add_argument("--config", default="configs/local.yaml", help="Path to YAML config")
    args = parser.parse_args()

    cfg_path = Path(args.config)
    cfg = load_config(cfg_path)

    boot_time = float(cfg.get("device", {}).get("boot_time_s", 2))

    device = SimulatedDevice(boot_time_s=boot_time)

    print("Connecting...")
    device.connect()
    print("Status after connect:", device.get_status())

    print("Disconnecting...")
    device.disconnect()
    print("Status after disconnect:", device.get_status())

if __name__ == "__main__":
    main()