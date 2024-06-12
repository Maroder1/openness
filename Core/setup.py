import sys
import os
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["pywinauto", "tkinter", "sqlite3"],
    "include_files": [
        # Assets
        "logo.png",
        "favico.ico",
        
        # Controller
        os.path.join("Controller", "OpennessController.py"),
        
        # Services
        os.path.join("Services", "OpennessService.py"),
        
        # repositories
        os.path.join("repositories", "Connection.py"),
        os.path.join("repositories", "MlfbManagement.py"),
        os.path.join("repositories", "UserConfig.py"),
        os.path.join("repositories", "ValidateDb.py"),
        os.path.join("repositories", "Openness.db"),
        
        # Database
        os.path.join("Database", "ddl.sql"),
        os.path.join("Database", "mlfb", "PLC_List.csv"),
        
        # SQLite
        os.path.join(sys.base_prefix, 'DLLs', 'sqlite3.dll')
    ]
}

if sys.platform == "win32":
    base = "Win32GUI"
    
target = Executable(
    script="Screen.py",
    base=base,
    icon="./favico.ico",
    target_name="RPA_Tia_Openness.exe"
    )

setup(
    name="RPA Tia Openness",
    version="0.1",
    description="Interface for automated creation of TIA Portal projects using Openness API",
    options={"build_exe": build_exe_options},
    executables=[target]
)
