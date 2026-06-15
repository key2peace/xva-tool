# ==============================================================================
#  XVATOOL PLUGIN - Systemd Journald Native Socket Logging Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
# -*- coding: utf-8 -*-
"""
Dynamic systemd journal extension module.
Pipes structured orchestration logs directly into the Linux systemd socket.
"""

import os
import sys
import socket

# Standard systemd journal socket path designation mapping
JOURNALD_SOCKET = "/run/systemd/journal/socket"

def is_supported():
	"""
	Proactive Environment Check. Verifies if the host operating system
	is running systemd and the binaire journald socket is writable.
	"""
	return os.path.exists(JOURNALD_SOCKET) and os.access(JOURNALD_SOCKET, os.W_OK)


def register_arguments(parser):
	"""Attaches systemd syslog facility codes mapping filters if required."""
	group = parser.add_argument_group("Systemd Journald Engine Options")
	group.add_argument("--journal-identifier", default="xva-tool",
		help="Enforce a specific syslog identifier string inside journalctl loops")


def send_to_journal(level, message, args=None):
	"""
	Pipes a structurally formatted payload block directly to the kernel socket.
	Utilizes native systemd field variables mapping (PRIORITY, SYSLOG_IDENTIFIER).
	"""
	syslog_id = "xva-tool"
	if args and hasattr(args, 'journal_identifier'):
		syslog_id = args.journal_identifier

	# Map framework log levels directly to standard syslog priority integers
	priority_map = {
		"info": "6",      # LOG_INFO
		"warning": "4",   # LOG_WARNING
		"error": "3",     # LOG_ERR
		"critical": "2"   # LOG_CRIT
	}
	priority = priority_map.get(level.lower(), "5") # Default to LOG_NOTICE

	# Format the structured multi-line string block required by the journald stream API
	payload = (
		"MESSAGE={}\n"
		"PRIORITY={}\n"
		"SYSLOG_IDENTIFIER={}\n"
		"CODE_FILE=xva-tool\n"
		"OPERATOR_UID={}\n"
	).format(message, priority, syslog_id, os.getuid() if hasattr(os, 'getuid') else 0)

	try:
		# Open a UNIX datagram socket to transmit the data instantly into RAM kernel space
		sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
		sock.connect(JOURNALD_SOCKET)
		sock.sendall(payload)
		sock.close()
		return True
	except (socket.error, IOError, OSError):
		# Silently fall back if the socket blocks or context switching fails
		return False
