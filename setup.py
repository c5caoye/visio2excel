from distutils.core import setup
import py2exe

options = { "py2exe": {
				'bundle_files': 1, 
				'compressed': True,
                'packages': ["xlsxwriter"]
          }}
setup(console=['convert2Excel.py'], options=options, windows = [{'script': 'single.py'}], zipfile = None)
