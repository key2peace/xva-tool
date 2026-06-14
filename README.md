# 🛠️ xva-tool

```text
██╗  ██╗██╗   ██╗ █████╗ ████████╗ ██████╗  ██████╗ ██╗     
╚██╗██╔╝██║   ██║██╔══██╗╚══██╔══╝██╔═══██╗██╔═══██╗██║     
 ╚███╔╝ ██║   ██║███████║   ██║   ██║   ██║██║   ██║██║     
 ██╔██╗ ╚██╗ ██╔╝██╔══██║   ██║   ██║   ██║██║   ██║██║     
██╔╝ ██╗ ╚████╔╝ ██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗
╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
```

An advanced, production-grade, zero-copy streaming infrastructure utility for Citrix XenServer / Xapi (.xva/.ova) virtual machine architecture. Built natively for maximum speed, memory optimization (~30MB blueprint footprint), cryptographic safety, and seamless multi-platform hypervisor migration pipelines.

![Retro Curses Main Dashboard](docs/images/tui_main_dashboard.png)
*Screenshot instruction: Run xva-tool without arguments. Capture the terminal showing the full blue Text User Interface with core subcommand choices.*

---

## 🖥️ Retro Curses Interactive TUI
When executed without any explicit command-line arguments in an interactive shell, xva-tool automatically launches an immersive retro-style Text User Interface (TUI) built on top of native curses. Navigate with arrow keys, use SPACE to live-toggle plugins, and hit ENTER to deploy complex recovery and orchestration processes.

---

## 🎯 Key Features

* ⚡ Fixed-Grid Zero-Copy Extraction:** Leverages bitwise mathematics (`idx >> 3`) to target and read precise disk sectors inside uncompressed tarballs instantaneously via `f.seek()`, optimizing I/O.
* 💾 Stream-Driven Engine: Processes 64GB+ virtual disks without caching files to disk, eliminating redundant I/O write wear on high-throughput RAID arrays.
* 🔒 Intelligent Advisory Locking: Implements kernel-level advisory locks via fcntl.flock to guarantee resource integrity and prevent concurrent modifications.
* 📂 Pluggable Module Architecture: Incorporates an industry-standard plugins-available/plugins-enabled directory topology supporting dynamic lazy loading and environment self-verification.
* 🧱 Multi-Format Target Pipeline: On-the-fly streaming conversion to raw .img, Proxmox qcow2, VMware vmdk, Hyper-V vhd, Expert Witness Format E01, AFF4, and bootable hybrid ISO media.
* 🛸 Elastic Hardware Auto-Discovery: Dynamic system evaluation that auto-scales internal buffer blocks between SPARSE_MODE (1MB chunking for legacy/recovery environments) and PERFORMANCE_MODE (16MB chunking for modern high-end RAID servers).
* 🏗️ 3-Tier Cascade Configuration: Parses configuration parameters progressively from System (/etc), User (~/.config), and Local (./.xva-tool.conf) namespaces.
* 🔎 Forensic Sparse Hole Protection: Employs an in-memory bitmask index to instantly return null-byte blocks (\0) for omitted empty sectors, bypassing disk calls entirely.
* 🩹 Proactive Autonomous Repair: Advanced troubleshooting engine that intercepts environment errors and proposes actionable, copy-paste or automatic apt/yum/pip remedies.
* 🛡️ Secure Command Validation: 100% immune to command injection flaws by enforcing array-string argument arrays instead of raw shell lines.

---

## 📁 System Topology & Architecture

To maintain modularity, the framework deploys the following directory structures:

```text
/etc/xva-tool/               # Global Configuration Cascade Space
├── conf-available/          # Instantiated configuration variants (log, storage, formats)
└── conf-enabled/            # Active configuration symlinks (e.g., 10-global.conf)

/usr/share/xva-tool/         # Global Dynamic Plugin Space
├── plugins-available/       # Fused source engines (log, storage, formats, commands)
└── plugins-enabled/         # Active orchestration subcommand symlinks

~/.config/xva-tool/          # User Configuration Cascade Space
~/.local/share/xva-tool/     # User Dynamic Plugin Space
./.xva-tool.conf             # Local/Project override file mapping (Highest priority)
```

---

## 🚀 Command-Line Interface (CLI)

`xva-tool` splits gracefully between its interactive desktop environment and a deterministic, non-interactive scriptable CLI engine. The universal `-f` / `--force` flag bypasses all interactive barriers, executing silent automated permission loops.

### 1. Inspect Archive Architecture
```bash
xva-tool info mainvm.xva
```
Outputs vital hypervisor descriptions, parses matching internal storage references, and evaluates the trailing bytes of the tarball to determine if an archive is structurally complete or truncated.

### 2. Stream-Merge Raw Disk Images
```bash
xva-tool merge -r mainvm.xva target.img
```
Extracts and flattens chunk layers directly into a single raw .img loop file. Incorporates the -r / --resume atomic block checker to seamlessly resume broken or interrupted extractions.

### 3. Forensic Dual-Hashing Extraction
```bash
xva-tool rescue corrupt.xva target.img
```
Advanced GNU ddrescue-inspired file recovery pipeline. Skips bad sectors, logs errors onto logs/bad_sectors.map, and computes MD5, SHA-1, and SHA-256 hashes on-the-fly, dumping a sidecar .meta file upon completion.

### 4. Advanced Network Plugin Management
```bash
xva-tool plugin install custom_plugin.tar.gz
```
Unified package manager layer. Opens the bundle, cryptographically cross-examines the SHA-256 code signature against the manifest.meta, auto-resolves missing Python libraries via user-space pip (--user), and prompts for live symbolic link activation.

### 5. Live Toggle Plugin States
```bash
xva-tool plugin enable storage/nfs
```
Creates the required relative symbolic link to instantly shift the NFS kernel mount engine from a sleeping state into production-active status across the CLI and TUI loops.

```bash
xva-tool plugin disable formats/qcow2
```
Safely severs the active symbolic link layer for the QCOW2 format plugin, rendering the conversion pipeline sleeping without purging the underlying available codebase source files.

---

## 🛠️ Automated Package Distribution

`xva-tool` is engineered to adapt flawlessly to any deployment layout. It supports the following distribution standards out-of-the-box:
1. Pip Package (setup.py / MANIFEST.in): Install universally into paths via pip install git+https://github.com --user.
2. Debian Package (.deb): Complete automated compilation bindings for native, apt-compliant deployment pipelines on Debian, Ubuntu, and Proxmox VE.
3. Red Hat Package (.rpm): Formal spec layout targeting enterprise architectures like RHEL, CentOS, and Rocky Linux.
4. Slackware Archive (.txz): Native pkg-compliant deployment maps conforming to Slackware design conventions.
5. Docker Container (Dockerfile): Fully isolated, privileged container layers (--privileged) optimized for instant cloud orchestration execution.

---

## ⚙️ Configuration Properties (xva-tool.conf.example)

Configure global or command-specific properties using clean INI definitions. Copy xvatool.conf.example to .xva-tool.conf or /etc/xva-tool/conf-available/global.conf to configure.

---

## Documentation Wiki Pages
Extensive architectural, development, and operational guides are located inside the docs/ repository space:
*   [Framework Core Architecture Overview](docs/index.md)
*   [Streaming Conversions and Bootable ISO Logic](docs/IMAGE_FORMATS.md)
*   [URI-Routing, Advisory Locking, and Block Writes](docs/STORAGE_PROTOCOLS.md)
*   [Webhooks, Push Alerts, and Kernel Log Aggregation](docs/NOTIFICATIONS_LOG.md)
*   [Non-Destructive Sector Skipping Specifications](docs/RECOVERY_RESCUE.md)

---

## License & Integrity
Designed for data recovery, forensic auditing, and high-performance cross-platform system migrations. Developed and maintained by Alexander Maassen (<outsider@cuci.nl>). Licensed under the permissive terms of the MIT License.

