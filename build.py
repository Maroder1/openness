import subprocess
import os
from Core.repositories.ValidateDb import validate_db

current_path = os.path.abspath(__file__)
core_path = os.path.join(os.path.dirname(current_path), "Core")

requirements_path = os.path.join(core_path, "requirements")

def install_dependencies():
    uninstall_dependencies()
    global requirements_path
    requirements_file = os.path.join(requirements_path, "requirements.txt")
    subprocess.call(["pip", "install", "-r", requirements_file])
    
def uninstall_dependencies():
    global requirements_path
    requirements_file = os.path.join(requirements_path, "uninstall.txt")
    subprocess.call(["pip", "uninstall", "-r", requirements_file])

def build():
    validate_db()
    global core_path
    os.chdir(core_path)
    setup_file = os.path.join(core_path, "setup.py")
    subprocess.call(["python", setup_file, "build"])
        
install_dependencies()
build()
