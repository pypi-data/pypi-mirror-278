#!/usr/bin/env python

import io
import os
from codecs import open
from setuptools import setup

current_dir = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(current_dir, "rapidapi_axisdirect", "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), about)

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    download_url=about["__download_url__"],
    license=about["__license__"],
    packages=["rapidapi_axisdirect"],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=[
        "requests>=2.32.3",
        "pycryptodome>=3.20.0",
    ],
    
)