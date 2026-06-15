#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVATOOL PLUGIN - Hybrid Bootable ISO 9660 Generation Engine
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic ISO compilation format extension module.
Evaluates Sector 0 binary structures on-the-fly to trigger El Torito boot emulation.
"""

import os
import sys
import subprocess
import shutil

def is_supported():
	"""
	Proactive Environment Check. Verifies if the host has genisoimage,
	xorriso, or isohybrid system binaries discoverable inside the PATH.
	"""
	for binary in ["genisoimage", "xorriso", "mkisofs"]:
		path_env = os.environ.get("PATH", "")
		for path_dir in path_env.split(os.path.pathsep):
			if os.path.isfile(os.path.join(path_dir, binary)):
				return True
	return False


def register_arguments(parser):
	"""Attaches ISO compilation volume descriptor flags to the core parser layer."""
	group = parser.add_argument_group("ISO Media Format Options")
	group.add_argument("--iso-volume-id", default="XVA_EXTRACTED_MEDIA",
		help="Specify the standard ISO 9660 volume identification label string")
	group.add_argument("--iso-publisher", default="Alexander Maassen",
		help="Specify the publisher metadata text embedded inside the ISO header")


def get_write_pipeline(target_path, args=None):
	"""
	Secure Downstream Pipe Provisioning. We initialize a temporary directory
	structure where the raw stream blocks will be evaluated before final compilation.
	"""
	vol_id = "XVA_EXTRACTED_MEDIA"
	publisher_str = "Alexander Maassen"

	if args:
		if hasattr(args, 'iso_volume_id'): vol_id = args.iso_volume_id
		if hasattr(args, 'iso_publisher'): publisher_str = args.iso_publisher

	# Allocate a secure transaction workspace directory layout
	pid = os.getpid()
	workspace_dir = "/tmp/xvatool_iso_workspace_{}".format(pid)
	if not os.path.exists(workspace_dir):
		os.makedirs(workspace_dir, 448)

	target_raw_file = os.path.join(workspace_dir, "disk.img")

	try:
		# Open the raw intermediate storage link file descriptor
		raw_out_fd = open(target_raw_file, "wb")
	except (IOError, OSError) as e:
		sys.stderr.write("[!] ISO Pipeline Failure: Cannot create temporary disk.img swap map: " + str(e) + "\n")
		if os.path.exists(workspace_dir): shutil.rmtree(workspace_dir)
		return None

	# We return a custom Pipeline Wrapper Class mimicking Popen behaviors to the core engine
	class ISOPipelineWrapper(object):
		def __init__(self, out_fd, work_dir, final_iso, v_id, pub):
			self.stdin = out_fd
			self.work_dir = work_dir
			self.final_iso = final_iso
			self.target_raw = os.path.join(work_dir, "disk.img")
			self.v_id = v_id
			self.pub = pub
			self.returncode = 0

		def terminate(self):
			try: self.stdin.close()
			except Exception: pass
			if os.path.exists(self.work_dir):
				shutil.rmtree(self.work_dir, ignore_errors=True)

		def wait(self):
			# 1. Close the active input handle to ensure all blocks are flushed down to disk
			self.stdin.close()

			if not os.path.exists(self.target_raw) or os.getsize(self.target_raw) < 512:
				if os.path.exists(self.work_dir): shutil.rmtree(self.work_dir, ignore_errors=True)
				return 1

			# 2. Binary Evaluation Stage: Read Sector 0 to analyze partitietabellen structures
			is_bootable = False
			try:
				with open(self.target_raw, "rb") as rf:
					sector_0 = rf.read(512)
					if len(sector_0) == 512 and sector_0[510:512] == "\x55\xAA":
						# Scan the 4 partition table slots for an active 0x80 boot flag marker
						for i in range(4):
							slot_offset = 446 + (i * 16)
							if sector_0[slot_offset] == 0x80:
								is_bootable = True
								break
			except Exception:
				pass

			# 3. Compilation Phase: Construct native array arguments list for compiler binaries
			# Discover which compilation utility tool is available on the host node
			compiler_bin = "genisoimage"
			for binary in ["genisoimage", "xorriso", "mkisofs"]:
				if any(os.path.isfile(os.path.join(p, binary)) for p in os.environ.get("PATH", "").split(os.path.pathsep)):
					compiler_bin = binary
					break

			cmd_array = [compiler_bin, "-V", self.v_id, "-publisher", self.pub, "-o", self.final_iso]

			if is_bootable and compiler_bin in ["genisoimage", "mkisofs"]:
				# Append standard El Torito hard disk emulation variables onto the array
				# Copies the raw drive structure directly inside an embedded compliance segment
				cmd_array.extend(["-hard-disk-boot", "-b", "disk.img", "-c", "boot.catalog"])

			cmd_array.append(self.work_dir)

			try:
				# Compile the definitive Hybrid-ISO asset file descriptor layout block
				proc = subprocess.Popen(cmd_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				_, stderr = proc.communicate()
				self.returncode = proc.returncode

				if proc.returncode != 0:
					sys.stderr.write("[!] ISO Compilation Binary Error: " + stderr.strip() + "\n")

				# 4. Hybrid post-processing execution phase if applicable
				if is_bootable and proc.returncode == 0:
					if any(os.path.isfile(os.path.join(p, "isohybrid")) for p in os.environ.get("PATH", "").split(os.path.pathsep)):
						subprocess.call(["isohybrid", self.final_iso])
			except Exception as e:
				sys.stderr.write("[!] ISO Post-processing Compiler Abruptly Crashed: " + str(e) + "\n")
				self.returncode = 1
			finally:
				# Forensically purge all temporary data layers and workspaces from the host system
				shutil.rmtree(self.work_dir, ignore_errors=True)

			return self.returncode

	return ISOPipelineWrapper(raw_out_fd, workspace_dir, target_path, vol_id, publisher_str)
