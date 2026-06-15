#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVATOOL PLUGIN - Cascading Local File Logger & Auto-Rotation Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic local file logging extension module.
Handles automated permission downgrades and runtime file rotation size limits.
"""

import os
import sys
import time

def is_supported():
	"""Proactive Environment Check. Always returns True as it utilizes core Python."""
	return True


def register_arguments(parser):
	"""Attaches file logging path parameters to the core framework parser."""
	group = parser.add_argument_group("Local File Logging Options")
	group.add_argument("--log-file-path", default=None,
		help="Manually override the file destination path layout for xva-tool.log")


def resolve_log_destination(args=None):
	"""Dynamic cascade routing path detection based on execution privileges (UID)."""
	if args and hasattr(args, "log_file_path") and args.log_file_path:
		return args.log_file_path

	# Check for root privilege to execute global system logging
	if os.getuid() == 0 if hasattr(os, "getuid") else False:
		target_dir = "/var/log"
	else:
		target_dir = os.path.expanduser("~/.local/share/xva-tool")

	if not os.path.exists(target_dir):
		try:
			os.makedirs(target_dir, 488)
		except OSError:
			target_dir = "./logs" # Fallback straight to local workspace context
			if not os.path.exists(target_dir):
				os.makedirs(target_dir)

	return os.path.join(target_dir, "xva-tool.log")


def enforce_log_rotation(log_path, max_size_mb=50):
	"""Checks active size metrics and triggers a clean rollover if limits are breached."""
	if not os.path.exists(log_path):
		return

	try:
		file_size_bytes = os.path.getsize(log_path)
		max_bytes = max_size_mb * 1024 * 1024

		if file_size_bytes >= max_bytes:
			# Shift historic logs down the archive chain pipeline
			backup_path = log_path + ".1"
			if os.path.exists(backup_path):
				os.remove(backup_path)
			os.rename(log_path, backup_path)
	except (IOError, OSError):
		pass


def send_log_event(level, message, args=None, max_size_mb=50):
	"""Appends structural logs entries to file targets with strict rotation checks."""
	log_path = resolve_log_destination(args)
	enforce_log_rotation(log_path, max_size_mb)

	timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
	log_entry = "[{}] [{}] {}\n".format(timestamp, level.upper(), message)

	try:
		with open(log_path, "a") as f:
			f.write(log_entry)
		return True
	except (IOError, OSError):
		return False
