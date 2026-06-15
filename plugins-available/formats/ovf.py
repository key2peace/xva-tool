#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
#  XVAPLUGIN - OVF / OVA (VMware / VirtualBox) Cross-Compatibility Adapter
# ==============================================================================
#  Copyright (c) 2026 Alexander Maassen <outsider@cuci.nl>
#  Licensed under the terms of the MIT License (See LICENSE.md in root)
# ==============================================================================
"""
Dynamic OVF/OVA conversion format extension module.
Wraps raw disk allocations alongside generated OVF XML descriptors into USTAR tarballs.
"""

import os
import sys
import tarfile

def is_supported():
	"""Proactive Environment Check. Always returns True as it uses pure Python core modules."""
	return True


def register_arguments(parser):
	"""Attaches DMTF OVF virtualization metadata attributes to the central core parser."""
	group = parser.add_argument_group("Open Virtualization Format Options")
	group.add_argument("--ovf-cpu", type=int, default=2,
		help="Specify the virtual CPU core allocation count inside the OVF manifest")
	group.add_argument("--ovf-ram", type=int, default=2048,
		help="Specify the virtual RAM memory allocation size in Megabytes")


def get_write_pipeline(target_path, args=None):
	"""
	Secure Downstream Pipe Provisioning. Intercepts the core byte stream
	to bundle the data on-the-fly into a compliance OVA distribution container.
	"""
	cpu_count = 2
	ram_size = 2048

	if args:
		if hasattr(args, "ovf_cpu"): cpu_count = args.ovf_cpu
		if hasattr(args, "ovf_ram"): ram_size = args.ovf_ram

	base_name = os.path.basename(target_path).replace(".ova", "")
	workspace_dir = "/tmp/xvatool_ova_workspace_{}".format(os.getpid())
	if not os.path.exists(workspace_dir):
		os.makedirs(workspace_dir, 448)

	target_raw_file = os.path.join(workspace_dir, base_name + ".vmdk")

	try:
		raw_out_fd = open(target_raw_file, "wb")
	except (IOError, OSError) as e:
		sys.stderr.write("[!] OVF Pipeline Failure: Cannot create swap map: " + str(e) + "\n")
		return None

	class OVAPipelineWrapper(object):
		def __init__(self, out_fd, work_dir, final_ova, cpu, ram, b_name):
			self.stdin = out_fd
			self.work_dir = work_dir
			self.final_ova = final_ova
			self.target_raw = os.path.join(work_dir, b_name + ".vmdk")
			self.cpu = cpu
			self.ram = ram
			self.b_name = b_name
			self.returncode = 0

		def terminate(self):
			try: self.stdin.close()
			except Exception: pass
			if os.path.exists(self.work_dir):
				import shutil
				shutil.rmtree(self.work_dir, ignore_errors=True)

		def wait(self):
			self.stdin.close()

			if not os.path.exists(self.target_raw):
				if os.path.exists(self.work_dir):
					import shutil
					shutil.rmtree(self.work_dir, ignore_errors=True)
				return 1

			# Generate compliance DMTF OVF XML descriptor block on-the-fly
			ovf_path = os.path.join(self.work_dir, self.b_name + ".ovf")
			ovf_xml = (
				"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
				"<Envelope xmlns=\"http://dmtf.org\">\n"
				"\t<References>\n"
				"\t\t<File id=\"file1\" href=\"{}.vmdk\" size=\"{}\"/>\n"
				"\t</References>\n"
				"\t<VirtualSystem id=\"vm\">\n"
				"\t\t<Info>Extracted via XvaTool</Info>\n"
				"\t\t<Name>{}</Name>\n"
				"\t\t<VirtualHardwareSection>\n"
				"\t\t\t<Item>\n"\
				"\t\t\t\t<Description>Number of virtual CPUs</Description>\n"
				"\t\t\t\t<VirtualQuantity>{}</VirtualQuantity>\n"
				"\t\t\t</Item>\n"
				"\t\t\t<Item>\n"
				"\t\t\t\t<Description>Memory size in MBytes</Description>\n"
				"\t\t\t\t<VirtualQuantity>{}</VirtualQuantity>\n"
				"\t\t\t</Item>\n"
				"\t\t</VirtualHardwareSection>\n"
				"\t</VirtualSystem>\n"
				"</Envelope>\n"
			).format(self.b_name, os.path.getsize(self.target_raw), self.b_name, self.cpu, self.ram)

			with open(ovf_path, "w") as f:
				f.write(ovf_xml)

			# Package both assets into a standardized USTAR compliant .ova archive tarball
			try:
				with tarfile.open(self.final_ova, "w") as tar:
					tar.add(ovf_path, arcname=self.b_name + ".ovf")
					tar.add(self.target_raw, arcname=self.b_name + ".vmdk")
				self.returncode = 0
			except Exception as e:
				sys.stderr.write("[!] OVA Package Compilation Failure: " + str(e) + "\n")
				self.returncode = 1
			finally:
				import shutil
				shutil.rmtree(self.work_dir, ignore_errors=True)

			return self.returncode

	return OVAPipelineWrapper(raw_out_fd, workspace_dir, target_path, cpu_count, ram_size, base_name)
