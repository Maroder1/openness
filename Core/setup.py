import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["pywinauto", "tkinter", "Openness"], "include_files": ["Openness.py"]}

# GUI applications require a different base on Windows (the default is for a console application).
base = None
if(sys.platform == "win32"):
    base = "Win32GUI"
    setup(
        name="RPA Tia Openness",
        version="0.1",
        description="Interface for automated creation of TIA Portal projects using Openness API",
        options={"build_exe": build_exe_options},
        executables=[Executable("Screen.py", base=base, target_name="RPA_Tia_Openness")]
    )
