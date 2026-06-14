#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVATOOL PLUGIN - iSCSI / SAN Target Bare-Metal Storage Transport Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic iSCSI storage transport extension module.
Automates secure target discovery, session logging, and bare-metal block stream piping.
"""

import os
import sys
import subprocess

def is_supported():
	"""
	Proactive Environment Check. Verifies if the standard Linux iSCSI administration
	utility 'iscsiadm' is fully discoverable and executable by root roles.
	"""
	binary_name = "iscsiadm"
	path_env = os.environ.get("PATH", "")
	
	is_root = (os.getuid() == 0 if hasattr(os, "getuid") else False)
	if not is_root:
		return False

	for path_dir in path_env.split(os.path.pathsep):
		candidate_path = os.path.join(path_dir, binary_name)
		if os.path.isfile(candidate_path) and os.access(candidate_path, os.X_OK):
			return True
	return False


def register_arguments(parser):
	"""Attaches domain-specific SAN routing and authentication parameters to the engine."""
	group = parser.add_argument_group("iSCSI Storage Area Network Options")
	group.add_argument("--iscsi-iqn", default=None,
		help="Specify the absolute target iSCSI Qualified Name (e.g., ://2026-06.com.san:target)")
	group.add_argument("--iscsi-user", default=None,
		help="Specify the CHAP inbound authentication username token string")
	group.add_argument("--iscsi-pass", default=None,
		help="Specify the CHAP inbound authentication secret password string")


def parse_iscsi_uri(uri_string):
	"""
	Parses iscsi://host:port/portal syntax.
	Extracts network portal addresses from the mapping constraint.
	"""
	clean_uri = uri_string.replace("iscsi://", "")
	if "/" in clean_uri:
		portal, target_suffix = clean_uri.split("/", 1)
	else:
		portal = clean_uri
	
	if ":" not in portal:
		portal = "{}:3260".format(portal) # Fallback to default iSCSI port
		
	return portal


def prepare_storage(uri_string, args=None, read_only=False):
	"""
	Executes the remote target discovery matrix and session login loop.
	Returns the physical mapped local block device node node string (e.g. /dev/sdX) to the core.
	"""
	portal = parse_iscsi_uri(uri_string)
	target_iqn = None
	chap_user = None
	chap_pass = None

	if args:
		if hasattr(args, "iscsi_iqn"): target_iqn = args.iscsi_iqn
		if hasattr(args, "iscsi_user"): chap_user = args.iscsi_user
		if hasattr(args, "iscsi_pass"): chap_pass = args.iscsi_pass

	if not target_iqn:
		sys.stderr.write("[!] iSCSI Storage Error: Target IQN specification mapping (--iscsi-iqn) is mandatory.\n")
		return None

	try:
		# 1. Trigger network target portal discovery sweep
		subprocess.Popen(["iscsiadm", "-m", "discovery", "-t", "st", "-p", portal], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

		# 2. Inject CHAP authentication node properties if provided
		if chap_user and chap_pass:
			subprocess.call(["iscsiadm", "-m", "node", "-T", target_iqn, "-p", portal, "-o", "update", "-n", "node.session.auth.authmethod", "-v", "CHAP"])
			subprocess.call(["iscsiadm", "-m", "node", "-T", target_iqn, "-p", portal, "-o", "update", "-n", "node.session.auth.username", "-v", chap_user])
			subprocess.call(["iscsiadm", "-m", "node", "-T", target_iqn, "-p", portal, "-o", "update", "-n", "node.session.auth.password", "-v", chap_pass])

		# 3. Log in to the target session
		proc = subprocess.Popen(["iscsiadm", "-m", "node", "-T", target_iqn, "-p", portal, "--login"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		_, stderr = proc.communicate()
		if proc.returncode != 0:
			sys.stderr.write("[!] iSCSI Session Login Refused: " + stderr.strip() + "\n")
			return None

		# 4. Block device mapping auto-discovery loop. 
		# We find the new drive node path by tracing the target symlinks inside disk/by-path
		by_path_dir = "/dev/disk/by-path"
		portal_clean = portal.replace(":", "-port-")
		expected_link_substr = "iscsi-{}-{}".format(portal_clean, target_iqn)
		
		# Give the kernel SCSI subsystem a tiny structural breath to populate block nodes
		import time
		time.sleep(1.5)

		if os.path.exists(by_path_dir):
			for entry in os.listdir(by_path_dir):
				if expected_link_substr in entry:
					full_path = os.path.join(by_path_dir, entry)
					local_device = os.path.realpath(full_path)
					print("[*] Target iSCSI Block Allocation successfully mapped to node: " + local_device)
					return local_device

		sys.stderr.write("[!] iSCSI Alignment Error: Login succeeded but failed to resolve local /dev block allocation node.\n")
		return None

	except (OSError, ValueError) as e:
		sys.stderr.write("[!] iSCSI Target Initialization Exception: " + str(e) + "\n")
		return None


def cleanup_storage(uri_string, args=None):
	"""
	Severs active iSCSI session handles during framework teardown or kernel exit signals.
	Logouts out cleanly to prevent ghost allocations inside the SAN matrix.
	"""
	portal = parse_iscsi_uri(uri_string)
	target_iqn = None
	if args and hasattr(args, "iscsi_iqn"):
		target_iqn = args.iscsi_iqn

	if not target_iqn:
		return

	try:
		# Enforce a synchronized physical flush step to block loss states before disconnecting
		subprocess.call(["sync"])
		
		# Log out from the remote block node target session
		subprocess.Popen(["iscsiadm", "-m", "node", "-T", target_iqn, "-p", portal, "--logout"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	except (OSError, ValueError):
		pass
