from distutils.core import setup
import py2exe

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    console=['main.py'],
    zipfile = None
)
# run "setup.py py2exe" to make exe file
