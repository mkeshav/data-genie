from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="data-genie-mkeshav",
    version="0.2.6",
    author="Keshav Murthy",
    author_email="mkeshav@gmail.com",
    description="A small genie to generate test data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/mkeshav/data_genie",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'jinja2',
    ],
)