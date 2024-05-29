import sys
import os
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["pywinauto", "tkinter", "Openness", "sqlite3"],
    "include_files": [
        "Openness.py",
        os.path.join("repositories", "Connection.py"),
        os.path.join("repositories", "MlfbManagement.py"),
        os.path.join("repositories", "UserConfig.py"),
        os.path.join("repositories", "ValidateDb.py"),
        os.path.join("repositories", "Openness.db"),
        os.path.join(sys.base_prefix, 'DLLs', 'sqlite3.dll')
    ]
}

if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="RPA Tia Openness",
    version="0.1",
    description="Interface for automated creation of TIA Portal projects using Openness API",
    options={"build_exe": build_exe_options},
    executables=[Executable("Screen.py", base=base, target_name="RPA_Tia_Openness")]
)