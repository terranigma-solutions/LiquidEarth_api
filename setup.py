﻿from os import path

from setuptools import setup, find_packages


def read_requirements(file_name):
    requirements = []
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            # Strip whitespace and ignore comments
            line = line.strip()
            if line.startswith("#") or not line:
                continue

            # Handle -r directive
            if line.startswith("-r "):
                referenced_file = line.split()[1]  # Extract the file name
                requirements.extend(read_requirements(referenced_file))  # Recursively read referenced file
            else:
                requirements.append(line)
    return requirements


setup(
    name='liquid_earth_api',
    packages=find_packages(exclude=('test', 'docs', 'examples')),
    url='',
    license='EUPL-v1.2',
    author='Miguel de la Varga',
    author_email='miguel@terranigma-solutions.com',
    description='Python API to interact with Liquid Earth',
    install_requires=read_requirements("requirements.txt"),
    setup_requires=['setuptools_scm'],
    use_scm_version={
            "root"            : ".",
            "relative_to"     : __file__,
            "write_to"        : path.join("liquid_earth_api", "_version.py"),
            "fallback_version": "0.0.1"
    },
)
