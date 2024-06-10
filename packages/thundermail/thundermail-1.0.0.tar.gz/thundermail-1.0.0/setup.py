#!/usr/bin/env python

from setuptools import find_packages, setup

from version import get_version

install_requires = open("requirements.txt").readlines()

setup(
    name="thundermail",
    version=get_version(),
    description="Thundermail Python SDK",
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    author="shubhojit-mitra-dev",
    author_email="mitrashubhojit2005@gmail.com",
    url="https://github.com/shubhojit-mitra-dev/thundermail-python-sdk/",
    python_requires=">=3.7",
    keywords=["email","email platform"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=find_packages(),
)