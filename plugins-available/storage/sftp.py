# ==============================================================================
#  XVATOOL PLUGIN - SFTP / SSHFS Enterprise Secure Storage Transport Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
# -*- coding: utf-8 -*-
"""
Dynamic SFTP network transport extension module using SSHFS FUSE.
Automates secure encrypted storage routing abstractions with signal cleanup guards.
"""

import os
import sys
import subprocess
import shutil

def is_supported():
	"""
	Proactive Environment Check. Verifies if the standard Linux FUSE
	sshfs utility binary is fully discoverable and executable.
	"""
	binary_name = "sshfs"
	path_env = os.environ.get("PATH", "")

	for path_dir in path_env.split(os.path.pathsep):
		candidate_path = os.path.join(path_dir, binary_name)
		if os.path.isfile(candidate_path) and os.access(candidate_path, os.X_OK):
			return True
	return False


def register_arguments(parser):
	"""Attaches domain-specific SSH performance options to the central parser."""
	group = parser.add_argument_group("SFTP/SSHFS Storage Protocol Options")
	group.add_argument("--ssh-port", type=int, default=22,
		help="Specify the remote target machine SSH port network constraint")
	group.add_argument("--ssh-options", default="Ciphers=aes128-gcm@openssh.com,compression=no",
		help="Enforce fast cryptographic ciphers to optimize CPU overhead on RAID streams")


def parse_sftp_uri(uri_string):
	"""
	Parses sftps://user@host:port/path or sshfs:// layout variants.
	Extracts and isolates credentials from the physical resource string.
	"""
	clean_uri = uri_string.replace("sftps://", "").replace("sshfs://", "")

	# Extract remote target path layout
	if "/" not in clean_uri:
		return None, None, None
	connection_part, remote_path = clean_uri.split("/", 1)
	remote_path = "/" + remote_path

	# Extract optional non-standard port override within URI string
	port = None
	if "]:" in connection_part and connection_part.startswith("["): # IPv6 bracket guard
		host_part, port_part = connection_part.rsplit(":", 1)
		connection_part = host_part.strip("[]")
		port = port_part
	elif ":" in connection_part and not connection_part.startswith("["):
		connection_part, port_part = connection_part.rsplit(":", 1)
		port = port_part

	user_host = connection_part
	return user_host, remote_path, port


def prepare_storage(uri_string, args=None, read_only=False):
	"""
	Executes the remote FUSE layer secure mount sequence.
	Returns the temporary local staging location string straight to the core.
	"""
	user_host, remote_path, uri_port = parse_sftp_uri(uri_string)
	if not user_host or not remote_path:
		sys.stderr.write("[!] SFTP Storage Error: Malformed secure URI definition syntax.\n")
		return None

	# Resolve active port assignments priorities
	ssh_port = "22"
	if uri_port:
		ssh_port = str(uri_port)
	elif args and hasattr(args, "ssh_port"):
		ssh_port = str(args.ssh_port)

	ssh_opts = "Ciphers=aes128-gcm@openssh.com,compression=no"
	if args and hasattr(args, "ssh_options"):
		ssh_opts = args.ssh_options

	# Provision localized unprivileged secure mountpoint directory nodes
	pid = os.getpid()
	tmp_mountpoint = "/tmp/xvatool_sftp_{}_{}".format(pid, user_host.replace("@", "_"))
	if not os.path.exists(tmp_mountpoint):
		os.makedirs(tmp_mountpoint, 448)

	# Construct strict array presentation layout parameters to fully seal injection flaws
	cmd_array = [
		"sshfs",
		"{}:{}".format(user_host, remote_path),
		tmp_mountpoint,
		"-p", ssh_port,
		"-o", "reconnect,ServerAliveInterval=15,ServerAliveCountMax=3"
	]

	# Append custom optimizations or read-only constraints onto the execution arrays
	options_extended = []
	if read_only:
		options_extended.append("ro")
	if ssh_opts:
		# SSH options must be passed individually via standard -o token formatting rules
		for opt in ssh_opts.split(","):
			options_extended.append("o={}".format(opt))

	if options_extended:
		for opt_entry in options_extended:
			cmd_array.extend(["-o", opt_entry])

	try:
		# Engage userspace background mounting procedures
		proc = subprocess.Popen(cmd_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		_, stderr = proc.communicate()

		if proc.returncode != 0:
			sys.stderr.write("[!] SFTP SSHFS Layer Mount Failed: " + stderr.strip() + "\n")
			sys.stderr.write("[*] Note: Ensure passwordless SSH public-key entry constraints are verified.\n")
			if os.path.exists(tmp_mountpoint):
				os.rmdir(tmp_mountpoint)
			return None

		return tmp_mountpoint
	except (OSError, ValueError) as e:
		sys.stderr.write("[!] SFTP Mount Execution Abruptly Aborted: " + str(e) + "\n")
		return None


def cleanup_storage(local_mountpoint):
	"""
	Severs active FUSE connection lines forcefully during clean exits
	or when intercepting unexpected Unix termination execution paths.
	"""
	if not local_mountpoint or not os.path.exists(local_mountpoint):
		return

	# Secure array presentation layout targeting immediate unmounting
	cmd_array = ["fusermount", "-u", "-z", local_mountpoint] # Lazy unmount guard loop
	try:
		proc = subprocess.Popen(cmd_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		proc.communicate()

		# Clear outstanding remnants from filesystem workspace scopes
		if os.path.exists(local_mountpoint):
			shutil.rmtree(local_mountpoint, ignore_errors=True)
	except (OSError, ValueError):
		pass
