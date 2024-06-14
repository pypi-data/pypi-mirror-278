import setuptools
from setuptools import setup

# read the contents of README file
from os import path
from io import open  # for Python 2 and 3 compatibility

# this_directory = path.abspath(path.dirname(__file__))


with open("README.md", "r") as fh:
    long_description = fh.read()

# read the contents of requirements.txt
# with open(path.join(this_directory, 'requirements.txt'),
#           encoding='utf-8') as f:
#     requirements = f.read().splitlines()

setup(
    name="udlayer",
    version="0.0.3",
    packages=setuptools.find_packages(),
    url="https://github.com/SJTU-CILAB/udl",
    license="MIT",
    author="Yiheng Wang",
    author_email="yhwang0828@sjtu.edu.cn",
    description="A suite of standardized data structure and pipeline for city data engineerin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "numpy==1.24.4",
        "pandas==2.0.3",
        "networkx==3.1",
        "pyproj==3.6.1",
        "pyshp==2.3.1",
        "shapely==2.0.2",
        "GDAL==3.8.1",
        "fiona==1.9.5",
        "geopandas==0.14.1",
        "rasterio==1.3.9",
        "scikit-learn==1.3.0",
        "tqdm==4.65.0",
    ],
)
