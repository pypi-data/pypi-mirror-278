from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="pbsc",
    packages=["pbsc"],
    entry_points={
        "console_scripts": ["pbsc=pbsc.__init__:main"],
    },
    version="0.1.0",
    description="High-Level API Client for Public Bike System Company",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Daniel J. Dufour",
    author_email="daniel.j.dufour@gmail.com",
    url="https://github.com/officeofperformancemanagement/pbsc",
    download_url="https://github.com/officeofperformancemanagement/pbsc/tarball/download",
    keywords=["data", "python"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests"],
)
