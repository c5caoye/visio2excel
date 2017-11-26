import sys
import os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = r"C:\Users\cy804\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\cy804\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6"

include_files = [r"C:\Users\cy804\AppData\Local\Programs\Python\Python36-32\DLLs\tcl86t.dll",
    r"C:\Users\cy804\AppData\Local\Programs\Python\Python36-32\DLLs\tk86t.dll"]

build_exe_options = {"packages" : ["os"], "includes" : ['idna.idnadata', 'numpy.core._methods', 'numpy.lib.format', 'cymem',
    'murmurhash', 'cytoolz._signatures', 'spacy.lemmatizer', 'spacy._ml', 'importlib',
    'spacy.tokens.underscore', 'spacy.tokens.printers', 'thinc.neural._classes.difference']}

base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

setup(
    name = "convert2Excel2",
    version = "1.0",
    description = "Convert txt file into Excel.",
    options = {"build_exe": build_exe_options},
    executables = [Executable("convert2Excel2.py", base=base)]
)
