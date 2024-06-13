'''
Author: Devin
Date: 2024-06-13 11:49:52
LastEditors: Devin
LastEditTime: 2024-06-13 15:47:47
Description: 

Copyright (c) 2024 by Devin, All Rights Reserved. 
'''
from setuptools import setup, find_packages

setup(
    name='devin_colors',
    version='0.1.0',
    author='Devin Long',
    author_email='long.sc@qq.com',
    description='colors map for python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Devin-Long-7/esil',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,# 允许包含在 MANIFEST.in 文件中指定的所有文件。
    package_data={
        'devin_colors': ['color_maps/*.rgb'],
        'devin_colors': ['color_maps/*.pkl'],  # 包含特定包中的 .pkl 文件
    },
    python_requires='>=3.6',
    #     # rich >= 9.13.0
    # install_requires =
    # numpy
    # matplotlib
    # ,
)