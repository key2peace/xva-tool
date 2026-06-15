# XVA-TOOL - Plugin API Reference
Welcome to the automated plugin reference. This documentation is generated directly from the source code docstrings and structural metadata. **Do not modify this file manually.**

## extract (`commands`)
**Summary:** Unpack an uncompressed XVA container into a structured directory of 1MB blocks.

### Developer Specifications
```text
XVA-TOOL Plugin: Command - Container Extraction Engine

This module implements the low-level extraction process for uncompressed
XVA containers. It processes the internal tarball stream, extracts individual
1MB binary disk segments sequentially, and recreates the path layouts.

Developer Specifications:
    - Entry Hook: Execute command invocation with target payload pathways.
    - Interactive Layer: Optional user-confirmation block per processed chunk.
    - Performance Layer: Enforces periodic garbage collection routines.
```
---

## info (`commands`)
**Summary:** Extract and display structural XML metadata from a target XVA container.

### Developer Specifications
```text
XVA-TOOL Plugin: Command - Information Extraction

This module implements the structural metadata analysis for uncompressed
XVA containers. It hooks into the main execution cycle to parse the leading
'ova.xml' descriptor without executing a full container extraction loop.

Developer Specifications:
    - Entry Hook: Execute command invocation with parsed namespace arguments.
    - Expected State: Valid read-binary descriptor targeting a local target file.
    - Thread Behavior: O(1) synchronous metadata block extraction.

Exposed Variables:
    - pl (dict): System metadata tracking array containing module type,
		 classification name, and CLI help bindings.
```
---

## merge (`commands`)
**Summary:** Slam and merge 1MB container chunks into a unified raw disk image.

### Developer Specifications
```text
XVA-TOOL Plugin: Command - Zero-Copy Block Merge Engine

This module contains the core streaming loop responsible for rebuilding
uncompressed 1MB chunk configurations into a unified, flat raw disk image (.raw).
It respects memory boundaries mapped out during the core bootstrap phase.

Developer Specifications:
    - Entry Hook: Triggers binary data rebuilding loops over extracted folders.
    - Memory Boundaries: Automatically scales block caching arrays from 1MB
			 (SPARSE_MODE) up to 32MB chunks (PERFORMANCE_MODE).
    - I/O Hardening: Utilizes explicit garbage collection loops and strict
		     sequential chunk resolution to guarantee absolute stability.
```
---

## pack (`commands`)
**Summary:** Assemble and seal a raw directory of chunks back into a deployment XVA container.

### Developer Specifications
```text
XVA-TOOL Plugin: Command - Container Packaging Engine

This module reverses the extraction sequence by marshaling an active directory
of 1MB raw data chunks back into a standardized uncompressed XVA file schema,
rebuilding the critical 'ova.xml' header descriptor in the process.

Developer Specifications:
    - Entry Hook: Compiles specific block arrays into target package envelopes.
    - Layout Hardening: Asserts chronological indexing integrity per data stream.
    - Performance Layer: Synchronizes block tracking states with memory boundary profiles.

Exposed Variables:
    - pl (dict): System metadata tracking array containing module type,
		 classification name, and CLI help bindings.
```
---

## rescue (`commands`)
**Summary:** Carve, salvage, and recover uncompressed data blocks from damaged containers.

### Developer Specifications
```text
XVA-TOOL Plugin: Command - Forensic Block Rescue Engine

This module executes low-level byte carving and alignment repairs over
damaged or incomplete uncompressed XVA containers. It intercepts corrupt
headers to recover isolated data fragments and enforce data reconstruction.

Developer Specifications:
    - Entry Hook: Initiates stream carving and structural integrity validation.
    - Resiliency Focus: Bypasses native EOF dropouts to extract orphan segments.
    - Audit Trail: Forces precise positional error capturing inside local logs.

Exposed Variables:
    - pl (dict): System metadata tracking array containing module type,
		 classification name, and CLI help bindings.
```
---

## aff4 (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic AFF4 forensic format extension module.
Pipes and compresses raw block streams into cryptographically signed open containers.
```
---

## e01 (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic E01 forensic format extension module.
Pipes and compresses raw block streams into legally sound EnCase evidence files.
```
---

## iso (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic ISO compilation format extension module.
Evaluates Sector 0 binary structures on-the-fly to trigger El Torito boot emulation.
```
---

## ovf (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic OVF/OVA conversion format extension module.
Wraps raw disk allocations alongside generated OVF XML descriptors into USTAR tarballs.
```
---

## qcow2 (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic QCOW2 stream format extension module.
Pipes raw block clusters on-the-fly into qemu-img without local caching.
```
---

## vhdx (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic VHDX stream format extension module.
Pipes raw block clusters directly into Hyper-V compliant targets via qemu-img.
```
---

## vmdk (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic VMDK stream format extension module.
Pipes raw block clusters directly into VMware-compliant targets via qemu-img.
```
---

## zstd (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic Zstandard stream format extension module.
Pipes raw block clusters on-the-fly through multi-threaded zstd binaries.
```
---

## apprise (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic Apprise logging and notification hub extension module.
Lazy-loads the apprise library backend to grant access to 80+ alerting endpoints.
```
---

## file (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic local file logging extension module.
Handles automated permission downgrades and runtime file rotation size limits.
```
---

## journald (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic systemd journal extension module.
Pipes structured orchestration logs directly into the Linux systemd socket.
```
---

## syslog (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic remote syslog extension module.
Dispatches structured logging frames over UDP or TCP to central SIEM nodes.
```
---

## csv (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic CSV reporting extension module.
Generates flat-table delimited spreadsheets tracking extraction metadata bounds.
```
---

## forensic (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic DFIR audit report extension module.
Compiles structurally verifiable cryptographic and environment metadata logs.
```
---

## html (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic HTML reporting extension module.
Compiles a self-contained, responsive bootstrap-styled visualization dashboard.
```
---

## json (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic JSON reporting extension module.
Generates RFC-compliant JSON objects optimized for centralized SIEM ingestors.
```
---

## pdf (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic PDF reporting extension module.
Compiles unmodifiable, compliance-ready executive PDF documents via ReportLab.
```
---

## xml (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic XML reporting extension module.
Generates structured, compliance-ready XML nodes tracking core data execution steps.
```
---

## iscsi (`storage`)
**Summary:** Stream raw container blocks directly from an enterprise remote iSCSI target LUN.

### Developer Specifications
```text
XVA-TOOL Plugin: Storage - Enterprise iSCSI Target Handler

This module orchestrates remote raw block storage streams straight from
iSCSI Storage Area Networks (SAN). It wraps around system 'iscsiadm' loops
to detect, log in, and expose remote LUN targets as local block devices.

Developer Specifications:
    - Module Class: storage
    - System Dependencies: open-iscsi package binary availability.
    - Security Isolation: Requires careful execution context separation
			   to prevent credential leakages into logs.
```
---

## local (`storage`)
**Summary:** Read and write uncompressed chunks directly from/to a local POSIX directory.

### Developer Specifications
```text
XVA-TOOL Plugin: Storage - Local File System Target

This module implements the standard file system I/O abstraction layer.
It hooks into the storage engine to validate local directories and read/write
raw binary chunks without utilizing external network protocols.

Developer Specifications:
    - Module Class: storage
    - Operational Focus: POSIX compliant block operations.
    - Performance Layer: Zero-copy read/write loops synchronized with the core.
```
---

## nfs (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic NFS network transport extension module.
Automates secure kernel space mount routing abstractions with forensic cleanup.
```
---

## sftp (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic SFTP network transport extension module using SSHFS FUSE.
Automates secure encrypted storage routing abstractions with signal cleanup guards.
```
---

## smb (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic SMB/Samba network transport extension module.
Automates secure CIFS kernel mounts with credentials isolation and forensic cleanup.
```
---

## usb (`unknown`)
**Summary:** No help text provided.

### Developer Specifications
```text
Dynamic USB/Raw block flash transport module.
Enforces strict multi-tier mount verification and direct kernel O_DIRECT writes.
```
---

