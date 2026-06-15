#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVATOOL PLUGIN - Machine-Readable JSON Telemetry & SIEM Aggregation Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic JSON reporting extension module.
Generates RFC-compliant JSON objects optimized for centralized SIEM ingestors.
"""

import os
import sys
import time
import platform
import getpass
import json

def is_supported():
	"""Proactive Environment Check. Always returns True as it uses native JSON modules."""
	return True


def register_arguments(parser):
	"""Attaches formatting options targeting JSON block serialization loops."""
	group = parser.add_argument_group("JSON Telemetry Reporting Options")
	group.add_argument("--json-pretty", action="store_true",
		help="Enforce expanded indentation padding to make output easily human-readable")


def compile_report(target_image_path, checksum_dict, args=None):
	"""Compiles an unassailable JSON descriptor record targeting monitoring pipelines."""
	report_file_path = target_image_path + ".json"
	timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

	pretty_print = False
	if args and hasattr(args, "json_pretty"):
		pretty_print = args.json_pretty

	# Construct the comprehensive multi-tier internal master data matrix dictionary
	report_matrix = {
		"framework": {
			"application": "xva-tool",
			"version": "1.0.0",
			"maintainer": "Alexander Maassen"
		},
		"environment": {
			"timestamp_utc": timestamp,
			"operator_handle": getpass.getuser(),
			"host_node_name": platform.node(),
			"operating_system": platform.platform(),
			"process_id": os.getpid()
		},
		"target_resource": {
			"filename": os.path.basename(target_image_path),
			"absolute_fhs_path": os.path.abspath(target_image_path),
			"file_size_bytes": os.path.getsize(target_image_path) if os.path.exists(target_image_path) else 0
		},
		"cryptographic_signatures": {
			"md5": checksum_dict.get("md5", "NOT_COMPUTED").upper(),
			"sha1": checksum_dict.get("sha1", "NOT_COMPUTED").upper(),
			"sha256": checksum_dict.get("sha256", "NOT_COMPUTED").upper()
		}
	}

	try:
		with open(report_file_path, "w") as jf:
			if pretty_print:
				# Serialize JSON utilizing 4-space tab structure mapping layouts
				json.dump(report_matrix, jf, indent=4, sort_keys=True)
			else:
				# Serialize into compact single-line string structures for log shippers
				json.dump(report_matrix, jf)
		return True
	except (IOError, OSError) as e:
		sys.stderr.write("[!] JSON Reporting Engine Failure: " + str(e) + "\n")
		return False
