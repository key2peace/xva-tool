# Framework Architecture Overview

The `xva-tool` framework consists of a deterministic core processor that interfaces with dynamic storage, format, and logging components.

## Resource Profiles
*   **SPARSE_MODE:** Triggered automatically on environments exhibiting constrained physical RAM or limited processor core allocations. The streaming framework restricts I/O buffers to 1MB bounds and explicitly invokes garbage collection cycles (`gc.collect()`) after individual block write transactions to preserve a minimal memory ceiling.
*   **PERFORMANCE_MODE:** Activated on target platforms containing 8GB of physical RAM or greater alongside multi-core processor threads. The runtime scaling mechanism automatically adjusts internal structures to utilize 16MB or 32MB buffer blocks, lowering sequential context-switching latency.

## Wiki Directory Navigation

Consult the specialized technical documentation sub-sheets to configure or develop custom plugin wrappers:
*   [Framework Core Architecture Overview](index.md) - High-Level System Architecture and Execution Lifecycles
*   [Image Formats Specification](IMAGE_FORMATS.md) - Streaming Format Conversion and Bootable ISO Logic
*   [Storage Transport Protocols](STORAGE_PROTOCOLS.md) - URI-Routing, Advisory Locking, and iSCSI SAN Transport
*   [Compression Tuning & Pacing](COMPRESSION_TUNING.md) - Multi-Threaded Zstd Pipelines and I/O Rate Limiting
*   [Integrity Auditing Specification](INTEGRITY_AUDITING.md) - Pre-Flight Verification Scans and Bad-Sector Maps
*   [Notifications & Log Aggregation](NOTIFICATIONS_LOG.md) - Webhooks, Systemd Sockets, and Remote Log Streams
*   [Recovery & Rescue Specifications](RECOVERY_RESCUE.md) - Non-Destructive Sector Skipping Specifications
