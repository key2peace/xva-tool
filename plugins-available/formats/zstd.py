#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVAPLUGIN - Zstandard (zstd) High-Throughput Streaming Compression Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic Zstandard stream format extension module.
Pipes raw block clusters on-the-fly through multi-threaded zstd binaries.
"""

import os
import sys
import subprocess

def is_supported():
	"""
	Proactive Environment Check. Verifies if the native 'zstd' system
	binary is fully discoverable and executable within the OS PATH.
	"""
	binary_name = "zstd"
	path_env = os.environ.get("PATH", "")
	
	for path_dir in path_env.split(os.path.pathsep):
		candidate_path = os.path.join(path_dir, binary_name)
		if os.path.isfile(candidate_path) and os.access(candidate_path, os.X_OK):
			return True
	return False


def register_arguments(parser):
	"""Attaches domain-specific Zstd multi-threading and level flags to the core."""
	group = parser.add_argument_group("Zstandard Compression Options")
	group.add_argument("--zstd-level", type=int, choices=range(1, 23), default=3,
		help="Set the specific Zstd mathematical compression level (1-22, Default: 3)")
	group.add_argument("--zstd-threads", type=int, default=0,
		help="Set the compression thread count limits (0 = Auto-match physical CPU cores)")


def get_write_pipeline(target_path, args=None):
	"""
	Secure Downstream Pipe Provisioning. Launches zstd enforcing
	strict array-string parameters to banish command injection vulnerabilities.
	"""
	z_level = "3"
	z_threads = "0"
	
	if args:
		if hasattr(args, 'zstd_level'): z_level = str(args.zstd_level)
		if hasattr(args, 'zstd_threads'): z_threads = str(args.zstd_threads)

	# Build the strict array representation layout for subprocess launch
	# -T0 instructs zstd to scale threads automatically across all CPU cores
	cmd_array = [
		"zstd",
		"-{}".format(z_level),
		"-T{}".format(z_threads),
		"-o", target_path,
		"-" # Instructs zstd to swallow the raw bitstream from STDIN
	]

	try:
		# Engage the child pipeline execution process cleanly
		proc = subprocess.Popen(cmd_array, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		return proc
	except (OSError, ValueError) as e:
		sys.stderr.write("[!] Zstd Pipeline Initiation Failure: " + str(e) + "\n")
		return None
