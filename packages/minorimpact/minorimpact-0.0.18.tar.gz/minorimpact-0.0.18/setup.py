#!/usr/bin/env python3

import minorimpact
from setuptools import find_packages, setup

with open('./README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    author='Patrick Gillan',
    author_email = 'pgillan@minorimpact.com',
    build_requires=['psutil'],
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        ],
    description='Personal utility library',
    install_requires=['psutil'],
    license='GPLv3',
    long_description = readme,
    long_description_content_type = 'text/markdown',
    name='minorimpact',
    packages=find_packages(include=['minorimpact']),
    setup_requires=['psutil'],
    tests_require=[],
    url = "https://github.com/minorimpact/python-minorimpact",
    version=minorimpact.__version__,
)
