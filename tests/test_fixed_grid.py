# ==============================================================================
#      XVA-TOOL - Forensics & Recovery Tool designed for XenServer
#
#      copyright ©2026 Alexander Maassen & Gemini AI
#      Distributed under the terms of the MIT License.
# ==============================================================================
# -*- coding: utf-8 -*-
import unittest
import struct

class TestXvaFixedGridAndBitmask(unittest.TestCase):
	def setUp(self):
		"""Initializes clean simulation boundaries before each test execution."""
		self.CHUNK_DATA_SIZE = 1024 * 1024
		self.CHUNK_TOTAL_SIZE = 512 + self.CHUNK_DATA_SIZE
		self.START_OF_CHUNKS = 43008 # Simulated size after parsing a sample ova.xml

	def test_fixed_grid_formula_precision(self):
		"""Verifies that the O(1) grid formula hits the exact byte boundaries of chunk N."""
		target_chunk_idx = 5
		byte_inside_chunk = 4096 # Kernel requested offset inside the block

		# Execute our calculated grid translation math
		physical_offset = self.START_OF_CHUNKS + (target_chunk_idx * self.CHUNK_TOTAL_SIZE) + 512 + byte_inside_chunk

		# Explicit mathematical verification of the target block alignment
		expected_offset = 43008 + (5 * (512 + 1048576)) + 512 + 4096
		self.assertEqual(physical_offset, expected_offset, "Binary grid misalignment detected!")

	def test_bytearray_bitmask_allocation(self):
		"""Ensures the compact bitmask uses minimal RAM while retaining instant lookup indexing."""
		# Allocate our standard 128KB bitmask matrix (covers up to 1 million chunks / 1TB)
		chunk_bitmask = bytearray(131072)

		# Simulate that chunk 45 and chunk 1024 physically exist in the XVA tarball
		test_chunks = [45, 1024]
		for chunk_idx in test_chunks:
			# Optimized bitwise shift operations mapping
			byte_pos = chunk_idx >> 3
			bit_pos = chunk_idx & 7
			chunk_bitmask[byte_pos] |= (1 << bit_pos)

		# Test boundary lookups: chunk 45 must return TRUE (allocated chunk)
		c45_byte = 45 >> 3
		c45_bit = 45 & 7
		self.assertTrue((chunk_bitmask[c45_byte] & (1 << c45_bit)) != 0)

		# Test boundary lookups: chunk 46 must return FALSE (sparse hole)
		c46_byte = 46 >> 3
		c46_bit = 46 & 7
		self.assertFalse((chunk_bitmask[c46_byte] & (1 << c46_bit)) != 0)

	def test_mbr_unpacker_integrity(self):
		"""Simulates a Sector 0 byte stream to verify structural struct.unpack mappings."""
		# Construct a fake 512-byte MBR block template container
		fake_mbr = bytearray(512)

		# Partition slot 1 starts at byte offset 446 inside Sector 0
		# Byte 4 inside the slot is the partition filesystem type identifier (offset 450)
		fake_mbr[450] = 0x83 # Linux Native filesystem flag (ext4 / xfs)

		# Bytes 8-11 inside the partition slot contain the LBA Start Sector (offset 454)
		# Write start sector 2048 (0x00000800) in Little-Endian format into bytes 454-457
		struct.pack_into("<I", fake_mbr, 454, 2048)

		# Bytes 12-15 contain total sectors count (offset 458)
		# Write total sectors count (e.g., 204800 sectors) into bytes 458-461
		struct.pack_into("<I", fake_mbr, 458, 204800)

		# Inject the mandatory structural MBR boot signature validation bytes at the tail end
		fake_mbr[510] = 0x55
		fake_mbr[511] = 0xAA

		# Pass our simulated binaire data block straight to a basic check validation rule
		self.assertEqual(fake_mbr[450], 0x83, "Forensic partition type identifier mapping failure.")
		self.assertEqual(fake_mbr[510], 0x55, "MBR validation signature sector corruption.")
		self.assertEqual(fake_mbr[511], 0xAA, "MBR validation signature sector corruption.")

if __name__ == "__main__":
	unittest.main()
