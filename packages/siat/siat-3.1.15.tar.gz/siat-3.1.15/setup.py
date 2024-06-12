# -*- coding: utf-8 -*-
"""
@author: WANG Dehong (Peter), IBS BFSU
"""

#from __future__ import print_function
from setuptools import setup, find_packages
#import sys

setup(
    name="siat",
    version="3.1.15",
    #author="Prof. WANG Dehong, Business School, BFSU (北京外国语大学 国际商学院 王德宏)",
    author="Prof. WANG Dehong, International Business School, Beijing Foreign Studies University",
    author_email="wdehong2000@163.com",
    description="Securities Investment Analysis Tools (siat)",
    url = "https://pypi.org/project/siat/",
    long_description="""
    Security Investment Analysis Toolkit (siat) is designed to use for making case studies in learning security investment, 
    where cases can be replayed, updated and re-created in different securities, 
    different time lines and different measurements. 
    The plug-in is only licensed for teaching and learning purposes, not for commercial use. 
    The author is not responsible for any results of applying this plug-in in real 
    investment activities.
    """,
    license="Copyright (C) WANG Dehong, 2024. For educational purpose only!",
    packages = find_packages(),
    install_requires=[
        'pandas_datareader',
        'yfinance',
        #'pandas_alive','tqdm',
        'plotly_express',
        #'akshare==1.3.95',#为与urllib3兼容
        #'akshare==1.4.57',#为其他兼容考虑
        #'akshare==1.10.3',
        'akshare',
        #'urllib3==1.25.11',#为其他兼容考虑
        'urllib3',
        #'urllib3',
        'mplfinance',
        'statsmodels',
        'yahoo_earnings_calendar',
        #'yahooquery==2.2.14',#为其他兼容考虑
        'yahooquery',
        'pypinyin',
        'seaborn',
        'numpy',
        'scipy',
        #'pandas==1.5.3',#为其他兼容考虑
        'pandas',
        'scikit-learn',
        'baostock',
        'pyproject.toml',
        #'ta-lib',
        'pathlib','ruamel-yaml','prettytable','graphviz','luddite',
        'pendulum',
    ],            
    #zip_sage=False,
    include_package_data=True, # 打包包含静态文件标识
) 