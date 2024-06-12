#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: luojiaxu
# Mail: luojiaxu@cibr.ac.cn
# Created Time:  2024-5-9 
#############################################

from setuptools import setup, find_packages            

setup(
    name = "MGFEA",      
    version = "1.0.2",  
    keywords = ["pip", "MGFEA"],
    description = "A package for single cell flux prediction",
    long_description = "A deep learning framework for metabolic flux prediction based on single cell transcriptome",
    license = "MIT Licence",

    url = "https://github.com/Sunwenzhilab/MGFEA",     
    author = "luojiaxu",
    author_email = "luojiaxu@cibr.ac.cn",

    packages = find_packages(['MGFEA']),
    include_package_data = True,
    platforms = "any",
    install_requires = ['torch','scipy','scanpy','torch_geometric']          
)
