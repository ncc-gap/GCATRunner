#!/usr/bin/env python

from setuptools import setup, find_packages
from scripts.gcat_runner import __version__

setup(
    name = 'gcat_runner',
    version = __version__,
    description = 'Python tools for running gcat workflow for cancer genome and transcriptome sequencing analysis',
    keywords = 'cloud bioinformatics',
    author = 'Kenichi Chiba, Ai Okada and Yuichi Shiraishi',
    author_email = 'genomon.devel@gmail.com',
    url = 'https://github.com/ncc-gap/GCATRunner.git',
    license = 'GPLv3',
    
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
    
    package_dir = {'': 'scripts'},
    packages = find_packages("scripts"),
    package_data = {'gcat_runner': ['*/data/*']},
    
    scripts = ['gcat_runner'],
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'pyyaml', 'drmaa',
    ],
    test_suite = 'tests'
)
