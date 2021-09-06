from cx_Freeze import setup, Executable
import os
import sys
import mpl_toolkits

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

exe = [Executable("main.py", base=base)]

# os.environ['TCL_LIBRARY'] = r'C:\\Users\\dm\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tcl8.6'
# os.environ['TK_LIBRARY'] = r'C:\\Users\\dm\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tk8.6'

options = {
    'build_exe': {
        # 'includes': ['scipy.io', 'scipy.spatial.ckdtree'],
        # 'includes': ['mpl_toolkits'],
        # 'include_files': [r'C:\\Users\\dm\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\pyqt5_tools\\platforms\\qwindows.dll'],
        'packages': ['PyQt5.sip','pkg_resources._vendor', 'pandas', 'numpy', 'qimage2ndarray', 'matplotlib.backends.backend_qt5agg'],
        'excludes': ['PyQt6', 'PySide2'],
        # "include_files": [os.path.join(python_dir, "python3.dll"), os.path.join(python_dir, "vcruntime140.dll")],
        'include_files': ['widgets/', 'files/', 'form.ui', 'stylesheet.css'],
        'namespace_packages': ['mpl_toolkits']
    }
}

setup(name="CQFlex", version="1.0", description='',
      options=options, executables=exe)
