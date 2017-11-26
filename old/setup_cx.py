import sys
import os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = "C:\\Users\\cy804\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\cy804\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"

build_exe_options = {"packages" : ["os"], "excludes" : ["tkiner"]}

base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

setup(
    name = "convert2Excel",
    version = "1.0",
    description = "Convert txt file into Excel.",
    options = {"build_exe": build_exe_options},
    executables = [Executable("convert2Excel2.py", base=base)]
)
