# -*- coding: utf-8 -*-
import os.path

from setuptools import setup

packages = ["dciagent", "dciagent.agents", "dciagent.core", "dciagent.core.agent"]

package_data = {"": ["*"]}

extras_require = {':python_version < "3.7"': ["importlib-metadata>=1.0,<2.0"]}

entry_points = {"console_scripts": ["dci-agent-ctl = dciagent.core.cli:main"]}

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    long_desc = readme.read()

setup_kwargs = {
    "name": "python-dciagent",
    "version": "0.2.0",
    "description": "A python framework for DCI agents",
    "long_description": long_desc,
    "author": "Distributed CI team",
    "author_email": "distributed-ci@redhat.com",
    "maintainer": None,
    "maintainer_email": None,
    "url": "https://github.com/redhat-cip/python-dciagent",
    "license": "Apache-2.0",
    "classifiers": [
        "Development Status :: 3 - Alpha"
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.11",
    ],
    "packages": packages,
    "package_data": package_data,
    "extras_require": extras_require,
    "entry_points": entry_points,
    "python_requires": ">=3.6.0,<4.0.0",
}


setup(**setup_kwargs)
