def test_fault_injection_and_recovery(device):
    # Inject a fault
    device.inject_fault("E42")

    status = device.get_status()
    assert status["status"] == "FAULT"

    device.reset()
    status = device.get_status()
    assert status["status"] == "READY"