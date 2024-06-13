import datetime
import importlib
import json
import os
import re
from typing import Union, List
import torch
import torch.distributed as dist
import torchaudio
from torchvision.io import write_video
from torchvision.transforms import ToTensor
from PIL import Image
from flask import Flask
from flask_cors import CORS
from flask_sock import Sock
import cv2
import numpy as np
import os
import requests
from tqdm import tqdm

def load_model_config(model_config_path=None):
    if model_config_path is None:
        model_config_path = os.path.join(os.getcwd(), "model.json")
    try:
        with open(model_config_path, "r") as file:
            model_config = json.load(file)
            default_params = model_config.get("params", {})
            plugin_name = model_config.get("name", "it broke")
    except FileNotFoundError:
        print(f"Warning: {model_config_path} not found. Using empty default parameters.")
        default_params = {}
        plugin_name = "it broke"
    return plugin_name, default_params


def check_for_saved_config(plugin_name, pipe_dict, default_params, load_pipe):
    model_dir = os.getenv("HF_HOME", "./models")
    filename = os.path.join(model_dir, f"{plugin_name}_server_config.json")
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # Ensure the directory for the file exists
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump({}, f)
        data = {}
    else:
        with open(filename) as f:
            data = json.load(f)
    if data.get("default_params"):
        default_params.update(data["default_params"])
    if data.get("pipeline"): # this will be the name 
        pipe_dict["name"] = data["pipeline"]
        pipe_dict["pipeline"] = load_pipe(data["pipeline"])
    if data.get("loras"):
        pipe_dict["loras"] = data["loras"]
    if data.get("adapter_weights"):
        pipe_dict["adapter_weights"] = data["adapter_weights"]
    if "loras" in pipe_dict and len(pipe_dict["loras"]) > 0 and "adapter_weights" in pipe_dict and len(pipe_dict["adapter_weights"]) > 0:
        # convert the weights to numbers
        pipe_dict["adapter_weights"] = [float(weight) for weight in pipe_dict["adapter_weights"]]
        for lora in pipe_dict["loras"]:
            pipe_dict["pipeline"].load_lora_weights(lora['url'], weight_name=lora['weight_name'], adapter_name=lora['adapter_name'])
        pipe_dict["pipeline"].set_adapters([lora['adapter_name'] for lora in pipe_dict['loras']], adapter_weights=pipe_dict["adapter_weights"])
        pipe_dict["pipeline"].fuse_lora(adapter_names=[lora['adapter_name'] for lora in pipe_dict['loras']])


def save_different_params(plugin_name, params):
    model_dir = os.getenv("HF_HOME", "./models")
    filename = os.path.join(model_dir, f"{plugin_name}_server_config.json")
    try:
        with open(filename, "r") as f:
            current_config = json.load(f)
        saved_params = current_config.get("default_params", {})
        different_params = [k for k, v in saved_params.items() if k != 'prompt' and str(params.get(k)) != str(v)]
        if different_params:
            print(f"Different params: {', '.join(different_params)}")
            print("Saving new params to server config")
            # Update only the different parameters to avoid overwriting with defaults
            for param in different_params:
                current_config["default_params"][param] = str(params[param]) if isinstance(params[param], bool) else params[param]
            with open(filename, "w") as f:
                json.dump(current_config, f, indent=4)
    except FileNotFoundError:
        with open(filename, "w") as f:
            json.dump({"default_params": params}, f, indent=4)


# takes in a pillow file and saves it to disk with proper formatting
def save_image(file, file_ext, prefix):
    inference_directory = os.getenv("INFERENCE_DIRECTORY", "./inference")
    datestr = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_prefix = re.sub(r'[^a-zA-Z0-9_-]', '', prefix)
    filename = f"{datestr}_{clean_prefix}.{file_ext}"
    outpath = os.path.join(inference_directory, filename)
    outdir = os.path.dirname(outpath)
    
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    file.save(outpath, format='PNG')
    
    # Explicitly delete the image object if it's no longer needed
    del file
    return outpath

def custom_export_to_video(frames, out_path, fps=14):
    # Check the file extension
    file_ext = os.path.splitext(out_path)[1]
    if file_ext == '.gif':
        # Save frames as a GIF
        frames[0].save(out_path, save_all=True, append_images=frames[1:], loop=0, duration=1/fps)
    else:
        # Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(out_path, fourcc, fps, (frames[0].size[1], frames[0].size[0]))
        for frame in frames:
            # Convert the image from BGR to RGB
            frame = cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2RGB)
            # Write the converted image
            video.write(frame)
        # Release the VideoWriter
        video.release()

def save_gif(frames, prefix, fps=24, quality=95, loop=1):
    imgs = frames #[Image.open(f) for f in sorted(frames)]
    if quality < 95:
        imgs = list(map(lambda x: x.resize((128, 128), Image.LANCZOS), imgs))
    inference_directory = os.getenv("INFERENCE_DIRECTORY", "./inference")
    datestr = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Clean the prefix by removing special characters other than "_" and "-"
    clean_prefix = re.sub(r'[^a-zA-Z0-9_-]', '', prefix)
    filename = f"{datestr}_{clean_prefix}.gif"
    outpath = os.path.join(inference_directory, filename) 
    outdir = os.path.dirname(outpath)
    duration_per_frame = 1000 // fps
    imgs[0].save(
        fp=outpath,
        format="GIF",
        append_images=imgs[1:],
        save_all=True,
        duration=duration_per_frame,
        loop=loop,
        quality=quality,
        optimize=False,
    )
    return outpath

def save_video(frames, prefix, fps=24, quality=95, audio_input=None):
    imgs = frames #[Image.open(f) for f in sorted(frames, key=lambda x: x.split("/")[-1])]
    if quality < 95:
        imgs = list(map(lambda x: x.resize((128, 128), Image.LANCZOS), imgs))

    img_tensors = [ToTensor()(img) for img in imgs]
    img_tensors = list(map(lambda x: x.unsqueeze(0), img_tensors))

    img_tensors = torch.cat(img_tensors)
    img_tensors = img_tensors * 255.0
    img_tensors = img_tensors.permute(0, 2, 3, 1)
    img_tensors = img_tensors.to(torch.uint8)

    inference_directory = os.getenv("INFERENCE_DIRECTORY", "./inference")
    datestr = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Clean the prefix by removing special characters other than "_" and "-"
    clean_prefix = re.sub(r'[^a-zA-Z0-9_-]', '', prefix)
    filename = f"{datestr}_{clean_prefix}.mp4"
    outpath = os.path.join(inference_directory, filename) 
    outdir = os.path.dirname(outpath)

    if audio_input is not None:
        audio_duration = len(img_tensors) / fps
        waveform, sr = torchaudio.load(audio_input)
        if waveform.shape[0] > 1:  # Check if audio is stereo
            waveform = torch.mean(waveform, dim=0, keepdim=True)  # Convert to mono
        num_frames = int(sr * audio_duration)
        waveform = waveform[:, :num_frames]  # Trim the waveform to the video duration
        audio_tensor = waveform.unsqueeze(0)

        write_video(
            outpath,
            video_array=img_tensors,
            fps=fps,
            audio_array=audio_tensor,
            audio_fps=sr,
            audio_codec="aac",
            video_codec="libx264",
        )
    else:
        write_video(
            outpath,
            video_array=img_tensors,
            fps=fps,
            video_codec="libx264",
        )

    return outpath


def create_app(name):
    app = Flask(name)
    CORS(app, resources={r"/*": {"origins": "*"}})  # This will enable CORS for all routes and all origins
    sock = Sock(app)

    print(f"cudnn version={torch.backends.cudnn.version()}")
    print(f"torch version={torch.__version__}")
    print(f"torch cuda version={torch.version.cuda}")

    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"

    return app, sock, device


# Helper method to create a safe file name
def create_safe_file_name(file_name):
    # Replace special characters in the file name to avoid OSError
    return re.sub(r'[\\/*?:"<>|]', "", file_name)

def count_params(model, verbose=False):
    total_params = sum(p.numel() for p in model.parameters())
    if verbose:
        print(f"{model.__class__.__name__} has {total_params*1.e-6:.2f} M params.")
    return total_params


def check_istarget(name, para_list):
    """ 
    name: full name of source para
    para_list: partial name of target para 
    """
    istarget=False
    for para in para_list:
        if para in name:
            return True
    return istarget


def instantiate_from_config(config):
    if not "target" in config:
        if config == '__is_first_stage__':
            return None
        elif config == "__is_unconditional__":
            return None
        raise KeyError("Expected key `target` to instantiate.")
    return get_obj_from_str(config["target"])(**config.get("params", dict()))


def get_obj_from_str(string, reload=False):
    module, cls = string.rsplit(".", 1)
    if reload:
        module_imp = importlib.import_module(module)
        importlib.reload(module_imp)
    return getattr(importlib.import_module(module, package=None), cls)


def load_npz_from_dir(data_dir):
    data = [np.load(os.path.join(data_dir, data_name))['arr_0'] for data_name in os.listdir(data_dir)]
    data = np.concatenate(data, axis=0)
    return data


def load_npz_from_paths(data_paths):
    data = [np.load(data_path)['arr_0'] for data_path in data_paths]
    data = np.concatenate(data, axis=0)
    return data   


def resize_numpy_image(image, max_resolution=512 * 512, resize_short_edge=None):
    h, w = image.shape[:2]
    if resize_short_edge is not None:
        k = resize_short_edge / min(h, w)
    else:
        k = max_resolution / (h * w)
        k = k**0.5
    h = int(np.round(h * k / 64)) * 64
    w = int(np.round(w * k / 64)) * 64
    image = cv2.resize(image, (w, h), interpolation=cv2.INTER_LANCZOS4)
    return image


def setup_dist(args):
    if dist.is_initialized():
        return
    torch.cuda.set_device(args.local_rank)
    torch.distributed.init_process_group(
        'nccl',
        init_method='env://'
    )


def download_model_if_not_exists(model_url, model_cache_directory, model_filename, max_attempts=3, headers=None):
    """
    Downloads a model file from a given URL to a specified directory with a specified filename if it does not already exist.
    Args:
    - model_url (str): URL of the model file to download.
    - model_cache_directory (str): Directory where the model file should be saved.
    - model_filename (str): Filename to save the model file as.
    - max_attempts (int): Maximum number of download attempts. Default is 3.
    - headers (dict): Optional headers to use for the request.
    """
    if not headers:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    full_path = os.path.join(model_cache_directory, model_filename)
    
    if os.path.exists(full_path) and os.path.getsize(full_path) > 0:
        print(f"Model file already exists at {full_path}. Skipping download.")
        return full_path

    os.makedirs(model_cache_directory, exist_ok=True)

    attempt = 0
    success = False
    while attempt < max_attempts and not success:
        try:
            response = requests.get(model_url, headers=headers, stream=True)
            response.raise_for_status()
            total_size_in_bytes = int(response.headers.get('content-length', 0))
            if total_size_in_bytes == 0:
                print("Received a 0-byte file, retrying...")
                attempt += 1
                continue

            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
            block_size = 1024  # 1 Kibibyte
            with open(full_path, 'wb') as file:
                for chunk in response.iter_content(block_size):
                    file.write(chunk)
                    progress_bar.update(len(chunk))
            progress_bar.close()

            if os.path.getsize(full_path) > 0:
                print("\nModel downloaded successfully.")
                success = True
            else:
                print("Downloaded file is 0 bytes, retrying...")
                attempt += 1
        except Exception as e:
            print(f"An error occurred: {e}")
            attempt += 1

    if not success:
        raise Exception("Failed to download model after multiple attempts.")
    return full_path

def get_available_vram():
    if torch.cuda.is_available():
        device = torch.device("cuda")
        total_memory = torch.cuda.get_device_properties(device).total_memory
        allocated_memory = torch.cuda.memory_allocated(device)
        free_memory = total_memory - allocated_memory
        return free_memory
    else:
        return 0

def get_total_vram():
    if torch.cuda.is_available():
        device = torch.device("cuda")
        total_memory = torch.cuda.get_device_properties(device).total_memory
        return total_memory
    else:
        return 0

def apply_low_memory_optimizations(pipe, optimizations={
    "vae_slicing": True,
    "vae_tiling": True,
    "model_cpu_offload": True,
    "sequential_cpu_offload": True,
}):
    if optimizations["vae_slicing"]:
        if hasattr(pipe, "enable_vae_slicing"):
            pipe.enable_vae_slicing()
    if optimizations["vae_tiling"]:
        if hasattr(pipe, "enable_vae_tiling"):
            pipe.enable_vae_tiling()
    if optimizations["model_cpu_offload"]:
        if hasattr(pipe, "enable_model_cpu_offload"):
            pipe.enable_model_cpu_offload()
    if optimizations["sequential_cpu_offload"]:
        if hasattr(pipe, "enable_sequential_cpu_offload"):
            pipe.enable_sequential_cpu_offload()
    return pipe

def auto_apply_low_memory_optimizations(pipe, vram_threshold=16):  # 16GB to differentiate 3090/4090+
    total_vram = get_total_vram()
    vram_threshold_bytes = vram_threshold * 1024 * 1024 * 1024  # Convert GB to bytes
    if total_vram < vram_threshold_bytes:
        print(f"Total VRAM: {total_vram / (1024 * 1024 * 1024):.2f} GB. Applying low memory optimizations.")
        if hasattr(pipe, "enable_vae_slicing"):
            pipe.enable_vae_slicing()
        if hasattr(pipe, "enable_vae_tiling"):
            pipe.enable_vae_tiling()
        if hasattr(pipe, "enable_model_cpu_offload"):
            pipe.enable_model_cpu_offload()
        if hasattr(pipe, "enable_sequential_cpu_offload"):
            pipe.enable_sequential_cpu_offload()
    else:
        print(f"Total VRAM: {total_vram / (1024 * 1024 * 1024):.2f} GB. Skipping low memory optimizations.")
    return pipe