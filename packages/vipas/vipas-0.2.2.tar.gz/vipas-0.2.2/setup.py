# coding: utf-8

"""
  All rights reserved. This program and the accompanying materials
  are made available under the terms of a proprietary license which prohibits
  redistribution and use in any form, without the express prior written consent
  of Vipas.AI.
  
  This code is proprietary to Vipas.AI and is protected by copyright and
  other intellectual property laws. You may not modify, reproduce, perform,
  display, create derivative works from, repurpose, or distribute this code or any portion of it
  without the express prior written permission of Vipas.AI.
  
  For more information, contact Vipas.AI at legal@vipas.ai

"""  # noqa: E501


from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "vipas"
VERSION = "0.2.2"
PYTHON_REQUIRES = ">=3.7"
REQUIRES = [
    "urllib3",
    "pydantic",
    "typing-extensions",
    "ratelimit",
    "pybreaker",
    "streamlit",
    "httpx"
]

setup(
    name=NAME,
    version=VERSION,
    description="Python SDK for Vipas AI Platform",
    author="Vipas Team",
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True
)
