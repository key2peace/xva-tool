#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVATOOL PLUGIN - Flat CSV Structural Logging & Metadata Export Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic CSV reporting extension module.
Generates flat-table delimited spreadsheets tracking extraction metadata bounds.
"""

import os
import sys
import time
import platform
import getpass

def is_supported():
	"""Proactive Environment Check. Always returns True as it uses pure Python modules."""
	return True


def register_arguments(parser):
	"""Attaches CSV specific delimiter parameters to the core framework parser."""
	group = parser.add_argument_group("CSV Spreadsheet Reporting Options")
	group.add_argument("--csv-delimiter", default=";",
		help="Specify the structural data cell separation delimiter string (Default: ;)")


def compile_report(target_image_path, checksum_dict, args=None):
	"""Generates a compliance-ready flat CSV spreadsheet table alongside the image output."""
	report_file_path = target_image_path + ".csv"
	timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
	
	delim = ";"
	if args and hasattr(args, "csv_delimiter"):
		delim = args.csv_delimiter

	try:
		with open(report_file_path, "w") as cf:
			# Write CSV explicit tabular key-value columns header fields
			cf.write("METADATA_PROPERTY{}REGISTERED_VALUE_STRING\n".format(delim))
			
			# Stream out structured rows mapping environmental attributes
			cf.write("filename{}{}\n".format(delim, os.path.basename(target_image_path)))
			cf.write("extracted_at{}{}\n".format(delim, timestamp))
			cf.write("operator_uid{}{}\n".format(delim, getpass.getuser()))
			cf.write("host_node{}{}\n".format(delim, platform.node()))
			cf.write("host_kernel{}{}\n".format(delim, platform.platform().replace(delim, "-")))
			cf.write("process_id{}{}\n".format(delim, os.getpid()))
			
			# Inject immutable cryptographic authentication signatures mapping fields
			cf.write("checksum_md5{}{}\n".format(delim, checksum_dict.get("md5", "NOT_COMPUTED").upper()))
			cf.write("checksum_sha1{}{}\n".format(delim, checksum_dict.get("sha1", "NOT_COMPUTED").upper()))
			cf.write("checksum_sha256{}{}\n".format(delim, checksum_dict.get("sha256", "NOT_COMPUTED").upper()))
			
		return True
	except (IOError, OSError) as e:
		sys.stderr.write("[!] CSV Reporting Engine Failure: " + str(e) + "\n")
		return False
