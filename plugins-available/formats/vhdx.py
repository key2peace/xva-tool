#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVAPLUGIN - VHDX (Microsoft Hyper-V / Azure) High-Performance Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic VHDX stream format extension module.
Pipes raw block clusters directly into Hyper-V compliant targets via qemu-img.
"""

import os
import sys
import subprocess

def is_supported():
	"""
	Proactive Environment Check. Verifies if the 'qemu-img' subsystem 
	is accessible on the host machine to compile VHDX metadata layout structures.
	"""
	binary_name = "qemu-img"
	path_env = os.environ.get("PATH", "")
	
	for path_dir in path_env.split(os.path.pathsep):
		candidate_path = os.path.join(path_dir, binary_name)
		if os.path.isfile(candidate_path) and os.access(candidate_path, os.X_OK):
			return True
	return False


def register_arguments(parser):
	"""Attaches Microsoft specific sub-format constraints to the core parser layer."""
	group = parser.add_argument_group("Microsoft Hyper-V VHDX Format Options")
	group.add_argument("--vhdx-subformat", choices=["dynamic", "fixed"], default="dynamic",
		help="Enforce a specific underlying Microsoft cluster allocation layout block")
	group.add_argument("--vhdx-block-size", type=int, default=1048576,
		help="Set the precise virtual sector block alignment boundaries (in bytes)")


def get_write_pipeline(target_path, args=None):
	"""
	Secure Downstream Pipe Provisioning. Launches the pipeline using
	string-array arguments to completely eliminate shell injection capabilities.
	"""
	subformat = "dynamic"
	block_size = "1048576"
	
	if args:
		if hasattr(args, 'vhdx_subformat'): subformat = args.vhdx_subformat
		if hasattr(args, 'vhdx_block_size'): block_size = str(args.vhdx_block_size)

	# Enforce secure list formatting targeting subprocess initialization
	cmd_array = [
		"qemu-img", "convert",
		"-f", "raw",
		"-O", "vhdx",
		"-o", "subformat={},block_size={}".format(subformat, block_size),
		"-", # Accepts the raw incoming bitstream over STDIN from the core
		target_path
	]

	try:
		proc = subprocess.Popen(cmd_array, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		return proc
	except (OSError, ValueError) as e:
		sys.stderr.write("[!] VHDX Pipeline Initiation Failure: " + str(e) + "\n")
		return None
