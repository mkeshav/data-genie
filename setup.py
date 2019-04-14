from setuptools import setup, find_packages
from genie_pkg import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = fh.readlines()

setup(
    name="data-genie-mkeshav",
    version=,
    author="Keshav Murthy",
    author_email="mkeshav@gmail.com",
    description="A small genie to generate test data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mkeshav/data-genie.git",
    packages=find_packages(include=('genie_pkg',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires
)