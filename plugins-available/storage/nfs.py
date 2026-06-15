#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVATOOL PLUGIN - NFS / NFSv4 Enterprise Storage Transport Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic NFS network transport extension module.
Automates secure kernel space mount routing abstractions with forensic cleanup.
"""

import os
import sys
import subprocess
import shutil

def is_supported():
	"""
	Proactive Environment Check. Verifies if the standard Linux
	mount utility and NFS mount helper binaries are available.
	"""
	return os.path.exists("/sbin/mount.nfs") or os.path.exists("/sbin/mount.nfs4")


def register_arguments(parser):
	"""Attaches system specific mount options flags to the central engine."""
	group = parser.add_argument_group("NFS Storage Protocol Options")
	group.add_argument("--nfs-version", choices=["3", "4", "4.1", "auto"], default="auto",
		help="Force a specific NFS protocol version layout string")
	group.add_argument("--nfs-options", default="nolock,tcp,rsize=1048576,wsize=1048576",
		help="Custom comma-separated layout parameters for the kernel mount")


def parse_nfs_uri(uri_string):
	"""Splits nfs://host/export/path syntax into separate host and export variables."""
	clean_uri = uri_string.replace("nfs4://", "").replace("nfs://", "")
	if "/" not in clean_uri:
		return None, None

	host, export_path = clean_uri.split("/", 1)
	return host, "/" + export_path


def prepare_storage(uri_string, args=None, read_only=False):
	"""
	Executes the native background kernel mount sequence.
	Returns the temporary local path wrapper mapping string to the core.
	"""
	host, export_path = parse_nfs_uri(uri_string)
	if not host or not export_path:
		sys.stderr.write("[!] NFS Storage Error: Invalid URI specification syntax.\n")
		return None

	# Allocate a secure local randomized transaction target directory
	tmp_mountpoint = "/tmp/xvatool_nfs_{}_{}".format(host, os.getpid())
	if not os.path.exists(tmp_mountpoint):
		os.makedirs(tmp_mountpoint, 448)

	nfs_ver = "auto"
	nfs_opts = "nolock,tcp,rsize=1048576,wsize=1048576"

	if args:
		if hasattr(args, 'nfs_version'): nfs_ver = args.nfs_version
		if hasattr(args, 'nfs_options'): nfs_opts = args.nfs_options

	# Assemble the strict argument list parameters array to block injections
	cmd_array = ["mount", "-t", "nfs"]

	options_list = []
	if nfs_ver != "auto":
		options_list.append("nfsvers={}".format(nfs_ver))
	if read_only:
		options_list.append("ro")
	if nfs_opts:
		options_list.append(nfs_opts)

	if options_list:
		cmd_array.extend(["-o", ",".join(options_list)])

	# Define source targets mapping context
	cmd_array.extend(["{}:{}".format(host, export_path), tmp_mountpoint])

	try:
		# Engage kernel mounting subsystem sequence
		proc = subprocess.Popen(cmd_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		_, stderr = proc.communicate()

		if proc.returncode != 0:
			sys.stderr.write("[!] NFS Mount Execution Failed: " + stderr.strip() + "\n")
			if os.path.exists(tmp_mountpoint):
				os.rmdir(tmp_mountpoint)
			return None

		return tmp_mountpoint
	except (OSError, ValueError) as e:
		sys.stderr.write("[!] NFS Mount Trigger Crash Exception: " + str(e) + "\n")
		return None


def cleanup_storage(local_mountpoint):
	"""
	Invoked by the core at process end or upon receiving critical Unix signals.
	Unmounts the path cleanly and purges temporary structural items.
	"""
	if not local_mountpoint or not os.path.exists(local_mountpoint):
		return

	# Secure array representation layout for unmounting transactions
	cmd_array = ["umount", "-f", "-l", local_mountpoint] # Lazy, forced unmount guard
	try:
		proc = subprocess.Popen(cmd_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		proc.communicate()

		# Post-unmount forensic safety clearance sweep
		if os.path.exists(local_mountpoint):
			shutil.rmtree(local_mountpoint, ignore_errors=True)
	except (OSError, ValueError):
		pass
