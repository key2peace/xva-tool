#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVAPLUGIN - VMDK (VMware ESXi / Workstation) Monolithic Conversion Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic VMDK stream format extension module.
Pipes raw block clusters directly into VMware-compliant targets via qemu-img.
"""

import os
import sys
import subprocess

def is_supported():
	"""
	Proactive Environment Check. Verifies if the 'qemu-img' subsystem
	is accessible on the host machine to compile VMDK descriptor envelopes.
	"""
	binary_name = "qemu-img"
	path_env = os.environ.get("PATH", "")

	for path_dir in path_env.split(os.path.pathsep):
		candidate_path = os.path.join(path_dir, binary_name)
		if os.path.isfile(candidate_path) and os.access(candidate_path, os.X_OK):
			return True
	return False


def register_arguments(parser):
	"""Attaches VMware specific sub-format constraints to the central engine parser."""
	group = parser.add_argument_group("VMware VMDK Format Options")
	group.add_argument("--vmdk-subformat", choices=["monolithicFlat", "streamOptimized", "sparse"],
		default="monolithicFlat", help="Enforce a specific underlying VMware cluster allocation map")


def get_write_pipeline(target_path, args=None):
	"""
	Secure Downstream Pipe Provisioning. Launches the pipeline using
	string-array arguments to completely eliminate shell injection capabilities.
	"""
	subformat = "monolithicFlat"
	if args and hasattr(args, 'vmdk_subformat'):
		subformat = args.vmdk_subformat

	# Enforce secure list formatting targeting subprocess initialization
	cmd_array = [
		"qemu-img", "convert",
		"-f", "raw",
		"-O", "vmdk",
		"-o", "subformat={}".format(subformat),
		"-", # Accepts the raw uncompressed incoming bitstream over STDIN
		target_path
	]

	try:
		proc = subprocess.Popen(cmd_array, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		return proc
	except (OSError, ValueError) as e:
		sys.stderr.write("[!] VMDK Pipeline Initiation Failure: " + str(e) + "\n")
		return None
