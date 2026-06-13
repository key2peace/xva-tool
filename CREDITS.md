# 🎖️ Credits & Acknowledgements

The development of **xva-tool** was initiated by Alexander Maassen to solve real-world enterprise virtualization blockers, data recovery constraints, and hypervisor migration complexities. This project stands on the shoulders of foundational Unix principles and enterprise open-source specifications.

---

## 🏛️ Core Architectural References

Special credit and gratitude are extended to the developers and maintainers of the following specifications, frameworks, and utilities that heavily inspired the binary logic and operational workflows of this tool:

### 1. Citrix XenServer / Xapi Project (.xva Format)
*   **Source Reference:** XenServer Virtual Machine Installation and Template Formats Specifications.
*   **Contribution:** The foundational dual-phase layout mapping (XML RPC schema description followed by consecutive 1MB chunk configurations) provided the exact binary blueprint required to design our high-speed streaming engine.

### 2. GNU ddrescue (Data Recovery Logic)
*   **Author:** Antonio Diaz Diaz
*   **Contribution:** Inspiring the algorithmic design behind our rescue bad-sector mapping framework. The concept of maintaining a live, non-destructive bad_sectors.map file while utilizing direct O(1) mathematical skips over hardware errors is derived directly from this legendary data recovery standard.

### 3. Microsoft Virtual Hard Disk (VHD) Image Format Specification
*   **Source Reference:** Virtual Hard Disk Image Format Specification (Version 1.0).
*   **Contribution:** Provided the precise structural byte offset charts (the final 512-byte tail footer matrix) necessary to map dynamic disk geometries, parent snapshot reference links, and sector alignment bounds directly out of raw streams.

### 4. Distributed Management Task Force (DMTF OVF)
*   **Source Reference:** Open Virtualization Format Specification (DSP0243).
*   **Contribution:** Guided the compilation of the formats/ovf.py translation hook, ensuring that exported OVA envelopes successfully conform to international hypervisor import standards across VMware ESXi, KVM, and Oracle VirtualBox.

---

## 🔧 Core System Components & Libraries

We acknowledge the exceptional reliability of the native core libraries that make up the backbone of xva-tool:

*   **ncurses / Python Curses Subsystem:** For allowing us to implement the lightning-fast, zero-overhead immersive Text User Interface.
*   **Linux FUSE Layer (Filesystem in Userspace):** For facilitating zero-copy, real-time live mounts via virtual loop abstractions.
*   **Python Standard Software Foundation (v2.7):** For providing immutable underlying structural modules (fcntl, struct, tarfile, hashlib) optimized for robust, low-level binary manipulation on enterprise backend storage servers.

---

## ✒️ Main Maintenance & Authorship
*   **Project Lead Architect:** Alexander Maassen <outsider@cuci.nl>

"If I have seen further, it is by standing on the shoulders of giants." — Sir Isaac Newton
