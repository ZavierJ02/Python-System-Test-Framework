# **System Test Framework (Python)**

Built as a portfolio project to demonstrate how production-style

system testing frameworks are structured in Python.

A lightweight system-level test automation framework built with Python

and pytest, designed to simulate how production hardware/system testing

environments are structured.

The framework demonstrates concepts commonly used in embedded, robotics,

and large-scale software systems:

- Interface abstraction (simulated vs real device)

- Structured logging (JSON logs)

- Per-run and per-test artifacts

- Automatic snapshot capture on failure

- Trace capture for debugging

- JUnit + HTML reporting

- Retry and timeout handling

- CLI test runner

### **Architecture**

The project is organized to mirror real-world test frameworks used in

industry.

```

system\_test\_framework/

│

├─ src/

│  └─ stf/

│     ├─ interfaces/

│     │  ├─ base.py

│     │  └─ simulated\_device.py

│     │

│     ├─ reporting/

│     │  ├─ artifacts.py

│     │  ├─ logging.py

│     │  └─ metadata.py

│     │

│     └─ runner/

│        └─ run\_pytest.py

│

├─ tests/

│  └─ system/

│     ├─ test\_boot\_sequence.py

│     ├─ test\_fault\_recovery.py

│     └─ test\_long\_run\_stability.py

│

├─ configs/

│

└─ artifacts/

```

##### **Interfaces**

####  

Defines how tests communicate with the system under test

(SUT). This allows swapping a SimulatedDevice with a real hardware

interface later without changing test logic.

##### **Runner**

 

The CLI runner orchestrates test execution and generates the

artifact bundle.

Command: python -m stf.runner.run_pytest

##### **Reporting**

Handles:

- JSON structured logging

- artifact directories

- run metadata

- snapshot capture on failures

#### **Example Artifact Bundle**

Each run produces a self-contained results bundle.

```

artifacts/run-YYYYMMDD-HHMMSS/

│

├─ run.log

├─ report.html

├─ junit.xml

├─ run\_metadata.json

│

└─ tests/

   │

   ├─ test\_boot\_sequence\_device\_reaches\_ready/

   │  ├─ test.log

   │  └─ trace.txt

   │

   ├─ test\_fault\_injection\_and\_recovery/

   │  ├─ test.log

   │  └─ trace.txt

   │

   └─ test\_long\_run\_stability/

      ├─ test.log

      └─ trace.txt

```

**report.html** - Interactive test results view.

**junit.xml** - CI-compatible test results.

**run.log** - Structured JSON logs for the entire test run.

**trace.txt** - Simulated device trace captured per test.

**snapshot_on_fail.json** - Automatically generated if a test fails.

### **Tests Implemented**

##### **Boot Sequence Test**

Validates that the device transitions from BOOTING ->

READY after connection.

##### **Fault Injection and Recovery**

Injects a simulated device fault and

verifies the system correctly recovers after reset.

##### **Long-Run Stability Test**

Simulates extended system operation and verifies:

 

- No bus-off conditions occur

- Memory usage remains bounded

#### **Example Command**

Run the entire test suite:

python -m stf.runner.run_pytest

Example output:

Run dir: artifacts/run-YYYYMMDD-HHMMSS

3 passed in ~5s

### **Key Features**

##### **Structured Logging**

All logs are JSON formatted for easy parsing and

observability.

Example log entry:

{
"ts": "2026-03-04T17:03:56.982",
"level": "INFO",
"logger": "stf",
"msg": "Creating SimulatedDevice boot_time_s=0.0"
}

##### **Snapshot on Failure**

If a test fails, the framework automatically saves a

device snapshot:

snapshot_on_fail.json

Example:

{
"connected": true,
"status": "READY",
"faulted": false,
"memory_mb": 50.2
}

##### **Trace Capture**

Each test captures a device trace:

TRACE_START

CONNECT

RESET

DISCONNECT

TRACE_STOP

### **Technologies Used**

- Python

- Pytest

- pytest-timeout

- pytest-rerunfailures

- pytest-html

- YAML configuration

- Structured JSON logging

### **Purpose**

This project demonstrates how a system-level test automation framework

can be structured to support:

- hardware interfaces

- automated debugging artifacts

- repeatable CI-compatible test runs

- production-style logging and reporting

### **Design Goals**

This framework was designed to demonstrate several principles commonly used in production system-test environments:

• **Interface abstraction** – Tests interact with a device interface rather than a concrete implementation, allowing the system under test to be swapped (simulated device vs real hardware).

• **Deterministic artifact capture** – Every test run generates a reproducible bundle containing logs, traces, and snapshots to simplify debugging and post-run analysis.

• **Failure transparency** – When tests fail, the framework automatically captures the device state (`snapshot\_on\_fail.json`) and trace data to reduce time-to-diagnosis.

• **CI compatibility** – Test results are exported in JUnit XML format, enabling integration with common CI systems such as GitHub Actions, Jenkins, or Azure DevOps.

• **Reproducible test runs** – A CLI runner ensures tests are executed in a consistent environment with predictable artifact output.

### **Architecture Overview**

Tests interact with the system through a defined device interface.

```
                +----------------------+
                |      Test Cases      |
                | (pytest test suite)  |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |   Device Interface   |
                |   (base.py)          |
                +----------+-----------+
                           |
             +-------------+-------------+
             |                           |
             v                           v
    +-------------------+       +-------------------+
    | Simulated Device  |       |  Real Device      |
    | simulated_device  |       | (future)          |
    +-------------------+       +-------------------+

                           |
                           v

                +----------------------+
                | Reporting + Artifacts|
                | logs / traces / XML  |
                +----------------------+
```
