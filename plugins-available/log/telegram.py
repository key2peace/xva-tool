#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVATOOL PLUGIN - Asynchronous Telegram Bot API Notification Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic Telegram notification extension module.
Dispatches administrative telemetry alerts using clean HTML text string encoding.
"""

import os
import sys
import threading
import urllib
import urllib2

def is_supported():
	"""Proactive Environment Check. Always returns True as it uses pure Python core modules."""
	return True


def register_arguments(parser):
	"""Attaches private Telegram bot authentication parameters to the engine parser."""
	group = parser.add_argument_group("Telegram Bot Alert Options")
	group.add_argument("--telegram-token", default=None,
		help="Specify the unique secret HTTP API authentication token string for the bot")
	group.add_argument("--telegram-chat-id", default=None,
		help="Specify the target private administrative conversation chat ID number entry")


def dispatch_telegram_message(bot_token, chat_id, encoded_text):
	"""Executes the synchronous remote API transaction inside an unlinked daemon thread."""
	api_url = "https://telegram.org{}/sendMessage".format(bot_token)
	post_fields = {
		"chat_id": chat_id,
		"text": encoded_text,
		"parse_mode": "HTML",
		"disable_web_page_preview": "true"
	}
	
	try:
		req_headers = {"User-Agent": "xva-tool-forensics/1.0"}
		data_bytes = urllib.urlencode(post_fields)
		
		request = urllib2.Request(api_url, data=data_bytes, headers=req_headers)
		response = urllib2.urlopen(request, timeout=10)
		response.read()
		response.close()
		return True
	except Exception:
		return False


def send_log_event(level, message, args=None):
	"""
	Formats a sanitized HTML text layout segment targeting Telegram chat rendering.
	Spawns an asynchronous worker container to ensure zero processing queue latency.
	"""
	bot_token = None
	chat_id = None
	
	if args:
		if hasattr(args, "telegram_token"): bot_token = args.telegram_token
		if hasattr(args, "telegram_chat_id"): chat_id = args.telegram_chat_id

	if not bot_token or not chat_id:
		return False

	# Format urgency markers with specific emoji layouts
	emoji_map = {"info": "ℹ️", "warning": "⚠️", "error": "🚨", "critical": "💀"}
	emoji = emoji_map.get(level.lower(), "🔔")

	# Assemble the clean HTML-compliant layout string block
	formatted_text = (
		"<b>{} XVATOOL PIPELINE EVENT: {}</b>\n"
		"<code>--------------------------------</code>\n"
		"<b>Message:</b> {}\n"
		"<b>Host Node:</b> {}\n"
		"<b>PID:</b> <code>{}</code>\n\n"
		"<i>Maintainer: Alexander Maassen</i>"
	).format(
		emoji, level.upper(), message,
		os.uname() if hasattr(os, "uname") else "Storage-Node",
		os.getpid()
	)

	try:
		worker = threading.Thread(
			target=dispatch_telegram_message,
			args=(bot_token, chat_id, formatted_text)
		)
		worker.daemon = True
		worker.start()
		return True
	except Exception:
		return False
