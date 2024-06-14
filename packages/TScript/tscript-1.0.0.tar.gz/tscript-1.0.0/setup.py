from setup import *
from setuptools import *
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
name="TScript",
long_description=long_description,
long_description_content_type='text/markdown',
author="SneakyFrameworkCreator",
version="1.0.0",
classifiers=[
    "Development Status :: 1 - Planning",
    "Environment :: Other Environment",
    "License :: OSI Approved :: MIT License",
    "Operating System :: Microsoft :: Windows :: Windows 11",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: Implementation",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
]
)