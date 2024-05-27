import subprocess
import os

current_path = os.path.abspath(__file__)
requiriments_path = os.path.join(os.path.dirname(current_path), "Core", "requirements")
script_dir = os.path.dirname(current_path)

def install_dependencies():
    uninstall_dependencies()
    global script_dir
    requirements_file = os.path.join(script_dir, "requirements.txt")
    subprocess.call(["pip", "install", "-r", requirements_file])
    
def uninstall_dependencies():
    global script_dir
    requirements_file = os.path.join(script_dir, "uninstall.txt")
    subprocess.call(["pip", "uninstall", "-r", requirements_file])

def build():
    global script_dir
    setup_dir = os.path.join(script_dir, "Core")
    os.chdir(setup_dir)  # change the current working directory
    setup_file = os.path.join(setup_dir, "setup.py")
    subprocess.call(["python", setup_file, "build"])

install_dependencies()
build()
