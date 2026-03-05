def test_boot_sequence_device_reaches_ready(device):
    status = device.get_status()
    assert status["connected"] is True
    assert status["status"] == "READY"


