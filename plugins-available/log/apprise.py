# ==============================================================================
#  XVATOOL PLUGIN - Universal Apprise Multi-Provider Notification Hub Client
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
# -*- coding: utf-8 -*-
"""
Dynamic Apprise logging and notification hub extension module.
Lazy-loads the apprise library backend to grant access to 80+ alerting endpoints.
"""

import os
import sys
import threading

# Track if the optional third-party apprise module is discoverable in the active space
APPRISE_AVAILABLE = False
try:
	import apprise
	APPRISE_AVAILABLE = True
except ImportError:
	pass

def is_supported():
	"""
	Proactive Environment Check. Verifies if the 'apprise' library wrapper
	is successfully installed and accessible within the python site-packages.
	"""
	return APPRISE_AVAILABLE


def register_arguments(parser):
	"""Attaches universal notification routing tokens to the central core parser."""
	group = parser.add_argument_group("Universal Apprise Notification Hub Options")
	group.add_argument("--apprise-url", default=None, action="append",
		help="Specify one or multiple unified Apprise URI targets (e.g., mailto://, twilio://)")


def dispatch_apprise_alert(apprise_urls_list, level, message):
	"""
	Executes synchronous multi-endpoint alert broadcasts within an isolated daemon thread.
	Insulates the active block-level storage array write stream from slow network latency.
	"""
	try:
		# Initialize the native Apprise orchestration asset controller instance
		obj = apprise.Apprise()

		# Register the array of target push providers strings
		for target_url in apprise_urls_list:
			obj.add(target_url)

		# Map internal log levels directly to matching Apprise notification severity types
		type_map = {
			"info": apprise.NotifyType.INFO,
			"warning": apprise.NotifyType.WARNING,
			"error": apprise.NotifyType.FAILURE,
			"critical": apprise.NotifyType.FAILURE
		}
		notify_type = type_map.get(level.lower(), apprise.NotifyType.INFO)

		title_string = "XVATOOL EVENT ALERT: " + level.upper()

		# Execute the dynamic multi-channel broadcast transaction
		obj.send(
			body=message,
			title=title_string,
			notify_type=notify_type
		)
		return True
	except Exception:
		return False


def send_log_event(level, message, args=None):
	"""
	Acts as the primary asynchronous logging hook wrapper inside the category.
	Extracts active target list profiles and passes execution to a detached worker thread.
	"""
	if not is_supported():
		sys.stderr.write("[!] Apprise Hub Error: Third-party 'apprise' python dependency is missing.\n")
		sys.stderr.write("[*] Proactive Remedy: Run 'pip install apprise' to leverage multi-channel alerts.\n")
		return False

	apprise_targets = []
	if args and hasattr(args, "apprise_url") and args.apprise_url:
		apprise_targets = args.apprise_url

	if not apprise_targets:
		# Quietly pass execution back if no alert endpoints are explicitly staged
		return False

	try:
		# Spawn background thread to guarantee complete decoupling from core storage pipelines
		worker = threading.Thread(
			target=dispatch_apprise_alert,
			args=(apprise_targets, level, message)
		)
		worker.daemon = True
		worker.start()
		return True
	except Exception:
		return False
