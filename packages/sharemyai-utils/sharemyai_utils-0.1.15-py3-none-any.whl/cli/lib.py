import asyncio
import base64
import time
from dotenv import load_dotenv, set_key
import os
import json
import requests
import subprocess
import sys
import asyncio
from websockets.sync.client import connect

from cli.fingerprint import get_fingerprint
base_url = "https://sharemy.ai/api"
dotenv_path = '.env'
load_dotenv(dotenv_path)

def login_with_token(token):
    try:
        # Check if SESSION_TOKEN already exists and update it; otherwise, add it
        if 'SESSION_TOKEN' in os.environ:
            # Update the SESSION_TOKEN value in the .env file
            with open(dotenv_path, 'r') as file:
                lines = file.readlines()
            with open(dotenv_path, 'w') as file:
                for line in lines:
                    if line.startswith('SESSION_TOKEN='):
                        file.write(f'SESSION_TOKEN={token}\n')
                    else:
                        file.write(line)
        else:
            # Append the SESSION_TOKEN to the .env file
            with open(dotenv_path, 'a') as file:
                file.write(f'SESSION_TOKEN={token}\n')

        # Load the updated environment variables
        load_dotenv(dotenv_path)

        user = get_current_user()
        if not user:
            # Remove the token from .env
            with open(dotenv_path, 'r') as file:
                lines = file.readlines()
            with open(dotenv_path, 'w') as file:
                for line in lines:
                    if not line.startswith('SESSION_TOKEN='):
                        file.write(line)
            print("Login failed. Please try again.")
            return False
        return user
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def get_current_user():
    token = os.getenv('SESSION_TOKEN')
    if not token:
        print("No session token found. Please login first.")
        return
    response = requests.get(f"{base_url}/user", headers={"Authorization": f"Bearer {token}"})
    return response.json()

def post_register_worker(pluginId=None):
    token = os.getenv('SESSION_TOKEN')
    if not token:
        print("No session token found. Please login first.")
        return
    fingerprint_bytes = asyncio.run(get_fingerprint())
    fingerprint_str = fingerprint_bytes.hex()
    data = {"fingerprint": fingerprint_str}
    if pluginId is not None:
        data["pluginId"] = pluginId
    response = requests.post(f"{base_url}/plugin/worker", headers={"Authorization": f"Bearer {token}"}, json=data)
    return response.json()
 
def get_my_workers():
    token = os.getenv('SESSION_TOKEN')
    if not token:
        print("No session token found. Please login first.")
        return
    response = requests.get(f"{base_url}/plugin/worker", headers={"Authorization": f"Bearer {token}"})
    return response.json()

def get_and_download_plugin(pluginId, base_path):
    token = os.getenv('SESSION_TOKEN')
    if not token:
        print("No session token found. Please login first.")
        return
    response = requests.get(f"{base_url}/plugin?id={pluginId}", headers={"Authorization": f"Bearer {token}"})
    remotePlugin = response.json()
    if not remotePlugin:
        raise Exception(f"Could not find plugin with id {pluginId}")
    
    pluginPath = os.path.join(base_path, remotePlugin['name'])
    if not os.path.exists(pluginPath):
        os.makedirs(pluginPath, exist_ok=True)
    
    modelJson = {
        "name": remotePlugin['name'],
        "description": remotePlugin['description'],
        "isPublic": remotePlugin['isPublic'],
        "remoteUrl": remotePlugin['remoteUrl'],
        "capabilities": remotePlugin['capabilities'],
        "requirements": remotePlugin['requirements'],
        "torchRequirements": remotePlugin['torchRequirements'],
        "params": remotePlugin['params'],
    }
    
    runPyPath = os.path.join(pluginPath, 'run.py')
    modelJsonPath = os.path.join(pluginPath, 'model.json')
  
    with open(runPyPath, 'w') as run_py:
        run_py.write(remotePlugin['code'])
    with open(modelJsonPath, 'w') as model_json:
        json.dump(modelJson, model_json, indent=2)
    
    return remotePlugin, pluginPath

def create_venv(plugin_path):
    venv_path = os.path.join(plugin_path, 'venv')
    if not os.path.exists(venv_path):
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
    return venv_path

def install_requirements(venv_path, requirements_list):
    pip_path = 'Scripts' if os.name == 'nt' else 'bin'
    subprocess.check_call([os.path.join(venv_path, pip_path, 'pip'), 'install', '--upgrade', "sharemyai-utils"])
    subprocess.check_call([os.path.join(venv_path, pip_path, 'pip'), 'install', *requirements_list])

def install_torch_requirements(venv_path, dependencies):
    pip_path = 'Scripts' if os.name == 'nt' else 'bin'
    torch_index_url = "https://download.pytorch.org/whl/cu118"
    print("Installing torch dependencies from", torch_index_url)
    subprocess.check_call([os.path.join(venv_path, pip_path, 'pip'), 'install'] + dependencies + ["--index-url", torch_index_url])
    
def run_plugin(venv_path, plugin_path, plugin_name):
    # make ./models if it doesnt exist
    models_path = os.path.join('.', 'models')
    os.makedirs(models_path, exist_ok=True)
    # Adjust plugin_name to create a valid directory path
    plugin_config_path = os.path.join(models_path, plugin_name.replace('/', os.sep))
    os.makedirs(plugin_config_path, exist_ok=True)
    # make the server config json 
    with open(os.path.join(plugin_config_path, "server_config.json"), 'w') as server_config_json:
        json.dump({}, server_config_json)
    os.environ['HF_HOME'] = './models'
    pip_path = 'Scripts' if os.name == 'nt' else 'bin'
    process = subprocess.Popen([os.path.join(venv_path, pip_path, 'python'), os.path.join(plugin_path, 'run.py')])
    print('Running plugin', plugin_name, 'with pid', process.pid)
    return process.pid

def get_inference_job(worker_id):
    token = os.getenv('SESSION_TOKEN')
    if not token:
        print("No session token found. Please login first.")
        return
    response = requests.get(f"{base_url}/inference/request/process?workerId={worker_id}", headers={"Authorization": f"Bearer {token}"})
    return response.json()

def process_inference_job(prompt, input_image, params, model_params, job_id):
    token = os.getenv('SESSION_TOKEN')
    if not token:
        print("No session token found. Please login first.")
        return
    params = {**model_params, **params}
    params.pop('image', None)
    params.pop('prompt', None)

    body = {
        'prompt': prompt,
        **params,
    }
    if input_image:
        if isinstance(input_image, str):
            body['image'] = input_image
        else:
            # Assuming input_image is a file-like object
            body['image'] = base64.b64encode(input_image.read()).decode('utf-8')
    print(body)
    try:
        with connect("ws://localhost:3030/ws/generate") as websocket:
            websocket.send(json.dumps(body))
            while True:
                message = websocket.recv()
                json_message = json.loads(message)
                if "error" in json_message:
                    print(f"Error: {json_message['error']}")
                    result_response = requests.delete(f"{base_url}/inference/result/submit", headers={"Authorization": f"Bearer {token}"}, json={
                                  "resultId": job_id,
                                  "errorMessage": f"Error processing inference job: {json_message['error']}",
                                })
                    print('result_response:', result_response.json())
                    break
                elif "message" in json_message:
                    print(f"Message: {json_message['message']}")
                elif "progress" in json_message:
                    print(f"Progress: {json_message['progress']}%, Step: {json_message.get('step', '?')}, Total Steps: {json_message.get('inference_steps', '?')}")
                elif "file_paths" in json_message or "file_path" in json_message:
                    formatted_paths = json_message['file_paths'] if "file_paths" in json_message else [json_message['file_path']]
                    print("Generated Image Paths:", formatted_paths)
                    for path in json_message['file_paths'] if "file_paths" in json_message else [json_message['file_path']]:
                        filename = os.path.basename(path)
                        signed_response = requests.get(f"{base_url}/presigned?file={filename}", headers={"Authorization": f"Bearer {token}"})
                        presigned_url = signed_response.json().get('presignedUrl')
                        image_path = signed_response.json().get('imagePath')
                        
                        # Determine the content type based on the file extension
                        _, file_extension = os.path.splitext(filename)
                        content_type = {
                            '.png': 'image/png',
                            '.jpg': 'image/jpeg',
                            '.jpeg': 'image/jpeg',
                            '.gif': 'image/gif',
                            '.bmp': 'image/bmp',
                            '.tiff': 'image/tiff',
                            '.webp': 'image/webp',
                            '.svg': 'image/svg+xml',
                        }.get(file_extension.lower(), 'application/octet-stream')
                        
                        # Upload the image to the presigned URL
                        with open(path, 'rb') as f:
                            upload_response = requests.put(presigned_url, data=f.read(), headers={'Content-Type': content_type})
                            if upload_response.status_code == 200:
                                result_response = requests.post(f"{base_url}/inference/result/submit", headers={"Authorization": f"Bearer {token}"}, json={
                                    "resultId": job_id,
                                    "originalFilename": filename,
                                    "output": image_path,
                                })
                                print('Upload success')
                                break
                            else:
                                print(f"Failed to upload {filename}. Status code: {upload_response.status_code}")
                                result_response = requests.delete(f"{base_url}/inference/result/submit", headers={"Authorization": f"Bearer {token}"}, json={
                                    "resultId": job_id,
                                    "errorMessage": f"Error processing inference job - Upload {filename} to {image_path} - {upload_response.status_code}",
                                })
                        pass
                    break
                else:
                    print(json_message)
                    print("Unhandled message type received.")
    except Exception as e:
        print('No websocket connection:', e)
