---
name: "🐛 Bug Report / Execution Failure"
about: Report a binary crash, I/O error, or storage pipeline blocker.
title: "[BUG] "
labels: ["bug", "triage"]
assignees: "key2peace"
---

## 🔍 Context & Environment Data
*   **Operating System & Version:** (e.g., Debian 12 / Proxmox VE 8.2)
*   **Python Version:** (Output of `python --version` - Target is 2.7)
*   **Execution Environment:** (e.g., Local CLI / Retro Curses TUI / Docker Container / Privileged Root)
*   **Storage Target Layout:** (e.g., RAID-6 Array, SSD, Local USB device)

## 🎯 The Subcommand Row
*Please provide the exact command string you executed when the failure occurred (sanitize sensitive IPs/domains).*
```bash
xva-tool merge -f /path/to/archive.xva.gz sftps://target-host/data
```

## 🚨 Error Indicators & Logs
*   **Did the Red Dialogue Box appear?** [Yes / No]
*   **What was the proposed fix shown in the troubleshoot guide?**
*   **Please paste the trailing log outputs from `logs/xva-tool.log` or syslog:**
```text
[2026-06-13 22:15:00] [CRITICAL] Execution interrupted: Downstream pipeline broken (SIGPIPE)
[2026-06-13 22:15:00] [ERROR] Subprocess failure inside plugins-enabled/formats/qcow2.py
```

## 📝 Steps to Reproduce
1. Stage an uncompressed XVA archive of size...
2. Invoke the subcommand using the `--force` flag...
3. See error row.

## 🧠 Additional Forensic Notes
*(Is the archive truncated? Did the MBR partition parser output anomalies during `xva-tool info`?)*
