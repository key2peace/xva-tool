# Security Policy & Vulnerability Reporting

## Supported Versions

We actively maintain and provide security updates for the current active alpha/beta branches. Legacy or unmaintained release forks are not covered.

| Version | Supported          |
| ------- | ------------------ |
| < v1.0  | :white_check_mark: |

## Reporting a Vulnerability

**Do not open an unencrypted public GitHub Issue for security bugs.**

If you discover a security vulnerability within `xva-tool` or its modular plugin subsystems, please report it responsibly by using one of the following secure channels:

1. **GitHub Private Vulnerability Reporting:** Go to the main repository page on GitHub.com, click on the **Security** tab, and select **Vulnerability reporting** to submit a private draft advisory securely.
2. **Direct Encrypted Contact:** Reach out directly to the maintainer via email at **Alexander Maassen <outsider@cuci.nl>**. If applicable, please use a secure, encrypted communication channel or PGP keys to safeguard the vulnerability details during transport.

### Required Information

To help us triage and resolve the issue efficiently, please include the following details in your report:
*   A detailed description of the vulnerability and its potential impact.
*   Step-by-step instructions, proof-of-concept (PoC) scripts, or commands required to reproduce the exploit.
*   The exact version of `xva-tool`, host operating system kernel, and any active plugin modules involved.

## Our Commitment

Upon receiving a valid security report, the maintainer will:
*   Acknowledge receipt of the vulnerability report within 48 business hours.
*   Work closely with the reporter to investigate, isolate, and remediate the issue within a reasonable timeline.
*   Coordinate a synchronized public security advisory along with the corresponding patch release to protect production deployments.
