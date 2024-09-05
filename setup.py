import os
from setuptools import setup, find_packages


author_email = os.getenv("SETUP_AUTHOR_EMAIL", "default@example.com")

setup(
    name="pystatpower",
    version="0.0.1-a2",
    packages=find_packages(include=["pystatpower", "pystatpower.*"]),
    install_requires=["scipy==1.14.1"],
    author="Snoopy1866",
    author_email=author_email,
    description="A Power Analysis Toolkit for Python",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PyStatPower/PyStatPower",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.12",
)
