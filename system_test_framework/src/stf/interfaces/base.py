from __future__ import annotations

from abc import ABC, abstractmethod

class DeviceInterface(ABC):
    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the device."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close connection to the device."""
        pass

    @abstractmethod
    def get_status(self) -> dict:
        """Retrieve the current status of the device."""
        pass

    @abstractmethod
    def snapshot(self) -> dict:
        """Take a snapshot of the device's current state."""
        pass

    @abstractmethod
    def inject_fault(self, code: str) -> None:
        """Inject a fault into the device for testing purposes."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset the device to a known good state."""
        pass

    @abstractmethod
    def start_trace(self) -> None:
        """Start collecting trace data from the device."""
        pass

    @abstractmethod
    def stop_trace(self) -> None:
        """Stop collecting trace data from the device."""
        pass

    @abstractmethod
    def read_telemetry(self) -> dict:
        """Read telemetry data from the device."""
        pass

    @abstractmethod
    def tick(self) -> None:
        """Advance the device's internal state by one tick (if applicable)."""
        pass