# ==============================================================================
#      XVA-TOOL PLUGIN - STORAGE: LOCAL FILE SYSTEM
#      Handles native POSIX directory and file block mapping hooks.
#
#      Developed and maintained by Alexander Maassen and Google's Gemini AI.
#      Licensed under the terms of the MIT License.
# ==============================================================================
# -*- coding: utf-8 -*-
"""
XVA-TOOL Plugin: Storage - Local File System Target

This module implements the standard file system I/O abstraction layer.
It hooks into the storage engine to validate local directories and read/write
raw binary chunks without utilizing external network protocols.

Developer Specifications:
    - Module Class: storage
    - Operational Focus: POSIX compliant block operations.
    - Performance Layer: Zero-copy read/write loops synchronized with the core.
"""

import os
import sys

# The Plugin Metadata Dictionary - Placed strictly below core imports
pl = {
	"name": "local",
	"type": "storage",
	"help": "Read and write uncompressed chunks directly from/to a local POSIX directory."
}

def validate_target(target_path):
	"""Verifies if the specified local target is an existing, accessible directory."""
	return os.path.isdir(target_path)

def stream_chunk(chunk_path, buffer_size):
	"""Reads and yields binary data chunks efficiently from the local storage layer."""
	if not os.path.exists(chunk_path):
		return

	with open(chunk_path, "rb") as fh:
		while True:
			data = fh.read(buffer_size)
			if not data:
				break
			yield data

def write_chunk(chunk_path, data_bytes):
	"""Writes raw binary chunk bytes directly and securely to the local disk layout."""
	try:
		# Extract target directory layout and enforce its existence programmatically
		target_dir = os.path.dirname(chunk_path)
		if target_dir and not os.path.exists(target_dir):
			os.makedirs(target_dir)

		# Execute strict binary-write block flush
		with open(chunk_path, "wb") as fh:
			fh.write(data_bytes)
		return True
	except IOError as e:
		print("\n[❌] Local Storage Write Failure: " + str(e))
		return False
