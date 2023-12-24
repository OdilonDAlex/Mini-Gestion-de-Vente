import os
import sys
from cx_Freeze import setup, Executable

files = ["icon.ico", "API"]

target = Executable(
    script="app.py",
    base="Win32GUI",
    icon="icon.ico"
)

setup(
    name= "BuyProduct",
    version= "0.1",
    descprition= "Desktop application for buying something",
    author= "Nomenjanahary Odilon D'Alex",
    options= {'build_exe' : {'include_files' : files}},
    executables= [target]
)