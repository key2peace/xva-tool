# ==============================================================================
#  XVATOOL PLUGIN - AFF4 (Advanced Forensic Format) Open-Source Container Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
# -*- coding: utf-8 -*-
"""
Dynamic AFF4 forensic format extension module.
Pipes and compresses raw block streams into cryptographically signed open containers.
"""

import os
import sys
import subprocess

# Track if the optional pyaff4 library backend is discoverable in the active environment
AFF4_AVAILABLE = False
try:
	import pyaff4
	AFF4_AVAILABLE = True
except ImportError:
	pass

def is_supported():
	"""
	Proactive Environment Check. Verifies if the host operating system
	has either the pyaff4 python module or the system-level 'aff4imager' binary.
	"""
	if AFF4_AVAILABLE:
		return True

	binary_name = "aff4imager"
	path_env = os.environ.get("PATH", "")
	for path_dir in path_env.split(os.path.pathsep):
		if os.path.isfile(os.path.join(path_dir, binary_name)):
			return True
	return False


def register_arguments(parser):
	"""Attaches AFF4 specific compression and multi-stream options to the core engine."""
	group = parser.add_argument_group("Advanced Forensic Format Options")
	group.add_argument("--aff4-compression", choices=["none", "lz4", "zlib"], default="lz4",
		help="Set the internal block compression architecture (Default: lz4)")
	group.add_argument("--aff4-threads", type=int, default=2,
		help="Set the multi-stream execution compression thread count limits")


def get_write_pipeline(target_path, args=None):
	"""
	Secure Downstream Pipe Provisioning. Launches aff4imager enforcing
	strict array-string parameters to banish command injection vulnerabilities.
	"""
	comp_tier = "lz4"
	thread_limit = "2"

	if args:
		if hasattr(args, "aff4_compression"): comp_tier = args.aff4_compression
		if hasattr(args, "aff4_threads"): thread_limit = str(args.aff4_threads)

	# Build the strict array representation layout for subprocess launch
	cmd_array = [
		"aff4imager",
		"-o", target_path,
		"-c", comp_tier,
		"-t", thread_limit,
		"-i", "-" # Instructs the imager to ingest the raw bitstream from STDIN
	]

	try:
		proc = subprocess.Popen(cmd_array, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		return proc
	except (OSError, ValueError) as e:
		sys.stderr.write("[!] AFF4 Pipeline Initiation Failure: " + str(e) + "\n")
		return None
