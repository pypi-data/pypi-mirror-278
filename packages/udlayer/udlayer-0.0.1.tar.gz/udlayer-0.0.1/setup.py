import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='udlayer',
    version='0.0.1',
    packages=setuptools.find_packages(),
    url='https://github.com/SJTU-CILAB/udl',
    license='MIT',
    author='Yiheng Wang',
    author_email='yhwang0828@sjtu.edu.cn',
    description='A suite of standardized data structure and pipeline for city data engineerin',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['networkx', 'pandas', 'geopandas', 'shapely', 'rasterio', 'pyproj', 'tqdm', 'rasterio']
)
