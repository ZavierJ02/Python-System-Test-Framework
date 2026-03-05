import logging

from stf.reporting.artifacts import make_run_dir, make_test_dir
from stf.reporting.logging import setup_file_logger, JsonLineFormatter
from stf.reporting.metadata import write_run_metadata


from pathlib import Path
import os

import pytest
import yaml

from stf.interfaces.simulated_device import SimulatedDevice

def load_test_config() -> dict:
    cfg_path = os.getenv("STF_TEST_CONFIG", "tests/configs/test.yaml")
    path = Path(cfg_path)
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
    
@pytest.fixture(scope="session")
def run_context():
    run_dir = Path(os.getenv("STF_RUN_DIR", str(make_run_dir("artifacts"))))
    logger = setup_file_logger(run_dir / "run.log", level="INFO", json_lines=True)
    write_run_metadata(run_dir)
    logger.info("Starting test session")
    return {"run_dir": run_dir, "logger": logger}


@pytest.fixture
def test_context(request, run_context):
    run_dir = run_context["run_dir"]
    test_dir = make_test_dir(run_dir, request.node.nodeid)

    #Create a dedicated logger for this test file
    test_logger = logging.getLogger(f"stf.{request.node.nodeid}")
    test_logger.setLevel(logging.INFO)
    test_logger.handlers.clear()  # Clear existing handlers

    fh = logging.FileHandler(test_dir / "test.log", encoding="utf-8")
    fh.setFormatter(JsonLineFormatter())
    test_logger.addHandler(fh)

    test_logger.info("Starting test %s", request.node.nodeid)

    request.node.stf_test_dir = test_dir  # Attach test_dir to the node for later use

    return {"test_dir": test_dir, "test_logger": test_logger}

@pytest.fixture
def device(request, run_context, test_context):
    logger = run_context["logger"]
    tlog = test_context["test_logger"]

    cfg = load_test_config()
    boot_time = float(cfg.get("device", {}).get("boot_time_s", 0))

    logger.info("Creating SimulatedDevice boot_time_s=%s", boot_time)
    tlog.info("boot_time_s=%s", boot_time)

    d = SimulatedDevice(boot_time_s=boot_time)
    request.node.stf_device = d  # Attach device to the node for later use
    d.start_trace()
    d.connect()
    tlog.info("connected status=%s", d.get_status())

    yield d

    d.disconnect()
    tlog.info("disconnected status=%s", d.get_status())

    trace_lines = d.stop_trace()
    trace_path = test_context["test_dir"] / "trace.txt"
    trace_path.write_text("\n".join(trace_lines) + "\n", encoding="utf-8")
    tlog.info("wrote trace file=%s", trace_path)

import json

def pytest_runtest_makereport(item, call):
    # Called for each phase: setup/call/teardown. We only care about the call phase (the test function execution)
    if call.when != "call":
        return
    
    outcome = call.excinfo
    if outcome is None:
        return # Test passed, no exception info
    
    test_dir = getattr(item, "stf_test_dir", None)
    device = getattr(item, "stf_device", None)
    if test_dir is None or device is None:
        return # We don't have the context we need to save artifacts
    
    snapshot_path = test_dir / "snapshot_on_fail.json"
    try:
        snap = device.snapshot()
        snapshot_path.write_text(json.dumps(snap, indent=2), encoding="utf-8")
    except Exception as e:
        # Last resort: write error to a text file
        (test_dir / "snapshot_error.txt").write_text(str(e), encoding="utf-8")

    