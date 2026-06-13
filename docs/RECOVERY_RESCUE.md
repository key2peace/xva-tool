# 🩹 Non-Destructive Sector Skipping & Recovery Specifications

When handling corrupted data backups, degraded RAID arrays, or failing physical storage blocks, traditional utilities crash abruptly with unhandled `IOError` states. xva-tool implements an advanced, GNU ddrescue-inspired non-destructive data recovery pipeline via its core `rescue` subcommand layout.

---

## 🛠️ The Bad Sector Rescue Loop

When the core encounter a physical block-level hardware error (`EIO` - Input/output error), the signal layer blocks a hard crash and triggers the recovery routine:

1.  **Mapfile Registration:** The precise absolute byte offset and boundary range of the failed block are immediately appended onto the localized runtime mapfile `logs/bad_sectors.map`.
2.  **The Fixed-Grid Skip:** Utilizing our mathematical fixed-grid wiskunde, the core calculates the starting boundary of the *next* clean archive block and fires an immediate `f.seek()` pointer jump over the hardware failure zone.
3.  **Resumption:** Streaming resumes instantly on the next healthy cluster, isolating disk head stress and maximizing overall data salvage velocity.

---

## 🧱 Format-Specific Block Masking

Once a sector skip is executed, the core passes the missing block offset to the active `formats/` export plugin to align data structures according to the precise expectations of the output target format:

### 1. RAW and ISO Targets (Forensic Zero-Padding)
*   **Logic:** The engine forces an injection of pure binary null bytes (`\0`) matching the exact length of the missed block.
*   **Why:** This maintains strict physical disk geometry size bounds and sector alignment parity. Ocluding the block would shift all following partitions forward, destroying file allocation tables.

### 2. E01 and AFF4 Containers (Forensic Block Marking)
*   **Logic:** The plugin injects a specialized placeholder byte matrix, but crucially flips a binaire **Corrupt Flag Metadata Bit** inside the container sector header mapping tables.
*   **Why:** When the resulting `.E01` file is mounted inside forensic suites like Autopsy or EnCase, the software displays a distinctive red "Unreadable Cluster" warning layout, keeping the final global image hash mathematically valid and legally sound.

### 3. QCOW2 and VMDK Formats (Sparse Cluster Bypass)
*   **Logic:** The plugin completely omits writing to that block range, executing an allocation skip.
*   **Why:** This marks the cluster metadata layout as unallocated (a sparse hole). The hypervisor will safely return virtual null bytes if the VM reads that block later, while saving massive amounts of physical disk space on the underlying production array.
