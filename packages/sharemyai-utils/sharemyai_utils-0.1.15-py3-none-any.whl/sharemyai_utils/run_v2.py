'''
run v2 plugins - gradio/web interfaces
'''
import os
import subprocess
import sys
import shutil
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
        print("pip not found, installing pip")
        subprocess.Popen(args='python.exe get-pip.py', cwd=str(python_path), shell=True).wait()
        pip_path.unlink()

    # Install dload if not already installed
    if not (python_path / 'Scripts' / 'dload.exe').exists():
        subprocess.Popen(args='python.exe -m pip install dload', cwd=str(python_path), shell=True).wait()
    
    # Install GitPython if not already installed
    if not (python_path / 'Scripts' / 'git.exe').exists():
        print("GitPython not found, installing GitPython")
        subprocess.Popen(args='python.exe -m pip install gitpython', cwd=str(python_path), shell=True).wait()

    # install gdown
    if not (python_path / 'Scripts' / 'gdown.exe').exists():
        subprocess.Popen(args='python.exe -m pip install gdown', cwd=str(python_path), shell=True).wait()

# https://astral.sh/blog/uv lets go fast
def install_uv(python_executable):
    subprocess.check_call([python_executable, "-m", "pip", "install", "uv"], env=set_environment_variables(python_executable))

def install_sharemyai(python_executable):
    subprocess.check_call([python_executable, "-m", "pip", "install", "sharemyai_utils", "--upgrade"], env=set_environment_variables(python_executable))


def install_dependencies(python_executable, plugin_full_path, dependencies, dependencies_overrides, dependencies_remove):
    filtered_dependencies = []
    pip_dependencies = []
    if "requirements.txt" in dependencies:
        requirements_path = f"{plugin_full_path}/requirements.txt"
        with open(requirements_path, "r") as req_file:
            all_requirements = req_file.readlines()
            for req in all_requirements:
                req = req.strip()
                if req and not req.startswith("#") and "torch" not in req and "xformers" not in req:
                    # Check for overrides
                    if req in dependencies_overrides:
                        req = dependencies_overrides[req]
                    if req in dependencies_remove:
                        continue
                    filtered_dependencies.append(req)
        
        for requirement in filtered_dependencies:
            subprocess.check_call([python_executable, "-m", "pip", "install", requirement], env=set_environment_variables(python_executable))
        dependencies.remove("requirements.txt")
    
    environment_file = "environment.yaml" if "environment.yaml" in dependencies else "environment.yml" if "environment.yml" in dependencies else None
    if environment_file:
        environment_path = f"{plugin_full_path}/{environment_file}"
        with open(environment_path, "r") as env_file:
            in_pip_section = False
            for line in env_file:
                if line.strip() == "pip:":
                    in_pip_section = True
                elif in_pip_section and line.startswith("  -"):
                    pip_dependency = line.strip()[2:]
                    if "torch" not in pip_dependency and "xformers" not in pip_dependency:
                        # Check for overrides
                        if pip_dependency in dependencies_overrides:
                            pip_dependency = dependencies_overrides[pip_dependency]
                        pip_dependencies.append(pip_dependency)
                elif in_pip_section and not line.startswith("  -"):
                    in_pip_section = False
        for pip_dependency in pip_dependencies:
            subprocess.check_call([python_executable, "-m", "pip", "install", pip_dependency], env=set_environment_variables(python_executable))
        dependencies.remove(environment_file)
    
    if dependencies:  # Check if there are any dependencies left to install after potentially removing "requirements.txt" and environment file
        remaining_dependencies = [dep for dep in dependencies] #if "torch" not in dep and "xformers" not in dep]
        if remaining_dependencies:
            subprocess.check_call([python_executable, "-m", "pip", "install"] + remaining_dependencies, env=set_environment_variables(python_executable))

def install_torch_dependencies(python_executable, dependencies):
    print("Python architecture:", "64-bit" if sys.maxsize > 2**32 else "32-bit")
    torch_index_url = "https://download.pytorch.org/whl/cu118"
    print("Installing torch dependencies from", torch_index_url)
    subprocess.check_call([python_executable, "-m", "pip", "install"] + dependencies + ["--index-url", torch_index_url], env=set_environment_variables(python_executable))
    
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
            env['HF_HOME'] = settings['model_cache_directory']
        if 'torch_device' in settings:
            env['TORCH_DEVICE'] = settings['torch_device']
        if 'training_directory' in settings:
            env['TRAINING_DIRECTORY'] = settings['training_directory']
        if 'inference_directory' in settings:
            env['INFERENCE_DIRECTORY'] = settings['inference_directory']
        if 'hf_token' in settings:
            env['HF_TOKEN'] = settings['hf_token']
    return env

def forward_output(pipe, label):
    for line in iter(pipe.readline, b''):
        print(f"{label}: {line.decode()}", end='')

def run_app(python_executable, plugin_path, run_commands, settings=None):
    print("Running", run_commands)
    print("Python executable:", python_executable)
    # attach our plugin path to the run command
    run_commands[0] = run_commands[0] #os.path.join(plugin_path, )
    # Use subprocess.Popen to launch the script with the updated working directory
    commands = [python_executable] + run_commands
    subprocess.check_call(commands, env=set_environment_variables(python_executable, settings), cwd=plugin_path)

def sanitize_path(path):
    return path.replace('\\x07', 'x07').replace('\\', '/')

def download_plugin(python_executable, url, plugin_path):
    """
    Download the plugin from the git url using a subprocess to utilize gitpython installed in the python executable path
    """
    plugin_path = sanitize_path(plugin_path)  # Sanitize the path
    print(f'Downloading {url} to {plugin_path}')
    # make the folder if it doesn't exist
    os.makedirs(plugin_path, exist_ok=True)
    download_command = f'from git import Repo; Repo.clone_from("{url}", "{plugin_path}")'
    subprocess.run([python_executable, "-c", download_command], check=True)

def run_postinstall(python_executable, postinstall_commands):
    for command in postinstall_commands:
        print("Running postinstall command:", command)
        try:
            subprocess.check_call([python_executable, "-c", command], env=set_environment_variables(python_executable))
        except subprocess.CalledProcessError as e:
            print(f"Error running postinstall command '{command}': {e}")
            sys.exit(1)

def run_runfile_overrides(runfile_path, runfile_overrides):
    # our runfile_overrides are key: value for string replacement (inline)
    # Open the python file to read its contents
    with open(runfile_path, 'r', encoding='utf-8') as file:
        code = file.read()
    # Replace each instance of key in our python file with our value, ensuring not to duplicate replacements
    for key, value in runfile_overrides.items():
        print(f"Replacing '{key}' with '{value}' in {runfile_path}")
        # Improved check to avoid duplicate replacements by examining the context around found strings
        start_index = 0
        while True:
            start_index = code.find(key, start_index)
            if start_index == -1:  # Key not found, move to next key
                break
            print(f"Replacing '{key}' with '{value}' in {runfile_path} at index {start_index}")
            # Check the surroundings of the found key to ensure it's not already replaced
            pre_context = code[max(0, start_index - len(value)):start_index]
            post_context = code[start_index + len(key):start_index + len(key) + len(value)]
            if value == "" or pre_context != value or post_context != value:  # If surroundings don't match the value, replace
                code = code[:start_index] + value + code[start_index + len(key):]
                start_index += len(value) if value else len(key)  # Move past the newly replaced segment or the key if value is empty
            else:
                start_index += len(key)  # Move past the current found key

    # Write the modified code back to the python file
    with open(runfile_path, 'w', encoding='utf-8') as file:
        file.write(code)
    print(f'Wrote runfile overrides to {runfile_path}')
            
def main(plugin_path, settings):
    pluginJson = json.load(open(plugin_path))
    plugin_name = pluginJson["name"]
    run_commands = pluginJson["run"]
    runfile = pluginJson.get("runfile", "")
    postinstall_commands = pluginJson.get("postInstall", [])
    runfile_overrides = pluginJson.get("runfileOverrides", {})
    python_ver = "3.10.6"
    venvs_path = settings["python_env_directory"] if settings and "python_env_directory" in settings else "./venvs"
    python_path = Path(venvs_path, plugin_name)
    python_path.mkdir(parents=True, exist_ok=True)
    install_python(python_ver, python_path)
    # Check if our plugin exists in the directory of the plugin JSON file, if not download it 
    plugin_directory = os.path.dirname(plugin_path)
    plugin_name = pluginJson["name"]
    python_executable = python_path / 'python.exe'
    # install_uv(python_executable)
    plugin_full_path = os.path.join(plugin_directory, plugin_name)
    if not os.path.exists(plugin_full_path) or not os.listdir(plugin_full_path):
        download_plugin(python_executable, pluginJson["remoteUrl"], plugin_full_path)
        # if we downloaded a plugin, check if it is sitting in a folder, if so move the contents to the plugin directory
        downloaded_plugin_path = plugin_full_path
        if len(os.listdir(downloaded_plugin_path)) == 1:
            inner_folder_path = os.path.join(downloaded_plugin_path, os.listdir(downloaded_plugin_path)[0])
            if os.path.isdir(inner_folder_path):  # Ensure it's a directory
                for file in os.listdir(inner_folder_path):
                    shutil.move(os.path.join(inner_folder_path, file), downloaded_plugin_path)
                os.rmdir(inner_folder_path)
    install_torch_dependencies(python_executable, pluginJson["torchRequirements"])
    copy_cuda_dlls(python_path)
    install_dependencies(python_executable, plugin_full_path, pluginJson["requirements"], pluginJson.get('requirementsOverrides', {}), pluginJson.get('requirementsRemove', []))
    # install_sharemyai_utils(python_executable)
    install_sharemyai(python_executable)
    # Change the current working directory to the plugin path so that relative paths in the Python app are based on the plugin path
    print("Changing current working directory to", plugin_full_path)
    # os.chdir(plugin_full_path)
    run_postinstall(python_executable=python_executable, postinstall_commands=postinstall_commands)
    if runfile_overrides and runfile != "":
        runfile_full_path = os.path.join(plugin_full_path, runfile)
        run_runfile_overrides(runfile_full_path, runfile_overrides)
    
    run_app(python_executable, plugin_full_path, run_commands, settings)

if __name__ == "__main__":
    plugin_path = sys.argv[1] if len(sys.argv) > 1 else ""
    json_settings_path = sys.argv[2] if len(sys.argv) > 2 else None
    print("Plugin path:", plugin_path)
    print("Settings path:", json_settings_path)
    settings = json.loads(open(json_settings_path).read()) if json_settings_path else None
    main(plugin_path, settings)

