# 🏛️ xva-tool Core Architecture Overview

Welcome to the technical documentation wiki for **xva-tool**. This framework is engineered by Alexander Maassen (<outsider@cuci.nl>) to provide high-speed, zero-copy, stream-driven orchestration for Citrix XenServer (XVA/OVA) virtual machine images.

---

## 🔬 Core Design Philosophy

The primary objective of xva-tool is to eliminate unnecessary disk I/O bottlenecks and local storage clutter during hypervisor extraction, backup validation, and format conversion loops.

The architecture is strictly divided into two distinct components:
1.  **The Pure Core Engine:** A standalone, zero-dependency Python 2.7 executable responsible for handling low-level binary tarball streaming, XML parsing metadata extraction, advisory file locking, and raw image writing (XVA -> RAW).
2.  **The Pluggable Module Architecture:** A dynamic extension layer (`plugins-available/` and `plugins-enabled/`) that lazily loads additional image formats (qcow2, vmdk, vhd, iso, e01, aff4), storage transport protocols (nfs, smb, sftp, usb), logging configurations, and notification hooks.

---

## ⚡ Adaptive Resource Allocation

Upon execution, the framework core automatically interrogates the host operating system kernel layers via `/proc/meminfo` to dynamically establish internal buffering models:

### 1. SPARSE_MODE
*   **Trigger Condition:** Host system exhibits less than 8GB of total available physical RAM or runs on a single CPU core.
*   **Behavior:** The I/O streaming grid is locked to strict **1MB chunk block constraints**. Python's garbage collection cycle (`gc.collect()`) is aggressively invoked manually after every individual block write transaction to maintain an unyielding **~30MB memory ceiling**.

### 2. PERFORMANCE_MODE
*   **Trigger Condition:** Host system exhibits 8GB of total physical RAM or greater alongside multi-core processor threads.
*   **Behavior:** The I/O loop automatically scales buffer boundaries up to **16MB or 32MB chunks**. This drops sequential context-switching overhead and maximizes sequential write performance on high-throughput NVMe RAID storage sets, resulting in an immediate 3x to 4x speed optimization.

---

## 🔒 Transactional Guard Rails

To ensure forensic integrity and system reliability under multi-user production workloads, xva-tool enforces two kernel-level protective rings:

*   **Advisory File Locking (`fcntl.flock`):** Prior to initiating any write sequence, the core demands an exclusive kernel lock (`LOCK_EX | LOCK_NB`) on the target resource. If another administrative task or background cronjob is accessing that file, execution halts instantly to avoid block-level intersection corruption.
*   **POSIX Signal Interception:** A centralized signal router maps critical Unix interrupts (`SIGINT`, `SIGTERM`, `SIGHUP`, `SIGPIPE`, `SIGQUIT`). If an operator aborts a running transfer via `Ctrl+C`, the handler intercepts the state, flushes active binary buffers, breaks curses layout states cleanly, releases all `fcntl` locks, and frees RAM buffers before exiting safely.

---

## Wiki Directory Navigation

Consult the specialized technical documentation sub-sheets to configure or develop custom plugin wrappers:
*   [Image Formats Specification](IMAGE_FORMATS.md) - Streaming Format Conversion and Bootable ISO Logic
*   [Storage Transport Protocols](STORAGE_PROTOCOLS.md) - URI-Routing, Advisory Locking, and Network Mounts
*   [Notifications & Log Aggregation](NOTIFICATIONS_LOG.md) - Webhooks, Systemd Sockets, and Remote Log Streams
*   [Recovery & Rescue Specifications](RECOVERY_RESCUE.md) - Non-Destructive Sector Skipping Specifications

