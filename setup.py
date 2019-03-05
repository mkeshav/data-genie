import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data-genie-mkeshav",
    version="0.0.8",
    author="Keshav Murthy",
    author_email="mkeshav@gmail.com",
    description="A small genie to generate test data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/mkeshav/data_genie",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'PyMonad',
        'jinja2',
    ],
)