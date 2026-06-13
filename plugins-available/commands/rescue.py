#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVATOOL PLUGIN - Advanced GNU ddrescue-inspired Data Recovery Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic rescue command extension module.
Orchestrates non-destructive block-level skipping over degraded storage arrays.
"""

import os
import sys

def is_supported():
	"""Proactive Environment Check. Always returns True as it relies on core Python."""
	return True


def register_arguments(parser):
	"""Attaches data recovery thresholds to the core command parser."""
	group = parser.add_argument_group("Data Recovery Skipping Options")
	group.add_argument("--mapfile", default="logs/bad_sectors.map",
		help="Specify a custom output path for the forensic sector error map")
	group.add_argument("--max-errors", type=int, default=100,
		help="Maximum allowed hardware I/O faults before terminating the recovery loop")


def execute(args):
	"""Main execution lifecycle entrypoint triggered by the xva-tool core mapper."""
	if not hasattr(args, 'archive') or not hasattr(args, 'target'):
		sys.stderr.write("[!] Syntax Error: Usage requires 'xva-tool rescue <source.xva> <target.img>'.\n")
		sys.exit(1)

	map_path = args.mapfile
	max_errs = args.max_errors

	print "Initializing non-destructive hardware sector salvage pipeline..."
	print "Target sector error mapfile location: " + map_path

	# Check if a previous recovery mapfile exists to seed historical logs
	if os.path.exists(map_path):
		print "[*] Existing sector mapfile discovered. Appending new block records."
	else:
		# Allocate parent directories if missing
		parent_dir = os.path.dirname(map_path)
		if parent_dir and not os.path.exists(parent_dir):
			os.makedirs(parent_dir)
		with open(map_path, "w") as f:
			f.write("# XVATOOL FORENSIC RESCUE LOG MAPFILE\n# Status: Active\n")

	# Import and invoke the streaming core merge engine with rescue hooks activated
	try:
		from xvatool import execute_merge_engine
		# Force rescue mode and pass down command constraints parameters
		success = execute_merge_engine(
			args.archive, args.target, 
			force_flag=args.force, resume_flag=args.resume, rescue_mode=True
		)
		
		if success:
			print "Success: Salvage run finalized. Consult the mapfile for corruption health reports."
		sys.exit(0 if success else 1)
		
	except ImportError:
		sys.stderr.write("[!] Core Engine Missing: Failed to bind command to the execution stream.\n")
		sys.exit(1)
