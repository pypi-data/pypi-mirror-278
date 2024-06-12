
import os
import sys
import urllib
from collections import defaultdict
import ctypes
import base64
import datetime
import gzip
import math
import string
import multiprocessing
import pickle
import platform
import random
import shutil
import sqlite3
import subprocess
import sys
import time
from io import StringIO
import warnings
import xml.etree.ElementTree as ET
import zipfile
from functools import partial
from glob import glob
from itertools import product
from shutil import copyfile, move, rmtree
from sqlite3.dbapi2 import DatabaseError
from pytube import YouTube, Playlist
import geopandas
import matplotlib.pyplot as plt
import numpy
import pandas
import psycopg2
import requests
import rtree
import seaborn
import xarray
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
from PIL import Image
from pySmartDL import SmartDL
from tqdm import tqdm

try:
    from osgeo import gdal, gdalconst, ogr
except ImportError:
    print("! Error importing gdal. cjfx will try to install it on your system. \nIf it doesn't work, please install it manually.")

    if platform.system() == "Windows":
    
        python_version_major = sys.version_info.major
        python_version_minor = sys.version_info.minor

        if python_version_major == 3 and python_version_minor == 7:
            os.system("pip install https://celray.chawanda.com/assets/downloads/GDAL-3.4.2-cp37-cp37m-win_amd64.whl")
        elif python_version_major == 3 and python_version_minor == 8:
            os.system("pip install https://celray.chawanda.com/assets/downloads/GDAL-3.4.3-cp38-cp38-win_amd64.whl")
        elif python_version_major == 3 and python_version_minor == 9:
            os.system("pip install https://celray.chawanda.com/assets/downloads/GDAL-3.4.3-cp39-cp39-win_amd64.whl")
        elif python_version_major == 3 and python_version_minor == 10:
            os.system("pip install https://celray.chawanda.com/assets/downloads/GDAL-3.4.3-cp310-cp310-win_amd64.whl")
        elif python_version_major == 3 and python_version_minor == 11:
            os.system("pip install https://celray.chawanda.com/assets/downloads/GDAL-3.4.3-cp311-cp311-win_amd64.whl")
        elif python_version_major == 3 and python_version_minor == 12:
            os.system("pip install https://celray.chawanda.com/assets/downloads/GDAL-3.8.4-cp312-cp312-win_amd64.whl")
        else:
            os.system("pip install gdal")

        from osgeo import gdal, gdalconst, ogr
            
    elif platform.system() == "Linux":
        try:
            os.system("pip install gdal --break-system-packages -y")
            from osgeo import gdal, gdalconst, ogr
        except:
            print("! Error installing gdal. Please install it manually.")

import wget
import rasterio
import openpyxl
from docx import Document
from docx.shared import Inches, Cm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import pyodbc
from sqlalchemy import MetaData, Table, create_engine, func, select
from pydub import AudioSegment
from shapely.geometry import Point, Polygon
from shapely import wkt

from .excel import excel
from .word import word_document as wordDocument
from .mssql_connection import mssql_connection as mssqlConnection
from .sqlite_connection import sqlite_connection as sqliteConnection

from .cjfx import (
        this_dir,
        copy_projection,
        set_tif_nodata,
        clip_features,
        assign_default_projection,
        plot,
        show,
        copy_file,
        copy_directory_tree,
        remove_header_duplicates,
        get_swat_timeseries,
        clip_raster,
        points_to_geodataframe,
        convert_webm_to_mp3,
        download_video_youtube,
        get_relative_path,
        install_package,
        get_usgs_timeseries,
        decode_64,
        wait,
        ignore_warnings,
        get_raster_value_for_coords,
        rasterise_shape,
        extract_timeseries_from_netcdf,
        rand_apha_num,
        make_plot,
        goto_dir,
        smart_copy,
        print_dict,
        transparent_image,
        get_file_size,
        cd,
        slope_intercept,
        distance,
        merge_documents,
        resize_image,
        download_file,
        download_file2,
        xml_children_attributes,
        python_variable,
        get_nse,
        get_pbias,
        report,
        print_list,
        disp,
        create_path,
        flow_duration_curve,
        delete_path,
        is_file,
        resample_ts_df,
        raster_statistics,
        empty_line,
        hide_folder,
        time_stamp,
        copy_folder,
        delete_file,
        run_swat_plus,
        open_file_in_code,
        format_timedelta,
        show_progress,
        confirm,
        open_tif_as_array,
        save_array_as_image,
        create_icon,
        unzip_file,
        single_spaces,
        view,
        quit,
        insert_newlines,
        write_to,
        exists,
        gdal_datatypes,
        resample_raster,
        create_polygon_geodataframe,
        reproject_raster,
        set_nodata,
        get_extents,
        file_name,
        read_from,
        error,
        strip_characters,
        list_files,
        list_all_files,
        list_folders,
    )
