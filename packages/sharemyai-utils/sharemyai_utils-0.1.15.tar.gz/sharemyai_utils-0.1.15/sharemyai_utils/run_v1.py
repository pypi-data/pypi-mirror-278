'''
run v1 plugins
'''
import os
import subprocess
import sys
import shutil
import re
import glob
import json
import urllib.request
import zipfile
from pathlib import Path

def download_file(url, savepath):
    """
    Download the file and save to savepath
    """
    print(f'Downloading {url}')
    urllib.request.urlretrieve(url, savepath)

def install_python(python_ver, python_path):
    """
    Download and install python
    """
    URL_PYTHON = f'https://www.python.org/ftp/python/{python_ver}/python-{python_ver}-embed-amd64.zip'
    URL_PIP = r'https://bootstrap.pypa.io/get-pip.py'
    URL_MSVC = r'https://sharemyai-releases-dev.s3.amazonaws.com/msvc.zip'
    python_zip_path = python_path / 'python.zip'
    pip_path = python_path / 'get-pip.py'
    msvc_zip_path = python_path / 'msvc.zip'
    
    # Download files if they do not exist
    if not python_zip_path.exists() and not (python_path / 'python.exe').exists():
        download_file(URL_PYTHON, python_zip_path)
    if not pip_path.exists() and not (python_path / 'Scripts' / 'pip.exe').exists():
        download_file(URL_PIP, pip_path)
    if not msvc_zip_path.exists() and not any(python_path.glob('msvc*.dll')):
        download_file(URL_MSVC, msvc_zip_path)
    
    # Extract python zip if not already extracted
    if not (python_path / 'python.exe').exists():
        print("Extracting python")
        with zipfile.ZipFile(python_zip_path, 'r') as zip_ref:
            zip_ref.extractall(python_path)
        python_zip_path.unlink()
    
    # Remove _pth file if it exists
    for pth_file in python_path.glob("*._pth"):
        pth_file.unlink()
    
    # Install MS VC dlls if not already installed
    if msvc_zip_path.exists() and not (python_path / 'msvc').exists():
        print("Installing MSVC dlls")
        with zipfile.ZipFile(msvc_zip_path, 'r') as zip_ref:
            zip_ref.extractall(python_path)
        msvc_zip_path.unlink()
    
    # Install pip if not already installed
    if not (python_path / 'Scripts' / 'pip.exe').exists():
        pip_process = subprocess.Popen(args='python.exe get-pip.py', cwd=str(python_path), shell=True)
        pip_process.wait()
        pip_path.unlink()
        # No need to kill the process as wait() ensures the process has terminated
        print('pip installation process completed')

# https://astral.sh/blog/uv lets go fast
# causes problems with check_call and piping the output to stdout, will need to cache and tree shake ourselves
def install_uv(python_executable):
    subprocess.check_call([python_executable, "-m", "pip", "install", "uv"], env=set_environment_variables(python_executable))

def install_dependencies(python_executable, dependencies):
    subprocess.check_call([python_executable, "-m", "pip", "install"] + dependencies, env=set_environment_variables(python_executable))

def install_sharemyai(python_executable):
    subprocess.check_call([python_executable, "-m", "pip", "install", "sharemyai_utils", "--upgrade"], env=set_environment_variables(python_executable))

def install_torch_dependencies(python_executable, dependencies):
    print("Python architecture:", "64-bit" if sys.maxsize > 2**32 else "32-bit")
    torch_index_url = "https://download.pytorch.org/whl/cu118"
    print("Installing torch dependencies from", torch_index_url)
    subprocess.check_call([python_executable, "-m", "pip", "install"] + dependencies + ["--index-url", torch_index_url], env=set_environment_variables(python_executable))
    
# todo, this should also use UV
def install_sharemyai_utils(python_executable):
    # temp workaround for sharemyai_utils
    # Check and install specific version of setuptools if version changed
    setuptools_version = "58.2.0"
    try:
        installed_version = subprocess.check_output([python_executable, "-m", "pip", "show", "setuptools"], env=set_environment_variables(python_executable)).decode().split('\n')[1].split(': ')[1].strip()
        if installed_version != setuptools_version:
            print(f"Updating setuptools from version {installed_version} to {setuptools_version}")
            subprocess.check_call([python_executable, "-m", "pip", "install", f"setuptools=={setuptools_version}"], env=set_environment_variables(python_executable))
    except subprocess.CalledProcessError:
        print("setuptools not found, installing version", setuptools_version)
        subprocess.check_call([python_executable, "-m", "pip", "install", f"setuptools=={setuptools_version}"], env=set_environment_variables(python_executable))
    sharemyai_utils_path = os.path.join(os.path.dirname(__file__), "sharemyai_utils")
    sharemyai_utils_dest_path = os.path.join(os.path.dirname(python_executable), "sharemyai_utils")
    
    # Check if sharemyai_utils version has changed before attempting re-installation or copying
    try:
        installed_sharemyai_utils_version = subprocess.check_output([python_executable, "-m", "pip", "show", "sharemyai_utils"], env=set_environment_variables(python_executable)).decode().split('\n')[1].split(': ')[1]
        with open(os.path.join(sharemyai_utils_path, 'sharemyai_utils', '__init__.py'), 'r') as f:
            local_version = f.readline().strip().split('=')[1].replace("'", "").strip()
        installed_sharemyai_utils_version = installed_sharemyai_utils_version.strip()
        local_version = local_version.strip()
        print(f"Installed sharemyai_utils version: {installed_sharemyai_utils_version}, Local sharemyai_utils version: {local_version}")
        if installed_sharemyai_utils_version.strip() == local_version.strip():
            print("Versions match. No update required.")
        else:
            print("Version mismatch detected. Update required.")
            print(f"Updating sharemyai_utils from version {installed_sharemyai_utils_version} to {local_version}")
            print("Copying sharemyai_utils to", sharemyai_utils_dest_path)
            shutil.copytree(sharemyai_utils_path, sharemyai_utils_dest_path, dirs_exist_ok=True)
            subprocess.check_call([python_executable, "-m", "pip", "install", "-e", sharemyai_utils_dest_path], env=set_environment_variables(python_executable))
            print("sharemyai_utils successfully installed or updated.")
    except subprocess.CalledProcessError as e:
        print("Installing sharemyai_utils for the first time.")
        print("Copying sharemyai_utils to", sharemyai_utils_dest_path)
        shutil.copytree(sharemyai_utils_path, sharemyai_utils_dest_path, dirs_exist_ok=True)
        subprocess.check_call([python_executable, "-m", "pip", "install", "-e", sharemyai_utils_dest_path], env=set_environment_variables(python_executable))
        print("sharemyai_utils successfully installed.")

def copy_cuda_dlls(python_path):
    # After installing torch, copy the CUDA dlls to the python's directory
    print("Copying CUDA dlls to python's directory")
    torch_lib_path = python_path / 'Lib' / 'site-packages' / 'torch' / 'lib'
    print("Torch lib path:", torch_lib_path)
    for cu_file in torch_lib_path.glob("cu*64*.dll"):
        destination_file = python_path / cu_file.name
        if not destination_file.exists():
            try:
                shutil.copy(cu_file, python_path)
                print(f'Copied {cu_file} to {python_path}')
            except Exception as e:
                print(f'Failed to copy {cu_file} to {python_path}. Error: {str(e)}')
    for file in torch_lib_path.glob("nvrtc*.dll"):
        destination_file = python_path / file.name
        if not destination_file.exists():
            try:
                shutil.copy(file, python_path)
                print(f'Copied {file} to {python_path}')
            except Exception as e:
                print(f'Failed to copy {file} to {python_path}. Error: {str(e)}')
    for file in torch_lib_path.glob("zlibwapi.dll"):
        destination_file = python_path / file.name
        if not destination_file.exists():
            try:
                shutil.copy(file, python_path)
                print(f'Copied {file} to {python_path}')
            except Exception as e:
                print(f'Failed to copy {file} to {python_path}. Error: {str(e)}')

def set_environment_variables(python_path, settings=None):
    env = os.environ.copy()
    env['CUDA_PATH'] = os.path.dirname(python_path)
    # Set the environment variables to the python's directory
    env['PYTHONHOME'] = '' #os.path.dirname(python_executable)
    env['PYTHONPATH'] = '' #os.path.join(os.path.dirname(python_executable), 'Lib', 'site-packages')
    env['PYTHON_PATH'] = os.path.dirname(python_path)
    env['PYTHONEXECUTABLE'] = \
    env['PYTHON_EXECUTABLE'] = \
    env['PYTHON_BIN_PATH'] = os.path.join(os.path.dirname(python_path), 'python.exe')
    env['PYTHONWEXECUTABLE'] = \
    env['PYTHON_WEXECUTABLE'] = os.path.join(os.path.dirname(python_path), 'pythonw.exe')
    env['PYTHON_LIB_PATH'] = os.path.join(os.path.dirname(python_path), 'Lib', 'site-packages')
    env['PYTHON_SCRIPTS_PATH'] = os.path.join(os.path.dirname(python_path), 'Scripts')  # Added the Python Scripts folder to the environment variables
    env['VIRTUAL_ENV'] = os.path.dirname(python_path)
    # add our settings to the environment variables
    if settings:
        if 'model_cache_directory' in settings:
            # env['HF_HOME'] = settings['model_cache_directory']
            # store them in the plugin env so they get removed together with the plugin
            env['HF_HOME'] = os.path.join(os.path.dirname(python_path), 'hf_home')
            os.makedirs(env['HF_HOME'], exist_ok=True)
        if 'torch_device' in settings:
            env['TORCH_DEVICE'] = settings['torch_device']
        if 'training_directory' in settings:
            env['TRAINING_DIRECTORY'] = settings['training_directory']
        if 'inference_directory' in settings:
            env['INFERENCE_DIRECTORY'] = settings['inference_directory']
        if 'hf_token' in settings:
            env['HF_TOKEN'] = settings['hf_token']
    return env

def run_app(python_executable, script_path, settings=None):
    print("Running", script_path)
    print("Python executable:", python_executable)
    # Use subprocess.check_call instead of subprocess.Popen to launch the script and auto pipe the output
    subprocess.check_call([python_executable, script_path], env=set_environment_variables(python_executable, settings))

def main(plugin_path, settings):
    print('python started')
    print(os.path.join(plugin_path, 'model.json'))
    model = json.load(open(os.path.join(plugin_path, 'model.json')))
    requirements = model["requirements"]
    torch_requirements = model["torchRequirements"]
    env_name = model["name"]
    script_path = os.path.join(plugin_path, "run.py")
    python_ver = "3.10.6"
    venvs_path = settings["python_env_directory"] if settings and "python_env_directory" in settings else "./venvs"
    python_path = Path(venvs_path, env_name)
    python_path.mkdir(parents=True, exist_ok=True)
    install_python(python_ver, python_path)
    python_executable = python_path / 'python.exe'
    # install_uv(python_executable)
    print('installing torch dependencies')
    install_torch_dependencies(python_executable, torch_requirements)
    print('successfully installed torch dependencies')
    copy_cuda_dlls(python_path)
    print('installing dependencies')
    install_dependencies(python_executable, requirements)
    print('successfully installed dependencies')
    print('installing sharemyai_utils')
    # install_sharemyai_utils(python_executable)
    install_sharemyai(python_executable)
    print('successfully installed sharemyai_utils')
    run_app(python_executable, script_path, settings)

if __name__ == "__main__":
    plugin_path = sys.argv[1] if len(sys.argv) > 1 else "plugins/Code/sd-test"
    json_settings_path = sys.argv[2] if len(sys.argv) > 2 else None
    print("Plugin path:", plugin_path)
    print("Settings path:", json_settings_path)
    settings = json.loads(open(json_settings_path).read()) if json_settings_path else None
    main(plugin_path, settings)

