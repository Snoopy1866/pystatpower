import os
from dotenv import load_dotenv
from setuptools import setup, find_packages

load_dotenv()

author_email = os.getenv("SETUP_AUTHOR_EMAIL", "default@example.com")

setup(
    name="openpower",
    version="0.0.1-alpha",
    packages=find_packages(include=["openpower", "openpower.*"]),
    install_requires=["scipy==1.14.1"],
    author="Snoopy1866",
    author_email=author_email,
    description="A Power Analysis Toolkit for Python",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/OpenPowerX/OpenPower",
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
