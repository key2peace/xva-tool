#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVATOOL PLUGIN - Windows Samba / CIFS Enterprise Storage Transport Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic SMB/Samba network transport extension module.
Automates secure CIFS kernel mounts with credentials isolation and forensic cleanup.
"""

import os
import sys
import subprocess
import shutil

def is_supported():
	"""
	Proactive Environment Check. Verifies if the standard Linux CIFS mount helper
	binary is fully discoverable and executable within the system paths.
	"""
	return os.path.exists("/sbin/mount.cifs")


def register_arguments(parser):
	"""Attaches Samba specific protocol and authentication flags to the central engine."""
	group = parser.add_argument_group("Samba / CIFS Storage Protocol Options")
	group.add_argument("--smb-version", default="3.0",
		help="Enforce a specific SMB dialect version layout layout (e.g., 2.1, 3.0, 3.1.1)")
	group.add_argument("--smb-options", default="iocharset=utf8,noperm",
		help="Custom comma-separated layout parameters for the CIFS kernel mount")


def parse_smb_uri(uri_string):
	"""
	Parses smb://user:pass@host/share/path layout variants.
	Isolates credentials cleanly from network host strings.
	"""
	clean_uri = uri_string.replace("smb://", "").replace("cifs://", "")

	if "/" not in clean_uri:
		return None, None, None, None

	credentials_part, share_path = clean_uri.split("/", 1)
	share_path = "/" + share_path

	if "@" in credentials_part:
		user_pass, host = credentials_part.split("@", 1)
		if ":" in user_pass:
			user, password = user_pass.split(":", 1)
		else:
			user, password = user_pass, None
	else:
		host = credentials_part
		user, password = "guest", ""

	# Isolate the base share name from the nested directories
	share_parts = [p for p in share_path.split("/") if p]
	if not share_parts:
		return None, None, None, None

	base_share = share_parts[0]
	nested_path = "/" + "/".join(share_parts[1:]) if len(share_parts) > 1 else "/"

	return user, password, host, {"share": base_share, "nested": nested_path}


def prepare_storage(uri_string, args=None, read_only=False):
	"""
	Executes the secure CIFS kernel space mount sequence using a credentials file.
	Returns the local temporary path workspace mapping straight to the core.
	"""
	user, password, host, paths = parse_smb_uri(uri_string)
	if not host or not paths:
		sys.stderr.write("[!] SMB Storage Error: Invalid Samba URI specification syntax.\n")
		return None

	pid = os.getpid()
	tmp_mountpoint = "/tmp/xvatool_smb_{}_{}".format(pid, host)
	if not os.path.exists(tmp_mountpoint):
		os.makedirs(tmp_mountpoint, 448)

	# Security Guard: Write credentials to a separate 384 file to hide passwords from ps aux
	cred_file = "/tmp/xvatool_smb_cred_{}".format(pid)
	try:
		with open(cred_file, "w") as cf:
			os.chmod(cred_file, 384)
			cf.write("username={}\n".format(user))
			if password:
				cf.write("password={}\n".format(password))
	except (IOError, OSError) as e:
		sys.stderr.write("[!] SMB Storage Error: Failed to allocate secure credentials swap: " + str(e) + "\n")
		if os.path.exists(tmp_mountpoint): os.rmdir(tmp_mountpoint)
		return None

	smb_ver = "3.0"
	smb_opts = "iocharset=utf8,noperm"

	if args:
		if hasattr(args, 'smb_version'): smb_ver = args.smb_version
		if hasattr(args, 'smb_options'): smb_opts = args.smb_options

	# Assemble strict argument structures arrays to prevent execution injections
	cmd_array = [
		"mount", "-t", "cifs",
		"//{}/{}".format(host, paths["share"]),
		tmp_mountpoint,
		"-o", "credentials={},vers={}".format(cred_file, smb_ver)
	]

	options_list = []
	if read_only:
		options_list.append("ro")
	if smb_opts:
		options_list.append(smb_opts)

	if options_list:
		cmd_array[-1] += "," + ",".join(options_list)

	try:
		proc = subprocess.Popen(cmd_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		_, stderr = proc.communicate()

		# Always wipe the localized plaintext credentials file from disk immediately
		if os.path.exists(cred_file):
			os.remove(cred_file)

		if proc.returncode != 0:
			sys.stderr.write("[!] SMB Mount Execution Failed: " + stderr.strip() + "\n")
			if os.path.exists(tmp_mountpoint): os.rmdir(tmp_mountpoint)
			return None

		# Return the mounted base path combined with any nested paths to the core router
		final_mapped_path = os.path.join(tmp_mountpoint, paths["nested"].lstrip("/"))
		return final_mapped_path
	except (OSError, ValueError) as e:
		if os.path.exists(cred_file): os.remove(cred_file)
		sys.stderr.write("[!] SMB Mount Initialization Exception: " + str(e) + "\n")
		return None


def cleanup_storage(local_mapped_path):
	"""
	Severs active Samba connection structures cleanly. Unmounts the target
	and purges localized staging environments from the filesystem layout.
	"""
	if not local_mapped_path:
		return

	# Extract the original root mountpoint directory from the mapped path string
	parts = local_mapped_path.split("/")
	base_indices = [i for i, p in enumerate(parts) if p.startswith("xvatool_smb_")]
	if not base_indices:
		return

	local_mountpoint = "/".join(parts[:base_indices[0] + 1])

	if not os.path.exists(local_mountpoint):
		return

	cmd_array = ["umount", "-f", "-l", local_mountpoint] # Forced lazy unmount guard
	try:
		proc = subprocess.Popen(cmd_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		proc.communicate()

		if os.path.exists(local_mountpoint):
			shutil.rmtree(local_mountpoint, ignore_errors=True)
	except (OSError, ValueError):
		pass
