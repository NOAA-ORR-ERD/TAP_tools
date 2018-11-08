from __future__ import print_function, unicode_literals, division

import os
import glob
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def get_version():
    """
    get version from __init__.py
    """
    with open(os.path.join("tap_tools", "__init__.py")) as initfile:
        for line in initfile:
            line = line.strip()
            if line.startswith("__version__"):
                version = line.split("=")[1].strip(' "')
                return version

print("version is:", get_version())

setuptools.setup(
    name="tap_tools",
    version=get_version(),
    author="NOAA Emergency Response Division",
    author_email="chris.barker@noaa.gov",
    description="Tools for developing datasets for the Trajectory Analysis Planner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NOAA-ORR-ERD/TAP_tools",
    packages=setuptools.find_packages(),
    scripts=glob.glob('tap_tools/scripts/*.py'),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)