# from distutils.core import setup

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
# from codecs import open
from os import path

# workaround from https://github.com/pypa/setuptools/issues/308 to avoid "normalizing" version "2018.01.09" to "2018.1.9":
# import pkg_resources
# pkg_resources.extern.packaging.version.Version = pkg_resources.SetuptoolsLegacyVersion
# 2019-10-02: this is causing "AttributeError: module 'pkg_resources' has no attribute 'SetuptoolsLegacyVersion'"
#             -> this trick is no longer working

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
#with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#    long_description = f.read()

setup(
    name="memacs",
    version="2019.11.05.1",
    description="Visualize your (digital) life in Emacs Org mode by converting data to Org mode format",
    author="Karl Voit",
    author_email="tools@Karl-Voit.at",
    url="https://github.com/novoid/memacs",
    download_url="https://github.com/novoid/memacs/zipball/master",
    keywords=["quantified self", "emacs", "org-mode", "org mode"],
    packages=find_packages(), # Required
    #package_data={},
    #install_requires=[FIXXME],  # 2019-10-02 Karl: unsure, if it is feasible to add all requirements since there are lots of independent modules ...
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        ],
    #entry_points={  # Optional   # 2019-10-02 Karl: unsure, if it is feasible to add all entry_points since there are lots of independent modules ...
    #    'console_scripts': [
    #       FIXXME
    #    ],
    #},
#    long_description=long_description, # Optional
    long_description="""This Python framework converts data from various sources to Org mode format
which may then included in Org mode agenda (calendar). This way, you get a 360-degree-view of your
digital life.

Each Memacs module converts a different input format into Org mode files.

- Target group: users of Emacs Org mode who are able to use command line tools
- Hosted and documented on github: https://github.com/novoid/memacs
"""
)
