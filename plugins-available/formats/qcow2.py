#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVAPLUGIN - QCOW2 (KVM / Proxmox VE) High-Performance Conversion Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic QCOW2 stream format extension module.
Pipes raw block clusters on-the-fly into qemu-img without local caching.
"""

import os
import sys
import subprocess

def is_supported():
	"""
	Proactive Environment Check. Verifies if the 'qemu-img' system
	binary is fully discoverable and executable within the OS PATH.
	"""
	binary_name = "qemu-img"
	path_env = os.environ.get("PATH", "")

	for path_dir in path_env.split(os.path.pathsep):
		candidate_path = os.path.join(path_dir, binary_name)
		if os.path.isfile(candidate_path) and os.access(candidate_path, os.X_OK):
			return True
	return False


def register_arguments(parser):
	"""Attaches domain-specific compression argument flags to the core compiler."""
	group = parser.add_argument_group("QCOW2 Format Configuration Options")
	group.add_argument("--qcow2-compat", choices=["0.10", "1.1"], default="1.1",
		help="Enforce a specific QEMU metadata compatibility version level")
	group.add_argument("--qcow2-cluster-size", type=int, default=65536,
		help="Set the specific internal allocation cluster size block boundaries")


def get_write_pipeline(target_path, args=None):
	"""
	Secure Downstream Pipe Provisioning. Launches qemu-img convert
	enforcing strict array-string parameters to banish command injection vulnerabilities.
	"""
	compat_version = "1.1"
	cluster_size = "65536"

	if args:
		if hasattr(args, 'qcow2_compat'): compat_version = args.qcow2_compat
		if hasattr(args, 'qcow2_cluster_size'): cluster_size = str(args.qcow2_cluster_size)

	# Build the strict array representation layout for subprocess launch
	cmd_array = [
		"qemu-img", "convert",
		"-f", "raw",
		"-O", "qcow2",
		"-o", "compat={},cluster_size={}".format(compat_version, cluster_size),
		"-", # Instructs qemu-img to swallow the raw bitstream from STDIN
		target_path
	]

	try:
		# Engage the child pipeline execution process cleanly
		proc = subprocess.Popen(cmd_array, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		return proc
	except (OSError, ValueError) as e:
		sys.stderr.write("[!] QCOW2 Pipeline Initiation Failure: " + str(e) + "\n")
		return None
