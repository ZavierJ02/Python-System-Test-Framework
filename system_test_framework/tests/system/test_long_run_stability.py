import time
import pytest

@pytest.mark.flaky(reruns=0) # No retries, we want to see if it fails
def test_long_run_stability(device, test_context):
    tlog = test_context["test_logger"]

    start = time.time()
    duration_s = 5.0  # Run for 5 seconds to check stability

    first = device.read_telemetry()
    tlog.info("telemetry_start=%s", first)

    while time.time() - start < duration_s:
        device.tick() # Simulate time passing and device activity
        tel = device.read_telemetry()
        tlog.info("telemetry=%s", tel)
        time.sleep(0.2) # Sleep a bit to avoid spamming too fast

    last = device.read_telemetry()
    tlog.info("telemetry_end=%s", last)

    #Assertions: no bus-off, and memory didn't blow up
    assert last["bus_off_count"] == 0
    assert last["memory_mb"] - first["memory_mb"] < 2.0  # Memory should not have increased by more than 2MB