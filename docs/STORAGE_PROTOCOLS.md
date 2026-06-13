# 📂 Storage Transport Protocols & URI-Routing

xva-tool treats storage endpoints as dynamic URI abstractions. When a command target string utilizes a network schema prefix, the core passes the execution state to the matching pluggable storage driver (`plugins-available/storage/`).

---

## 🛸 URI-Routing Layout

### 1. nfs:// and nfs4:// (Network File System)
*   **Syntax:** `nfs://<host>/<export_path>/target.img`
*   **Implementation:** The plugin invokes a lightweight OS kernel mount directive on the background layer using high-performance read/write buffers.
*   **Performance:** Achieves near-native sequential hardware throughput by executing direct DMA operations across 10GbE/25GbE network interfaces with zero userspace context switching overhead.

### 2. smb:// (Windows Samba / CIFS)
*   **Syntax:** `smb://<user>:<pass>@<host>/<share_path>/target.img`
*   **Implementation:** Leverages kernel `mount -t cifs` loop wrappers to securely hook remote shared namespaces into local framework orchestration zones.

### 3. sftps:// and sshfs:// (Secure Shell FUSE)
*   **Syntax:** `sftps://<user>@<host>:<port>/<remote_path>/target.img`
*   **Implementation:** Mounts the remote target storage directory securely over an encrypted SSH tunnel using FUSE user-space abstractions (`sshfs`).
*   **Automation Rule:** Relies on pre-staged SSH public-key authentication paths (`ssh-copy-id`) to bypass interactive password constraints during background execution pipelines.

---

## 🔌 Direct Bare-Metal Flash (usb://)

The `usb.py` plugin introduces specific block-level structural security rails for raw drive writing:

1.  **Device Identification:** Automatically detects raw block device handles (e.g., `/dev/sdX` or `/dev/nvmeXnX`).
2.  **Safety Interception Guard:** Prior to flashing a single byte, the plugin scans `/proc/mounts`. If any partition on the target device is currently mounted by the operating system, execution blocks instantly, throwing a critical red alert to prevent data destruction.
3.  **Direct I/O Execution:** Opens the raw file handle with the strict kernel synchronization flag `os.O_DIRECT`. This entirely bypasses the operating system page cache layer, forcing blocks straight to physical silicone sectors to maintain raw speed and absolute mathematical write integrity.
