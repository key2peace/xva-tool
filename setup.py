from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name="xva-tool",
	version="1.0.0",
	author="Alexander Maassen",
	author_email="outsider@cuci.nl",
	description="Advanced Zero-Copy Streaming Architecture Utility for Citrix XenServer XVA/OVA Images",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com",
	
	# Transports the main script straight into the executable PATH of the OS
	scripts=["xva-tool", "xvapkg"],
	
	# Maps system man pages directly into the standard Unix layout nodes
	data_files=[('share/man/man1', ['xva-tool.1'])],
	
	packages=find_packages(),
	include_package_data=True,
	
	# Legacy enterprise environment standard boundary constraints
	python_requires=">=2.7, <3.0",
	install_requires=[],
	
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Environment :: Console :: Curses",
		"Intended Audience :: System Administrators",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX :: Linux",
		"Programming Language :: Python :: 2.7",
		"Topic :: System :: Systems Administration",
		"Topic :: System :: Recovery Tools",
	],
)
