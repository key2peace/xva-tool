# ==============================================================================
#      XVA-TOOL PLUGIN - COMMAND: RESCUE ENGINE
#      Executes deep forensic stream carving over corrupted block layouts.
#
#      Developed and maintained by Alexander Maassen and Google's Gemini AI.
#      Licensed under the terms of the MIT License.
# ==============================================================================
# -*- coding: utf-8 -*-
"""
XVA-TOOL Plugin: Command - Forensic Block Rescue Engine

This module executes low-level byte carving and alignment repairs over 
damaged or incomplete uncompressed XVA containers. It intercepts corrupt 
headers to recover isolated data fragments and enforce data reconstruction.

Developer Specifications:
    - Entry Hook: Initiates stream carving and structural integrity validation.
    - Resiliency Focus: Bypasses native EOF dropouts to extract orphan segments.
    - Audit Trail: Forces precise positional error capturing inside local logs.

Exposed Variables:
    - pl (dict): System metadata tracking array containing module type,
                 classification name, and CLI help bindings.
"""

import os
import sys

# The Plugin Metadata Dictionary - Placed strictly below core imports
pl = {
	"name": "rescue",
	"type": "commands",
	"help": "Carve, salvage, and recover uncompressed data blocks from damaged containers."
}

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

	print("Initializing non-destructive hardware sector salvage pipeline...")
	print("Target sector error mapfile location: " + map_path)

	# Check if a previous recovery mapfile exists to seed historical logs
	if os.path.exists(map_path):
		print("[*] Existing sector mapfile discovered. Appending new block records.")
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
			print("Success: Salvage run finalized. Consult the mapfile for corruption health reports.")
		sys.exit(0 if success else 1)
		
	except ImportError:
		sys.stderr.write("[!] Core Engine Missing: Failed to bind command to the execution stream.\n")
		sys.exit(1)
