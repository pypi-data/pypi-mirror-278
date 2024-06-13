# System Monitor

System Monitor is a Python module that provides functionality for monitoring system resources and hardware information. It allows you to retrieve information about the CPU, GPU, storage, and other system components.

## Installation

You can install the System Monitor module using pip:

## Usage

Here's an example of how to use the System Monitor module:

```python
from system_monitor import performance_monitor

# Get CPU model
cpu_model = performance_monitor.cpumodel()
print(f"CPU Model: {cpu_model}")

# Get GPU model
gpu_model = performance_monitor.gpumodel()
print(f"GPU Model: {gpu_model}")

# Get storage information
storage = performance_monitor.storage()
total_storage = storage.storagetotal()
used_storage = storage.storageused()
free_storage = storage.storageleft()

print(f"Total Storage: {total_storage}")
print(f"Used Storage: {used_storage}")
print(f"Free Storage: {free_storage}")