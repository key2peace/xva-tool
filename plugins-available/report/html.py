#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVATOOL PLUGIN - Responsive HTML5 Visual Audit Dashboard Report Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic HTML reporting extension module.
Compiles a self-contained, responsive bootstrap-styled visualization dashboard.
"""

import os
import sys
import time
import platform
import getpass

def is_supported():
	"""Proactive Environment Check. Always returns True as it relies on core Python."""
	return True


def register_arguments(parser):
	"""Attaches visual configuration properties to the central engine."""
	group = parser.add_argument_group("HTML Dashboard Reporting Options")
	group.add_argument("--html-title", default="xva-tool Storage Extraction Report",
		help="Set the specific title header string inside the generated HTML page")


def compile_report(target_image_path, checksum_dict, args=None):
	"""
	Generates a fully self-contained HTML5 diagnostic asset file
	directly alongside the extracted volume output path.
	"""
	report_file_path = target_image_path + ".html"
	timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

	page_title = "xva-tool Storage Extraction Report"
	if args and hasattr(args, "html_title"):
		page_title = args.html_title

	try:
		with open(report_file_path, "w") as hf:
			hf.write("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n")
			hf.write("\t<meta charset=\"UTF-8\">\n")
			hf.write("\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n")
			hf.write("\t<title>{}</title>\n".format(page_title))

			# Embed thin responsive CSS rules directly into the file layout bounds
			hf.write("\t<style>\n")
			hf.write("\t\tbody { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f4f6f9; color: #333; margin: 0; padding: 20px; }\n")
			hf.write("\t\t.container { max-width: 1100px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }\n")
			hf.write("\t\th1 { color: #1e3a8a; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; margin-top: 0; }\n")
			hf.write("\t\t.grid-metrics { display: flex; gap: 20px; margin-bottom: 30px; }\n")
			hf.write("\t\t.card { flex: 1; background: #f8fafc; padding: 20px; border-radius: 6px; border: 1px solid #e2e8f0; }\n")
			hf.write("\t\t.card h3 { margin-top: 0; color: #475569; font-size: 14px; text-transform: uppercase; }\n")
			hf.write("\t\t.card p { margin: 5px 0 0 0; font-size: 18px; font-weight: bold; color: #0f172a; }\n")
			hf.write("\t\ttable { width: 100%; border-collapse: collapse; margin-bottom: 30px; }\n")
			hf.write("\t\tth, td { text-align: left; padding: 12px; border-bottom: 1px solid #e2e8f0; }\n")
			hf.write("\t\tth { background: #f1f5f9; color: #334155; }\n")
			hf.write("\t\t.badge { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; color: #fff; }\n")
			hf.write("\t\t.badge-success { background: #10b981; }\n")
			hf.write("\t\t.footer { text-align: center; color: #94a3b8; font-size: 12px; margin-top: 4px; padding-top: 20px; border-top: 1px solid #e5e7eb; }\n")
			hf.write("\t</style>\n</head>\n<body>\n")

			hf.write("<div class=\"container\">\n")
			hf.write("\t<h1>💾 Storage Extraction Matrix Analytics</h1>\n")

			# Render tracking metrics overview summary row cards
			hf.write("\t<div class=\"grid-metrics\">\n")
			hf.write("\t\t<div class=\"card\"><h3>Status</h3><p><span class=\"badge badge-success\">SUCCESS</span></p></div>\n")
			hf.write("\t\t<div class=\"card\"><h3>Target Image</h3><p>{}</p></div>\n".format(os.path.basename(target_image_path)))
			hf.write("\t\t<div class=\"card\"><h3>Verification Date</h3><p>{}</p></div>\n".format(timestamp))
			hf.write("\t</div>\n")

			# Render detailed administrative system metadata listings
			hf.write("\t<h2>📋 Execution Environment Details</h2>\n")
			hf.write("\t<table>\n")
			hf.write("\t\t<tr><th>Attribute Key</th><th>Registered Value String</th></tr>\n")
			hf.write("\t\t<tr><td>Operator Handle</td><td>{} (UID={})</td></tr>\n".format(getpass.getuser(), os.getuid() if hasattr(os, 'getuid') else 0))
			hf.write("\t\t<tr><td>Host Server Node Name</td><td>{}</td></tr>\n".format(platform.node()))
			hf.write("\t\t<tr><td>Operating System Kernel</td><td>{}</td></tr>\n".format(platform.platform()))
			hf.write("\t\t<tr><td>Execution Process ID (PID)</td><td>{}</td></tr>\n".format(os.getpid()))
			hf.write("\t</table>\n")

			# Render cryptographic forensic check tables
			hf.write("\t<h2>🔒 Cryptographic Validation Checksums</h2>\n")
			hf.write("\t<table>\n")
			hf.write("\t\t<tr><th>Algorithm</th><th>Immutable Fingerprint Matrix Hash Value</th></tr>\n")
			hf.write("\t\t<tr><td><b>MD5</b></td><td><code>{}</code></td></tr>\n".format(checksum_dict.get("md5", "NOT_COMPUTED").upper()))
			hf.write("\t\t<tr><td><b>SHA-1</b></td><td><code>{}</code></td></tr>\n".format(checksum_dict.get("sha1", "NOT_COMPUTED").upper()))
			hf.write("\t\t<tr><td><b>SHA-256</b></td><td><code>{}</code></td></tr>\n".format(checksum_dict.get("sha256", "NOT_COMPUTED").upper()))
			hf.write("\t</table>\n")

			hf.write("\t<div class=\"footer\">Orchestration Engine Core designed and maintained by Alexander Maassen &lt;outsider@cuci.nl&gt;</div>\n")
			hf.write("</div>\n")
			hf.write("</body>\n</html>\n")

		return True
	except (IOError, OSError) as e:
		sys.stderr.write("[!] HTML Reporting Engine Failure: " + str(e) + "\n")
		return False
