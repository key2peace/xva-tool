# ==============================================================================
#      XVA-TOOL PLUGIN - COMMAND: MOUNT ENGINE
#      Orchestrates VFS entry points and block device virtualization loops.
#
#      Developed and maintained by Alexander Maassen and Google's Gemini AI.
#      Licensed under the terms of the MIT License.
# ==============================================================================
# -*- coding: utf-8 -*-
"""
XVA-TOOL Plugin: Command - Forensic Mount Engine

This module orchestrates virtual filesystem entry points for uncompressed
XVA containers. It maps individual 1MB data blocks into a continuous read-only
virtual block device wrapper using loop devices or standalone FUSE structures.

Developer Specifications:
    - Entry Hook: Execute filesystem mount sequence onto a target path layout.
    - Integrity Layer: Enforces strict read-only parameters to block data mutation.
    - Platform Bounds: Integrates closely with system storage subsystems.

Exposed Variables:
    - pl (dict): System metadata tracking array containing module type,
		 classification name, and CLI help bindings.
"""

import os
import sys
import errno

# The Plugin Metadata Dictionary - Placed strictly below core imports
pl = {
	"name": "mount",
	"type": "commands",
	"help": "Mount an uncompressed XVA container dynamically as a read-only VFS block device."
}

# Track if optional python-fuse bindings are discoverable in the active environment
FUSE_AVAILABLE = False
try:
	import fuse
	fuse.fuse_python_api_version = (0, 2)
	FUSE_AVAILABLE = True
except ImportError:
	pass

def is_supported():
	"""
	Proactive Environment Check. Verifies if the host OS has the
	FUSE kernel module loaded and the python-fuse libraries present.
	"""
	return FUSE_AVAILABLE and os.path.exists("/dev/fuse")


def register_arguments(parser):
	"""Attaches FUSE-specific runtime attributes to the core parser."""
	group = parser.add_argument_group("FUSE Virtual Mount Options")
	group.add_argument("--mount-allow-other", action="store_true",
		help="Allow unprivileged local system users access to the virtual partition")


class XvaVirtualFileSystem(fuse.Fuse):
	"""
	FUSE Low-Level Translation Matrix. Maps OS virtual filesystem operations
	directly into O(1) mathematical seek structures inside the XVA tarball container.
	"""
	def __init__(self, *args, **kw):
		fuse.Fuse.__init__(self, *args, **kw)
		self.archive_path = None
		self.virtual_file_name = "disk.img"
		self.virtual_file_size = 100 * 1024 * 1024 * 1024 # Standard 100GB allocation default

	def getattr(self, path):
		"""Defines the virtual directory file tree entries and ownership attributes."""
		st = fuse.Stat()
		if path == '/':
			st.st_mode = fuse.S_IFDIR | 0755
			st.st_nlink = 2
		elif path == '/' + self.virtual_file_name:
			st.st_mode = fuse.S_IFREG | 0644
			st.st_nlink = 1
			st.st_size = self.virtual_file_size
		else:
			return -errno.ENOENT
		return st

	def readdir(self, path, offset):
		"""Returns the virtual disk.img inside the mountpoint directory structure."""
		yield fuse.Direntry('.')
		yield fuse.Direntry('..')
		yield fuse.Direntry(self.virtual_file_name)

	def open(self, path, flags):
		"""Enforces read-only transactional constraints on the virtual drive handle."""
		if path != '/' + self.virtual_file_name:
			return -errno.ENOENT
		accmode = flags & 3
		if accmode != os.O_RDONLY:
			return -errno.EACCES
		return 0

	def read(self, path, size, offset):
		"""
		The Core FUSE Intercept Loop. Translates random read offsets
		directly into precise block targets inside the XVA archive via f.seek().
		"""
		if path != '/' + self.virtual_file_name:
			return -errno.ENOENT

		# Mathematical fixed-grid alignment properties mapping variables
		chunk_size = 1024 * 1024
		tar_header_size = 512
		start_of_chunks_offset = 43008
		chunk_total_stride = tar_header_size + chunk_size

		# Determine which 1MB chunk cluster corresponds to the requested offset
		chunk_idx = offset // chunk_size
		byte_inside_chunk = offset % chunk_size

		# Calculate the precise absolute binary target location on the hardware array
		physical_seek_pos = start_of_chunks_offset + (chunk_idx * chunk_total_stride) + tar_header_size + byte_inside_chunk

		try:
			with open(self.archive_path, "rb") as f:
				f.seek(physical_seek_pos)
				return f.read(size)
		except Exception:
			return -errno.EIO


def execute(args):
	"""Main execution lifecycle entrypoint triggered by the xva-tool core mapper."""
	if not is_supported():
		sys.stderr.write("[!] FUSE Mount Interruption: Kernel bindings or python-fuse package missing.\n")
		sys.stderr.write("[*] Proactive Remedy: Run 'apt install python-fuse' or 'pip install fuse-python'.\n")
		sys.exit(1)

	if not hasattr(args, 'archive') or not hasattr(args, 'target'):
		sys.stderr.write("[!] Syntax Error: Usage requires 'xva-tool mount <source.xva> <target_dir>'.\n")
		sys.exit(1)

	print("Initializing high-speed FUSE virtual mapping abstraction loop...")
	print("Mounting virtual raw volume straight to: " + args.target)

	# Initialize and configure the operational FUSE server runtime daemon
	fs = XvaVirtualFileSystem()
	fs.archive_path = args.archive

	# Pass execution over to the native multi-threaded userspace filesystem mount loop
	fuse_args = [sys.argv[0], args.target, "-o", "ro"] # Enforce strict read-only compliance
	if hasattr(args, 'mount_allow_other') and args.mount_allow_other:
		fuse_args.extend(["-o", "allow_other"])

	try:
		fs.main(fuse_args)
		print("Success: FUSE instance safely dismantled and unmounted from system space.")
	except Exception as e:
		sys.stderr.write("[!] FUSE Filesystem execution failure encountered: " + str(e) + "\n")
		sys.exit(1)
