#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVATOOL PLUGIN - Bare-Metal USB / Raw Block Device Direct Flash Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic USB/Raw block flash transport module.
Enforces strict multi-tier mount verification and direct kernel O_DIRECT writes.
"""

import os
import sys

def is_supported():
	"""
	Proactive Environment Check. Verifies if the operating system 
	exposes access to native block storage device trees inside /dev.
	"""
	return os.path.exists("/dev") and hasattr(os, "O_DIRECT")


def register_arguments(parser):
	"""Attaches safe block validation flags to the core parser infrastructure."""
	group = parser.add_argument_group("Bare-Metal Raw Block Flashing Options")
	group.add_argument("--usb-block-size", type=int, default=4096,
		help="Enforce a specific block storage sector write alignment size (Default: 4096)")


def verify_device_safety(device_path):
	"""
	Executes rigorous background checks against /proc/mounts to verify 
	that no logical partition on the target physical storage is actively mounted.
	"""
	if not device_path.startswith("/dev/"):
		return False

	base_device = os.path.basename(device_path)
	
	try:
		if os.path.exists("/proc/mounts"):
			with open("/proc/mounts", "r") as f:
				for line in f:
					parts = line.split()
					if not parts:
						continue
					mount_source = parts[0]
					
					# Intercept if the device identifier matches any mounted node
					if base_device in mount_source:
						sys.stderr.write("[!] CRITICAL ACCESSIBILITY ALERT: Target drive block is currently active inside the OS!\n")
						sys.stderr.write("[!] Active mount configuration discovered: " + line.strip() + "\n")
						return False
		return True
	except (IOError, OSError):
		# Fall back to strict failure state if the environment state is ambiguous
		return False


def get_direct_write_handle(device_path, args=None):
	"""
	Opens the raw block device node directly bypassing the OS page cache entirely.
	Enforces privileged role checks and target alignment safety bounds.
	"""
	# 1. Enforce strict root operational privilege boundaries
	if os.getuid() != 0:
		sys.stderr.write("[!] Privilege Violation: Direct drive sector flashing requires root execution.\n")
		return None

	# 2. Run the logical block mount verification routine
	if not verify_device_safety(device_path):
		sys.stderr.write("[!] Execution Aborted: Target location contains active logical volume alignments.\n")
		return None

	block_size = 4096
	if args and hasattr(args, "usb_block_size"):
		block_size = args.usb_block_size

	try:
		# 3. Direct I/O Layer Injection: Open the file descriptor with flags
		# os.O_WRONLY: Open for binary writing
		# os.O_DIRECT: Completely bypasses the Linux kernel page cache memory pools
		# os.O_SYNC: Enforces immediate physical sector level cache flushes
		flags = os.O_WRONLY | os.O_DIRECT | os.O_SYNC
		
		fd = os.open(device_path, flags)
		
		# Define a basic Stream Wrapper Object mimicking standard file objects to return to the core
		class DirectIOBlockStreamWrapper(object):
			def __init__(self, raw_fd, b_size):
				self.fd = raw_fd
				self.block_size = b_size
				self.closed = False

			def write(self, binary_payload):
				"""Writes data ensuring alignment bounds conform to O_DIRECT parameters."""
				payload_len = len(binary_payload)
				
				# Ensure incoming memory addresses line up precisely with kernel constraints
				if payload_len % self.block_size != 0:
					# Pad trailing remnants with binary null bytes to preserve grid boundaries
					padding_needed = self.block_size - (payload_len % self.block_size)
					binary_payload += "\0" * padding_needed
				
				try:
					os.write(self.fd, binary_payload)
					return True
				except OSError as e:
					sys.stderr.write("[!] Sector Level Hardware I/O Exception: " + str(e) + "\n")
					return False

			def close(self):
				if not self.closed:
					try:
						os.close(self.fd)
					except OSError:
						pass
					self.closed = True

			def terminate(self):
				self.close()

			def wait(self):
				self.close()
				return 0

		return DirectIOBlockStreamWrapper(fd, block_size)

	except (OSError, ValueError) as e:
		sys.stderr.write("[!] Raw Block Storage Deployment Failure: " + str(e) + "\n")
		return None
