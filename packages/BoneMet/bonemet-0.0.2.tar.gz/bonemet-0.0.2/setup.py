import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="BoneMet",  # Replace with your project's name
    version="0.0.2",
    author="Jason S Jiang",
    author_email="jjiang15@umd.edu",
    description="Coming Soon!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/graeyyscale/BoneMet",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",  # List your project's dependencies here
        "numpy",
    ],
)