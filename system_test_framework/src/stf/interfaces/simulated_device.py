from __future__ import annotations

import time
from dataclasses import dataclass, field

from .base import DeviceInterface

@dataclass
class SimulatedDevice(DeviceInterface):
    boot_time_s: float = 2.0
    connected: bool = field(default=False, init=False)
    status: str = field(default="DISCONNECTED", init=False)
    faulted: bool = field(default=False, init=False)
    fault_code: str | None = field(default=None, init=False)
    _trace: list[str] = field(default_factory=list, init=False, repr=False)
    bus_off_count: int = field(default=0, init=False)
    memory_mb: float = field(default=50.0, init=False)
    _ticks: int = field(default=0, init=False, repr=False)

    def connect(self) -> None:
        self.connected = True
        self.status = "BOOTING"
        time.sleep(self.boot_time_s)
        self.status = "READY"
        self._trace.append("CONNECT")

    def disconnect(self) -> None:
        self.connected = False
        self.status = "DISCONNECTED"
        self._trace.append("DISCONNECT")

    def get_status(self) -> dict:
        return {
            "connected": self.connected,
            "status": self.status
        }
    
    def snapshot(self) -> dict:
        return {
            "connected": self.connected,
            "status": self.status,
            "boot_time_s": self.boot_time_s,
            "faulted": self.faulted,
            "fault_code": self.fault_code,
            "bus_off_count": self.bus_off_count,
            "memory_mb": round(self.memory_mb, 2),
            "ticks": self._ticks,
        }
    
    def inject_fault(self, code: str) -> None:
        self.faulted = True
        self.fault_code = code
        self.status = "FAULT"
        self._trace.append(f"FAULT:{code}")

    def reset(self) -> None:
        # Reset clears fault and returns to READY if connected, otherwise DISCONNECTED
        self.faulted = False
        self.fault_code = None
        self._trace.append("RESET")
        if self.connected:
            self.status = "READY"
        else:
            self.status = "DISCONNECTED"

    def start_trace(self) -> None:
        self._trace.clear()
        self._trace.append("TRACE_START")

    def stop_trace(self) -> list[str]:
        self._trace.append("TRACE_STOP")
        return list(self._trace)
    
    def tick(self) -> None:
        # Simulate time passing / periodic updates
        self._ticks += 1

        # Simulate tiny memory drift (should stay bounded)
        self.memory_mb += 0.01

        # In a stable sim, bus-off should not happen

        self._trace.append(f"TICK:{self._ticks}")

    def read_telemetry(self) -> dict:
        return{
            "bus_off_count":self.bus_off_count,
            "memory_mb": round(self.memory_mb, 2),
            "ticks": self._ticks,
        }