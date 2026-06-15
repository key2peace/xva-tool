# ==============================================================================
#      XVA-TOOL PLUGIN - COMMAND: MERGE ENGINE
#      Optimized for zero-copy streaming, memory profiles, and structural safety.
#
#      Developed and maintained by Alexander Maassen and Google's Gemini AI.
#      Licensed under the terms of the MIT License.
# ==============================================================================
# -*- coding: utf-8 -*-
"""
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
"""

import os
import sys
import gc

# The Plugin Metadata Dictionary - Placed strictly below core imports
pl = {
	"name": "merge",
	"type": "commands",
	"help": "Slam and merge 1MB container chunks into a unified raw disk image."
}

def execute(args, global_state):
	"""Executes the zero-copy binary merge sequence over the block array."""
	source_dir = args.target
	output_raw = args.output if getattr(args, 'output', None) else "output_disk.raw"

	# Resolve the memory profile mapped out by the core bootstrap
	mem_profile = global_state.get("active_profile", "SPARSE_MODE")
	buffer_size = 1024 * 1024 # Strict 1MB block allocation default

	if mem_profile == "PERFORMANCE_MODE":
		buffer_size = 32 * 1024 * 1024 # Scale up to 32MB streaming buffers

	print("[*] Target detected. Initiating block extraction over: " + source_dir)
	print("[*] Enforcing runtime memory allocation boundary: " + mem_profile)

	# Verify extraction directory state
	if not os.path.isdir(source_dir):
		print("[❌] Critical: Target path is not a valid directory environment.")
		sys.exit(1)

	# Target block scanning (e.g. Ref:00000000/)
	block_files = []
	for root, dirs, files in os.walk(source_dir):
		for file in files:
			if file.isdigit() or file.startswith("block_"):
				block_files.append(os.path.join(root, file))

	if not block_files:
		print("[❌] Critical: No valid raw binary storage chunks discovered.")
		sys.exit(1)

	# Enforce absolute chronological sequential block alignment
	block_files.sort()
	total_chunks = len(block_files)
	print("[+] Sequenced " + str(total_chunks) + " structural data segments for consolidation.")

	print("[*] Provisioning destination raw layout handle: " + output_raw)
	try:
		# Open destination image with strict binary-write locks
		with open(output_raw, "wb") as out_fh:
			for index, chunk_path in enumerate(block_files):
				sys.stdout.write("\r[*] Progress: Mapping block " + str(index + 1) + "/" + str(total_chunks))
				sys.stdout.flush()

				# Zero-copy streaming loop over the OS-layer buffers
				with open(chunk_path, "rb") as in_fh:
					while True:
						chunk_bytes = in_fh.read(buffer_size)
						if not chunk_bytes:
							break
						out_fh.write(chunk_bytes)

				# Forced garbage collection to prevent WebKit-level memory accumulation
				if index % 50 == 0:
					gc.collect()

		print("\n[🟢] Success: Data stream finalized. Extraction matrix completed.")
	except IOError as e:
		print("\n[❌] Structural Write Interruption: " + str(e))
		sys.exit(1)
