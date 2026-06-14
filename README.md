# xva-tool

An uncompressed XVA container processing utility designed for Citrix XenServer and XCP-ng virtual machine architectures. The framework enables high-speed data extraction, live conversions, and recovery options without regional file caching.

## Features
*   **Zero-Copy Extraction:** Utilizes bitwise offset navigation to target and read disk sectors directly inside tarball structures via `f.seek()`.
*   **Stream-Driven Architecture:** Processes large virtual disks without writing intermediate files to disk, minimizing local storage I/O usage.
*   **Advisory Locking:** Implements kernel-level advisory locks via `fcntl.flock` to guarantee file integrity during concurrent processes.
*   **Pluggable Architecture:** Employs a standard directory structure for runtime extension scanning and modular component validation.
*   **Zstandard Compression:** Integrates native `zstd` piping to optimize compression and decompressions speed on high-throughput storage arrays.
*   **iSCSI Storage Transport:** Connects to remote SAN storage targets using standard Linux `iscsiadm` utilities, routing block streams without local disk caching.
*   **I/O Rate Limiting:** Enforces execution bandwidth caps via the `--throttle-mb` parameter to prevent disk I/O starvation on production nodes.
*   **Pre-Merge Verification:** Runs a non-destructive block allocation audit on the uncompressed XVA container before executing merge routines.

## Installation & Deployment
The tool is packaged for Debian (`.deb`), Red Hat (`.rpm`), and Slackware (`.txz`) distributions. Run the appropriate package manager configuration for your local environment.

## Command-Line Interface (CLI)

### 1. Evaluate Metadata
```bash
xva-tool info image.xva
```

### 2. Stream-Flatten layers to RAW
```bash
xva-tool merge image.xva target.img
```

### 3. Limited Bandwidth SAN Migration
```bash
xva-tool merge -r --throttle-mb 50 image.xva /dev/disk/by-path/iscsi-target-lun-0
```

### 4. Integrity Verification Scan
```bash
xva-tool verify image.xva --deep-scan
```

## Documentation
Extensive development, testing, and operational guides are available inside the `docs/` repository directory.

## License
Developed and maintained by Alexander Maassen (<outsider@cuci.nl>) and Google's Gemini AI. Released under the permissive terms of the MIT License.
