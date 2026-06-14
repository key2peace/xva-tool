#!/usr/bin/python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
	name="xva-tool",
	version="1.0.0",
	author="Alexander Maassen",
	author_email="outsider@cuci.nl",
	description="Enterprise XVA Zero-Copy Streaming Architecture Utility",
	url="https://github.com",
	packages=find_packages(),
	scripts=['xva-tool', 'xvapkg'],
	classifiers=[
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX :: Linux",
	],
	python_requires='>=2.7',
)
