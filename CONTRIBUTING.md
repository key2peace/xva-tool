# Contributing to xva-tool

Thank you for your interest in contributing to the `xva-tool` enterprise forensics framework. To maintain structural integrity, binary compliance, and flawless diffs across all development environments, all contributors must strictly adhere to the repository gatekeeping rules defined below.

## 1. Core Coding Standards (The Non-Negotiables)

The architecture of `xva-tool` is governed by strict white-space and cross-platform formatting rules. Any pull request failing to meet these automation standards will be automatically rejected by the CI/CD boundary pipelines.

*	**Indentation:** You must use **TABS exclusively** for code alignment and indentation. Space-based indentation (`    `) is strictly forbidden.
*	**Line Endings:** All repository files must use **Unix LF (`\n`)** line breaks. Windows CRLF (`\r\n`) line endings will fail sanity checks immediately. Configure your editor (e.g., Notepad++, VS Code) to enforce Unix LF prior to committing.
*	**Encoding:** Every source, header, and configuration file must be stored in raw **UTF-8 (without BOM)** formatting.

## 2. Licensing & Intellectual Property Matrix

To ensure absolute clarity regarding intellectual property rights across the `xva-tool` ecosystem, contributions are strictly divided into two architectural scopes:

### A. Core Framework Modifications & Existing Code Patching
*	Any patches, optimizations, or bugfixes targeting existing `xva-tool` source files inherit the overarching enterprise license.
*	**Existing headers must never be wiped or replaced.** Modifying or removing the original authorship block (Alexander Maassen / OUTsider) is strictly prohibited. Contributors modifying existing code may exclusively append their name to the header block as an additional contributor or patch-author (e.g., `* Patch by: John Doe`).

### B. Splinterverse New Plugins & Extensions (Absolute Autonomy)
*	**A new plugin is not the core.** If you develop a brand-new, standalone plugin or extension from scratch that interacts through our interfaces, you maintain full intellectual property rights.
*	Authors of entirely new plugins retain **100% control over their own licensing, custom copyright blocks, and terms of use**. You own your extension completely.

## 3. Pull Request (PR) Workflow

To keep the repository history clean and traceable during forensic tracking:

1.	**Branch Isolation:** Never submit a PR from your local `master` or `main` branch. Create a feature-specific tracking branch (e.g., `feature/cli-core-hardening` or `bugfix/issue-3-crlf-leak`).
2.	**Atomic Commits:** Keep your commit payloads small, clean, and logical. Squashing unnecessary micro-commits before filing the pull request is highly encouraged.
3.	**Validation:** Ensure your code passes all local execution tests and displays zero syntax warnings before pushing upstream.

---
**By contributing code to this repository, you explicitly certify that your contributions are your own original work and conform entirely to the xva-tool architecture matrix.**
