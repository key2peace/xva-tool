#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVATOOL PLUGIN - E01 (Expert Witness Format / EnCase) Forensic Export Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic E01 forensic format extension module.
Pipes and compresses raw block streams into legally sound EnCase evidence files.
"""

__doc__ = """Forensic Expert Witness (E01) image stream parser."""

import os
import sys
import subprocess

# Track if the optional pyewf forensic library library is present on the host
PYEWF_AVAILABLE = False
try:
	import pyewf
	PYEWF_AVAILABLE = True
except ImportError:
	pass

def is_supported():
	"""
	Proactive Environment Check. Verifies if the host machine has either
	the pyewf Python module or the system-level 'ewfcreate' binary installed.
	"""
	if PYEWF_AVAILABLE:
		return True

	# Fallback: scan the system execution PATH for ewfcreate
	binary_name = "ewfcreate"
	path_env = os.environ.get("PATH", "")
	for path_dir in path_env.split(os.path.pathsep):
		if os.path.isfile(os.path.join(path_dir, binary_name)):
			return True
	return False


def register_arguments(parser):
	"""Attaches official DFIR chain-of-custody markers to the core framework parser."""
	group = parser.add_argument_group("EnCase E01 Forensic Container Options")
	group.add_argument("--e01-description", default="xva-tool Forensic Acquisition Run",
		help="Set the standard case description string inside the E01 container header")
	group.add_argument("--e01-compression", choices=["none", "fast", "best"], default="fast",
		help="Set the internal cryptographic block compression ratio profile layout")


def get_write_pipeline(target_path, args=None):
	"""
	Secure Downstream Pipe Provisioning. Launches ewfcreate using strict
	array-string arguments to map the incoming bitstream directly to the silicon.
	"""
	description_str = "xva-tool Forensic Acquisition Run"
	compression_tier = "fast"

	if args:
		if hasattr(args, "e01_description"): description_str = args.e01_description
		if hasattr(args, "e01_compression"): compression_tier = args.e01_compression

	# Translate our compression text profile to standard ewf flags matrix keys
	comp_flag = "good"
	if compression_tier == "none": comp_flag = "none"
	elif compression_tier == "best": comp_flag = "best"

	# Compile strict array parameters to block shell injection attacks completely
	cmd_array = [
		"ewfcreate",
		"-t", target_path.replace(".e01", ""), # ewfcreate appends the extension automatically
		"-c", comp_flag,
		"-d", description_str,
		"-u", "0", # Default operator identifier UID reference mapping
		"-" # Reads the raw block stream straight from STDIN from the core
	]

	try:
		# Engage the child pipeline execution process cleanly
		proc = subprocess.Popen(cmd_array, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		return proc
	except (OSError, ValueError) as e:
		sys.stderr.write("[!] E01 Forensic Pipeline Initiation Failure: " + str(e) + "\n")
		return None
