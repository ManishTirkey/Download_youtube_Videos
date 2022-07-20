import cx_Freeze
import sys
import os
base = None

if sys.platform == 'win32':
    base = "Win32GUI"

os.environ['TCL_LIBRARY'] = r"F:\INSTALLED\python\Python3.8\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"F:\INSTALLED\python\Python3.8\tcl\tk8.6"

executables = [cx_Freeze.Executable("youtube.py", base=base, icon="Youtube.ico")]


cx_Freeze.setup(
    name="YouTube Video Downloader",
    options={"build_exe": {"packages": ["tkinter","os"], "include_files": ["Youtube.ico",'tcl86t.dll','tk86t.dll']}},
    version="1.2",
    description="Tkinter Application to download youtube videos",
    executables=executables,
    )