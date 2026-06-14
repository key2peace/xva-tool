# Pre-Flight Integrity Auditing

The framework incorporates specialized subroutines to validate the structural integrity of uncompressed XVA containers before executing resource-intensive operations.

## The Verify Subcommand
The `verify.py` extension performs low-RAM, non-destructive scans on the archive's internal fixed-grid allocation matrix.

### Command Execution
```bash
xva-tool verify /path/to/archive.xva [--deep-scan]
```

### Operational Architecture
1. **Metadata Validation**: Parses and cross-examines the leading `ova.xml` layout definitions against the actual block alignment.
2. **Allocation Grid Sweep**: Reads precise block sectors via $O(1)$ disk navigation hooks to confirm block completeness without local file write operations.
3. **Forensic Logging**: Tracks anomalies and reports truncated or misaligned archives instantly onto `logs/bad_sectors.map`.
