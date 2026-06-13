#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVATOOL PLUGIN - Asynchronous Slack Incoming Webhook Notification Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic Slack notification extension module.
Dispatches micro-managed JSON alert cards within an isolated background thread.
"""

import os
import sys
import threading
import json
import urllib2

def is_supported():
	"""Proactive Environment Check. Always returns True as it uses pure Python core modules."""
	return True


def register_arguments(parser):
	"""Attaches domain-specific communication flags to the central core parser."""
	group = parser.add_argument_group("Slack Webhook Alert Options")
	group.add_argument("--slack-webhook", default=None,
		help="Specify the absolute incoming Slack integration webhook endpoint target URL")
	group.add_argument("--slack-channel", default=None,
		help="Override the default workspace target channel designation string")


def dispatch_slack_payload(webhook_url, payload_dict):
	"""
	Executes the synchronous network post transaction inside an isolated execution container.
	Prevents internet responses or socket timeouts from stalling active disk I/O streams.
	"""
	try:
		req_headers = {"Content-Type": "application/json"}
		data_bytes = json.dumps(payload_dict)
		
		# Invoke pure Python url handlers to bypass command execution security issues completely
		request = urllib2.Request(webhook_url, data=data_bytes, headers=req_headers)
		response = urllib2.urlopen(request, timeout=10)
		response.read()
		response.close()
		return True
	except Exception:
		# Safely swallow transport errors to prevent diagnostic notifications from blocking the terminal
		return False


def trigger_notification(level, event_title, execution_details, args=None):
	"""
	Assembles a rich Slack payload block card layout based on event urgency metrics.
	Spawns an asynchronous background thread instantly to handle the transmission loop.
	"""
	# Check for command line parameters or fall back straight to cascaded configuration states
	webhook_target = None
	channel_override = None
	
	if args:
		if hasattr(args, "slack_webhook"): webhook_target = args.slack_webhook
		if hasattr(args, "slack_channel"): channel_override = args.slack_channel

	if not webhook_target:
		# Silently abort if no valid notification routing path has been provisioned
		return False

	# Map operational levels to distinct color codes (Green for health, Red for structural faults)
	color_map = {
		"info": "#2eb886",      # Operational Green
		"warning": "#e8a71c",   # Amber Warning Layout
		"error": "#de0e2d",     # Red High Severity
		"critical": "#ff0000"   # Red Disaster Core
	}
	card_color = color_map.get(level.lower(), "#439fe0") # Default to Industrial Blue

	# Assemble the standardized enterprise attachment JSON schema mapping layout
	slack_payload = {
		"attachments": [
			{
				"fallback": "[xva-tool Alert] {}: {}".format(event_title.upper(), execution_details),
				"color": card_color,
				"pretext": "🔔 *xva-tool Infrastructure Notification Alert*",
				"title": event_title.upper(),
				"text": execution_details,
				"fields": [
					{
						"title": "Execution Host Node",
						"value": os.uname()[1] if hasattr(os, "uname") else "Storage-Server",
						"short": True
					},
					{
						"title": "Severity Tier",
						"value": level.upper(),
						"short": True
					}
				],
				"footer": "Orchestration Blueprint maintained by Alexander Maassen",
				"ts": int(threading.time.time()) if hasattr(threading, "time") else int(urllib2.time.time())
			}
		]
	}

	if channel_override:
		slack_payload["channel"] = channel_override

	# Spawning phase: Dispatch the task asynchronously onto a non-blocking background thread worker
	try:
		worker = threading.Thread(
			target=dispatch_slack_payload,
			args=(webhook_target, slack_payload)
		)
		worker.daemon = True # Detach lifecycle bounds from the parent binary execution thread
		worker.start()
		return True
	except Exception:
		return False
