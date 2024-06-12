
'''
File to set up the cjfx package

Author  : Celray James CHAWANDA
Email   : celray.chawanda@outlook.com
Licence : All rights Reserved
Repo    : https://github.com/celray

Date    : 2023-07-19
'''

# imports
from setuptools import setup, find_packages
import os

# Read README file
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    long_description = readme.read()

setup(
    name="cjfx",
    version="0.0.2",
    description="A module for common functions optimised for data scientists that need to code repeatitive tasks fast",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Celray James CHAWANDA",
    author_email="celray@chawanda.com",
    url='https://github.com/celray/cjfx',
    packages=find_packages(),
    install_requires=[
        'pytube',
        'geopandas',
        'pytube',
        'geopandas',
        'matplotlib',
        'numpy',
        'pandas',
        'psycopg2-binary',
        'requests',
        'rtree',
        'seaborn',
        'xarray',
        'xlsxwriter',
        'Pillow',
        'pySmartDL',
        'docxcompose',
        # 'GDAL',
        'python-docx',
        'tqdm',
        'wget',
        'rasterio',
        'openpyxl',
        'pyodbc',
        'SQLAlchemy',
        'pydub',
        'shapely',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)