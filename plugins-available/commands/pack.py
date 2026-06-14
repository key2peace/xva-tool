#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVATOOL PLUGIN - High-Performance Streaming XVA Compressor Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic pack command extension module.
Re-compiles raw disk boundaries back into sparse compressed XenServer tarballs.
"""

import os
import sys
import tarfile
import zlib
import io

def is_supported():
	"""Proactive Environment Check. Always returns True as it uses pure Python core modules."""
	return True


def register_arguments(parser):
	"""Attaches compression tuning parameters to the central framework compiler."""
	group = parser.add_argument_group("XVA Target Packing Options")
	group.add_argument("-c", "--compress", action="store_true",
		help="Enforce dynamic zlib compression passes over outgoing allocation chunks")
	group.add_argument("--level", type=int, choices=range(1, 10), default=6,
		help="Set the specific zlib mathematical compression level (1=Fast, 9=Maximum)")


def execute(args):
	"""Main execution lifecycle entrypoint triggered by the xva-tool core mapper."""
	if not hasattr(args, 'archive') or not hasattr(args, 'target'):
		sys.stderr.write("[!] Syntax Error: Usage requires 'xva-tool pack <source.img> <target.xva.gz>'.\n")
		sys.exit(1)

	src_img = args.archive
	target_xva = args.target

	if not os.path.exists(src_img):
		sys.stderr.write("[!] Packing Error: Source raw storage disk node does not exist.\n")
		sys.exit(1)

	print("Initializing streaming compilation cascade (RAW -> XVA)...")
	print("Target archive destination: " + target_xva)

	# Load cascade properties or fall back straight to command arguments flags
	enforce_compression = args.compress
	z_level = args.level

	chunk_size = 1024 * 1024 # Standard 1MB chunk alignment matrix
	tar_header_size = 512

	try:
		# Open upstream read handles and output write descriptors
		in_f = open(src_img, "rb")
		
		# Determine output suffix based on active compression settings
		out_f = open(target_xva, "wb")
	except (IOError, OSError) as e:
		sys.stderr.write("[!] Infrastructure Lock Failure: Cannot bind file streams: " + str(e) + "\n")
		sys.exit(1)

	# 1. Seed the initial fake master configuration descriptor ova.xml
	print("[*] Injecting primary virtual hypervisor structure manifest maps...")
	fake_xml = (
		'<?xml version="1.0" encoding="UTF-8"?>'
		'<value><struct>'
		'<member><name>name_label</name><value>Recompiled-Image-By-XvaTool</value></member>'
		'</struct></value>'
	)
	
	# Compile a standard USTAR compliant header for the XML file segment
	xml_header = bytearray(512)
	struct.pack_into("<100s8s8s8s12s12s", xml_header, 0, "ova.xml", "0000644", "0000000", "0000000", "{:011o}".format(len(fake_xml)), "{:011o}".format(int(time.time())))
	struct.pack_into("<6s2s", xml_header, 257, "ustar", "00")
	
	out_f.write(xml_header)
	out_f.write(fake_xml)
	# Align block padding bounds up to 512 multiples sequence
	xml_padding = 512 - (len(fake_xml) % 512)
	if xml_padding < 512:
		out_f.write("\0" * xml_padding)

	print("[*] Entering binaire chunk extraction and streaming compression loops...")
	chunk_idx = 0
	
	while True:
		try:
			chunk_bytes = in_f.read(chunk_size)
			if not chunk_bytes:
				break # Raw block storage allocation tracking finalized

			# 2. Forensic Sparse Hole Detection Layer
			# If the entire 1MB chunk is purely populated by null bytes, completely bypass writing
			if chunk_bytes == "\0" * len(chunk_bytes):
				chunk_idx += 1
				continue

			# 3. Compile structural name markers mapping context (e.g. Ref:0/00000000)
			chunk_filename = "Ref:0/{:08d}".format(chunk_idx)
			
			# Build standard tar chunk configuration block header
			header_block = bytearray(512)
			struct.pack_into("<100s8s8s8s12s12s", header_block, 0, chunk_filename, "0000644", "0000000", "0000000", "{:011o}".format(len(chunk_bytes)), "{:011o}".format(int(time.time())))
			struct.pack_into("<6s2s", header_block, 257, "ustar", "00")

			# 4. Transmission Layer Output Allocation Routing
			if enforce_compression:
				# Compress the data block dynamically utilizing zlib parameters mapping
				compressed_payload = zlib.compress(chunk_bytes, z_level)
				# Recalculate size blocks to match compressed output bounds inside headers
				struct.pack_into("<12s", header_block, 124, "{:011o}".format(len(compressed_payload)))
				
				out_f.write(header_block)
				out_f.write(compressed_payload)
				# Pad the compressed chunk trail cleanly to align blocks
				pad_len = 512 - (len(compressed_payload) % 512)
				if pad_len < 512: out_f.write("\0" * pad_len)
			else:
				# Stream raw untouched blocks directly down to the storage array layout
				out_f.write(header_block)
				out_f.write(chunk_bytes)
				
		except (IOError, OSError) as e:
			sys.stderr.write("[!] Critical streaming write interruption failure: " + str(e) + "\n")
			break

		chunk_idx += 1

	# 5. Append official USTAR double 512-byte null terminator frames at EOF
	out_f.write("\0" * 1024)
	
	in_f.close()
	out_f.close()
	print("Success: Compilation sequence finalized cleanly. Output archive locked.")
