# ==============================================================================
#  XVATOOL PLUGIN - Remote RFC 5424 Syslog Network Aggregator Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
# -*- coding: utf-8 -*-
"""
Dynamic remote syslog extension module.
Dispatches structured logging frames over UDP or TCP to central SIEM nodes.
"""

import os
import sys
import socket
import platform

def is_supported():
	"""Proactive Environment Check. Always returns True as it utilizes socket layers."""
	return True


def register_arguments(parser):
	"""Attaches central syslog target networking configurations to the engine."""
	group = parser.add_argument_group("Remote Syslog Aggregation Options")
	group.add_argument("--syslog-host", default="localhost",
		help="Specify the remote syslog collection server IP or domain hostname")
	group.add_argument("--syslog-port", type=int, default=514,
		help="Specify the network UDP/TCP port boundary for syslog input (Default: 514)")
	group.add_argument("--syslog-proto", choices=["udp", "tcp"], default="udp",
		help="Enforce a specific network socket layer transport protocol rule")


def send_log_event(level, message, args=None):
	"""
	Formats and transmits a standard syslog frame to centralized aggregators.
	Utilizes strict RFC 5424 structural envelope properties mapping variables.
	"""
	syslog_host = "localhost"
	syslog_port = 514
	syslog_proto = "udp"

	if args:
		if hasattr(args, "syslog_host"): syslog_host = args.syslog_host
		if hasattr(args, "syslog_port"): syslog_port = args.syslog_port
		if hasattr(args, "syslog_proto"): syslog_proto = args.syslog_proto

	# Facility 24 (User-Level Messages) shifted into standard priority calculation matrices
	# Priority = (Facility * 8) + Severity
	severity_map = {"info": 6, "warning": 4, "error": 3, "critical": 2}
	severity_code = severity_map.get(level.lower(), 5)
	priority = (1 << 3) + severity_code # User context shift mapping

	timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
	hostname = platform.node()
	pid = os.getpid()

	# Build valid RFC 5424 structured syslog data packet layout string
	syslog_envelope = "<{}>1 {} {} xva-tool {} ID42 - {}\n".format(
		priority, timestamp, hostname, pid, message
	)

	try:
		# Socket allocation based on transport protocol specifications
		if syslog_proto.lower() == "tcp":
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(2.0)
			sock.connect((syslog_host, syslog_port))
			sock.sendall(syslog_envelope)
		else:
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.sendto(syslog_envelope, (syslog_host, syslog_port))

		sock.close()
		return True
	except (socket.error, IOError, OSError):
		# Silently fail-safe to avoid disrupting storage streams over networking locks
		return False
