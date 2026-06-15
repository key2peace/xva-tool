# ==============================================================================
#      XVA-TOOL - Forensics & Recovery Tool designed for XenServer
#
#      copyright ©2026 Alexander Maassen & Gemini AI
#      Distributed under the terms of the MIT License.
# ==============================================================================
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XVA-TOOL - Automated Developer API & Plugin Documentation Generator
Extracts documentation straight from core metadata and plugin docstrings.
Targeted strictly for GitHub Actions CI/CD runtime (Python 3.11+).
"""

import os
import sys
import importlib.util
from pathlib import Path

# Enforce clean path loading for relative plugin imports
sys.path.insert(0, str(Path(__file__).parent.absolute()))

def extract_plugin_meta(plugin_path: Path) -> dict:
	"""Dynamically imports a plugin file using Python 3 importlib and extracts its specifications."""
	module_name = plugin_path.stem

	try:
		# Modern Python 3 dynamic spec loading straight from file path
		spec = importlib.util.spec_from_file_location(module_name, str(plugin_path))
		if spec is None or spec.loader is None:
			return {"name": module_name, "type": "error", "help": "Could not load spec", "doc": ""}

		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)

		# Extract structural metadata dictionary and docstring
		plugin_dict = getattr(module, 'pl', {})
		docstring = getattr(module, '__doc__', 'No detailed description available.')

		return {
			"name": plugin_dict.get("name", module_name),
			"type": plugin_dict.get("type", "unknown"),
			"help": plugin_dict.get("help", "No help text provided."),
			"doc": docstring.strip() if docstring else "No detailed description available."
		}
	except Exception as e:
		return {"name": module_name, "type": "error", "help": f"Failed to import: {e}", "doc": ""}

def generate_markdown():
	"""Scans the plugins directory and compiles the centralized Markdown documentation."""
	plugin_dir = Path("plugins-available")
	output_file = Path("docs/PLUGIN_API.md")

	# Ensure the output directory exists
	output_file.parent.mkdir(parents=True, exist_ok=True)

	print(f"[*] Initiating Docs Analysis: Scanning {plugin_dir}...")

	markdown_buffer = [
		"# XVA-TOOL - Plugin API Reference\n",
		"Welcome to the automated plugin reference. This documentation is generated directly from the source code docstrings and structural metadata. **Do not modify this file manually.**\n\n"
	]

	# Scan for available plugins chronologically using pathlib
	if plugin_dir.exists():
		for plugin_path in sorted(plugin_dir.glob("**/*.py")):
			if plugin_path.name.startswith("__"):
				continue

			print(f"[+] Parsing plugin: {plugin_path}")
			meta = extract_plugin_meta(plugin_path)

			if meta["type"] == "error":
				print(f"[!] Skipping error in {plugin_path.name}: {meta['help']}")
				continue

			markdown_buffer.append(f"## {meta['name']} (`{meta['type']}`)\n")
			markdown_buffer.append(f"**Summary:** {meta['help']}\n\n")
			markdown_buffer.append("### Developer Specifications\n")
			markdown_buffer.append(f"```text\n{meta['doc']}\n```\n")
			markdown_buffer.append("---\n\n")

	# Write out the final document with clean Unix endings
	output_file.write_text("".join(markdown_buffer), encoding="utf-8")
	print(f"[🟢] Success: '{output_file}' compiled successfully.")

if __name__ == "__main__":
	generate_markdown()
