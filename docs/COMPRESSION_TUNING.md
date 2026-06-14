# Compression Tuning and I/O Rate Limiting

This document specifies the streaming compression pipelines and production bandwidth controls implemented within the framework.

## Zstandard (zstd) Streaming Pipeline
The `zstd.py` format extension module pipes raw block clusters directly through the multi-threaded system `zstd` binary. 

### Operational Parameters
*   `--zstd-level [1-22]`: Sets the mathematical compression level. Default is `3`.
*   `--zstd-threads [N]`: Defines the exact thread execution limits. Setting this to `0` automatically scales threads across all available physical hardware CPU cores.

---

## I/O Rate Limiting (Pacing Engine)
To shield active production workloads on shared RAID arrays or storage channels, the core framework implements an inline bandwidth throttling mechanism.

### Throughput Control
*   `--throttle-mb [N]`: Limits the maximum sequential I/O write throughput rate in Megabytes per second.
*   **Mechanism**: The controller measures the elapsed time for each processed 1MB block. If the execution velocity exceeds the defined limit, precise sub-millisecond pacing delays are enforced via thread scheduling.
