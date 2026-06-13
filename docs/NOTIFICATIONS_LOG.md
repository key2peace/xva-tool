# 📝 Notifications & Kernel Log Aggregation

The framework incorporates a decoupled, non-blocking event system (`plugins-available/log/`) designed to catch core signals and route operational statuses, transaction audits, and resource warnings to diverse endpoints.

---

## 📰 Logging Engines

### 1. file.py (Cascading File Logger)
*   **Behavior:** Writes timestamped records cleanly to `/var/log/xva-tool.log`. If root permissions are unavailable, it falls back automatically to userspace paths (`~/.local/share/xva-tool/xva-tool.log`).
*   **Management:** Implements automated internal rollover logic governed by the `max_log_size_mb` variable defined in the configuration tier.

### 2. journald.py (Systemd Journal Socket)
*   **Behavior:** Bypasses flat files and pipes structured binary records directly into the local Linux kernel socket `/run/systemd/journal/socket`.
*   **Winst:** All xva-tool activities are fully queryable natively via standard system execution routines like `journalctl -u xva-tool` or `journalctl _PID=XXXX`, preserving OS process metadata (PID, UID).

### 3. syslog.py (Remote RFC 5424 Aggregator)
*   **Behavior:** Formats runtime events into standardized syslog envelopes and dispatches them via UDP/TCP network pipelines to central log management servers (rsyslog, Splunk, Graylog).

---

## 🔔 Non-Blocking Notification Webhooks

Notification plugins operate within asynchronous background threads, ensuring that active I/O streaming pipelines are never delayed by slow external web responses:

*   **slack.py / discord.py:** Fires structured incoming JSON POST payloads to webhook integration paths, color-coding results instantly (green tick cards for success, red block markers for system faults).
*   **telegram.py:** Interfaces with the lightweight Telegram Bot API to dispatch discrete private administrative text messages (DMs) straight to the sysadmin's phone.
*   **apprise.py (Universal Hub Hub):** Lazy-loads the optional system extension wrapper if discoverable on the host, granting instant delivery access to over 80 push, SMS, and chat notification provider backends.
