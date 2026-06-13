# 💿 Streaming Image Formats Specification

The xva-tool architecture utilizes a dynamic format pipeline (`plugins-available/formats/`) to intercept raw 1MB/16MB chunk bitstreams from the core engine and pipe them on-the-fly into specialized targets without local disk caching.

---

## 🏗️ Supported Hypervisor Targets

### 1. qcow2.py (KVM / Proxmox VE)
*   **Mechanism:** Pipes data blocks directly into `qemu-img convert -f raw -O qcow2 - target.qcow2`.
*   **Optimization:** Fully supports Copy-on-Write metadata clusters and real-time zero-block compaction.
*   **Dependencies:** Requires system `qemu-utils` to be discoverable via the active PATH environment.

### 2. vmdk.py (VMware ESXi)
*   **Mechanism:** Translates the raw block stream into standard monolithic flat VMware virtual disk allocation tables.
*   **Use Case:** Ideal for instant cross-platform infrastructure migration routines targeting vSphere pools.

### 3. vhd.py (Microsoft Hyper-V / Azure)
*   **Mechanism:** Appends a dynamic 512-byte structural geometry footer sector onto the absolute tail end of the output volume.
*   **Forensic Note:** The core reads the final sector of existing targets via backward pointer offsets to evaluate internal parent links and block allocation boundaries prior to extraction operations.

---

## 📀 Bootable Hybrid ISO Generation (iso.py)

The ISO format plugin introduces automated MBR sector detection algorithms:

1.  **Sector 0 Analysis:** As the core initiates data streaming, the ISO plugin executes a structural evaluation on the Master Boot Record.
2.  **Boot Flag Verification:** If byte `0x80` (active bootable partition marker) or a valid EFI System Partition configuration signature is detected, the plugin automatically engages El Torito hard-disk emulation parameters.
3.  **Compilation:** The engine dynamically compiles a bootable hybrid ISO media layout on-the-fly using `genisoimage` or `xorriso`. If no active boot signature is found, it falls back to generating a flat, standardized compliance Data ISO.

---

## 🛡️ Forensic Image Containers

To support Digital Forensics and Incident Response (DFIR) workflows, xva-tool hooks into secure forensic containers:

*   **e01.py (Expert Witness Format / EnCase):** Segments bitstreams into strict 64-sector data blocks protected by discrete 32-bit CRC checksum grids. Integrates investigator metadata (Case Number, Evidence ID, Examiner Name) directly into the file header.
*   **aff4.py (Advanced Forensic Format):** Modern open-source forensic container. Uses multi-stream internal compression (lz4/zlib) and native cryptographic signature blocks to secure the data integrity chain.
