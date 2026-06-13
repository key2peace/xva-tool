#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVATOOL PLUGIN - Asynchronous Discord Webhook Notification Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic Discord notification extension module.
Dispatches structured rich embed cards within an isolated background thread.
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
	"""Attaches Discord specific webhook parameters to the central core parser."""
	group = parser.add_argument_group("Discord Webhook Alert Options")
	group.add_argument("--discord-webhook", default=None,
		help="Specify the absolute incoming Discord integration webhook endpoint target URL")


def dispatch_discord_payload(webhook_url, payload_dict):
	"""Executes the network post transaction inside an isolated background worker container."""
	try:
		req_headers = {"Content-Type": "application/json", "User-Agent": "xva-tool-forensics/1.0"}
		data_bytes = json.dumps(payload_dict)
		
		request = urllib2.Request(webhook_url, data=data_bytes, headers=req_headers)
		response = urllib2.urlopen(request, timeout=10)
		response.read()
		response.close()
		return True
	except Exception:
		return False


def send_log_event(level, message, args=None):
	"""
	Assembles a structured Discord Embed block layout based on urgency metrics.
	Spawns an asynchronous execution thread instantly to bypass network latency.
	"""
	webhook_target = None
	if args and hasattr(args, "discord_webhook"):
		webhook_target = args.discord_webhook

	if not webhook_target:
		return False

	# Map operational levels to distinct decimal color codes for Discord Embeds
	color_map = {
		"info": 3066993,      # Emerald Green
		"warning": 15105570,   # Orange / Amber
		"error": 15158332,     # Alizarin Crimson Red
		"critical": 16711680   # Pure Red
	}
	embed_color = color_map.get(level.lower(), 3447003) # Default to Blue

	discord_payload = {
		"username": "xva-tool Auditor",
		"avatar_url": "https://github.com",
		"embeds": [
			{
				"title": "⚙️ XVATOOL ORCHESTRATION EVENT: " + level.upper(),
				"description": message,
				"color": embed_color,
				"fields": [
					{
						"name": "Execution Host Node",
						"value": platform.node() if 'platform' in sys.modules else "Storage-Node",
						"inline": True
					},
					{
						"name": "Process ID (PID)",
						"value": str(os.getpid()),
						"inline": True
					}
				],
				"footer": {
					"text": "Core Utility Architect: Alexander Maassen",
					"icon_url": "https://github.com"
				}
			}
		]
	}

	try:
		worker = threading.Thread(
			target=dispatch_discord_payload,
			args=(webhook_target, discord_payload)
		)
		worker.daemon = True
		worker.start()
		return True
	except Exception:
		return False
