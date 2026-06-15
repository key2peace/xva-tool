# ==============================================================================
#  XVATOOL PLUGIN - Structured Compliance XML Audit Logging Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
# -*- coding: utf-8 -*-
"""
Dynamic XML reporting extension module.
Generates structured, compliance-ready XML nodes tracking core data execution steps.
"""

import os
import sys
import time
import platform
import getpass

def is_supported():
	"""Proactive Environment Check. Always returns True as it relies on core Python string blocks."""
	return True


def register_arguments(parser):
	"""Hooks domain specific XML namespace tags variables if needed."""
	pass


def compile_report(target_image_path, checksum_dict, args=None):
	"""Generates a compliance-compliant structured XML document ledger string to disk."""
	report_file_path = target_image_path + ".xml"
	timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

	# Compile structurally sound XML tree representation layout blocks manually
	xml_document = (
		"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
		"<XvaToolAuditReport version=\"1.0.0\">\n"
		"\t<Generator maintainer=\"Alexander Maassen\" email=\"outsider@cuci.nl\"/>\n"
		"\t<EnvironmentContext>\n"
		"\t\t<Timestamp>{}</Timestamp>\n"
		"\t\t<Operator handle=\"{}\" uid=\"{}\"/>\n"
		"\t\t<HostNode>{}</HostNode>\n"
		"\t\t<OperatingSystem>{}</OperatingSystem>\n"
		"\t\t<ProcessID>{}</ProcessID>\n"
		"\t</EnvironmentContext>\n"
		"\t<TargetResource>\n"
		"\t\t<Filename>{}</Filename>\n"
		"\t\t<AbsolutePath>{}</AbsolutePath>\n"
		"\t</TargetResource>\n"
		"\t<CryptographicSignatures>\n"
		"\t\t<Hash algorithm=\"MD5\">{}</Hash>\n"
		"\t\t<Hash algorithm=\"SHA1\">{}</Hash>\n"
		"\t\t<Hash algorithm=\"SHA256\">{}</Hash>\n"
		"\t</CryptographicSignatures>\n"
		"</XvaToolAuditReport>\n"
	).format(
		timestamp, getpass.getuser(), os.getuid() if hasattr(os, 'getuid') else 0,
		platform.node(), platform.platform(), os.getpid(),
		os.path.basename(target_image_path), os.path.abspath(target_image_path),
		checksum_dict.get("md5", "NOT_COMPUTED").upper(),
		checksum_dict.get("sha1", "NOT_COMPUTED").upper(),
		checksum_dict.get("sha256", "NOT_COMPUTED").upper()
	)

	try:
		with open(report_file_path, "w") as xf:
			xf.write(xml_document)
		return True
	except (IOError, OSError) as e:
		sys.stderr.write("[!] XML Reporting Engine Failure: " + str(e) + "\n")
		return False
