from setuptools import setup, find_packages
import pathlib

# The directory containing this file
file = pathlib.Path(__file__).parent

# The text of the README file
README = (file / "README.md").read_text()

setup(
    name = 'python-csv-demjson3',
    packages = ['pcsv'],
    version = "0.0.16",
    description = 'Python tools for manipulating csv files. This package resolves demjson/setuptools issue with original python-csv',
    long_description=README,
    long_description_content_type="text/markdown",
    author = "Jason Trigg",
    author_email = "jasontrigg0@gmail.com",
    url = "https://github.com/jasontrigg0/python-csv",
    download_url = 'https://github.com/jasontrigg0/python-csv/tarball/0.0.13',
    scripts=[
        "pcsv/pcsv",
        "pcsv/pagg",
        "pcsv/pgraph",
        "pcsv/pjoin",
        "pcsv/plook",
        "pcsv/psort",
        "pcsv/pset",
        "pcsv/ptable",
        "pcsv/pindent",
        "pcsv/pconcat",
        "pcsv/ptr",
        "pcsv/pcat",
        "pcsv/any2csv"
    ],
    install_requires=[
        "argparse",
        "numpy",
        "pandas",
        "matplotlib",
        "xlrd",
        "xmltodict",
        "demjson3",
        "leven",
        "jtutils"
    ],
    keywords = [],
    classifiers = [],
)
