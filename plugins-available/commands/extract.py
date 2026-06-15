# ==============================================================================
#      XVA-TOOL PLUGIN - COMMAND: EXTRACT ENGINE
#      Handles binary chunk extraction with interactive timeout protections.
#
#      Developed and maintained by Alexander Maassen and Google's Gemini AI.
#      Licensed under the terms of the MIT License.
# ==============================================================================
# -*- coding: utf-8 -*-
"""
XVA-TOOL Plugin: Command - Container Extraction Engine

This module implements the low-level extraction process for uncompressed
XVA containers. It processes the internal tarball stream, extracts individual
1MB binary disk segments sequentially, and recreates the path layouts.

Developer Specifications:
    - Entry Hook: Execute command invocation with target payload pathways.
    - Interactive Layer: Optional user-confirmation block per processed chunk.
    - Performance Layer: Enforces periodic garbage collection routines.
"""

import os
import sys
import tarfile
import gc

# The Plugin Metadata Dictionary - Placed strictly below core imports
pl = {
	"name": "extract",
	"type": "commands",
	"help": "Unpack an uncompressed XVA container into a structured directory of 1MB blocks."
}

def execute(args, global_state):
	"""Executes the zero-copy binary extraction sequence from the XVA archive."""
	source_xva = args.target
	output_dir = args.output if getattr(args, 'output', None) else "extracted_chunks"
	interactive = getattr(args, 'interactive', False)

	print("[*] Opening target container archive: " + source_xva)
	if not os.path.exists(source_xva):
		print("[❌] Critical: Source XVA container path does not exist.")
		sys.exit(1)

	try:
		with tarfile.open(source_xva, "r:") as tar:
			print("[*] Scanning structural archive descriptors...")
			members = tar.getmembers()
			total_files = len(members)
			print("[+] Found " + str(total_files) + " uncompressed elements inside repository.")

			for index, member in enumerate(members):
				# Safeguard against directory traversal attacks
				if ".." in member.name or member.name.startswith("/"):
					print("\n[⚠️] Security Alert: Skipping suspicious block layout: " + member.name)
					continue

				sys.stdout.write("\r[*] Processing element " + str(index + 1) + "/" + str(total_files) + " -> " + member.name)
				sys.stdout.flush()

				# Interactive Chunk Hook to prevent memory or pipeline freezes
				if interactive and member.isreg():
					print("\n[?] Halt: Next data segment ready (" + str(member.size) + " bytes).")
					user_input = raw_input("    Press [Enter] to flush block to disk, or 'q' to abort: ") if sys.version_info[0] < 3 else input("    Press [Enter] to flush block to disk, or 'q' to abort: ")
					if user_input.strip().lower() == 'q':
						print("[*] Extraction sequence aborted by user command.")
						sys.exit(0)

				# Execute strict sequential block write
				tar.extract(member, path=output_dir)

				# Forced garbage collection loop
				if index % 50 == 0:
					gc.collect()

		print("\n[🟢] Success: Container extraction sequence finalized cleanly.")
	except Exception as e:
		print("\n[❌] Structural Ingestion Failure: " + str(e))
		sys.exit(1)
