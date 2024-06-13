import datetime
import json
import os
import platform
import time
import psutil
import torch
from flask import jsonify, request
from .utils import check_for_saved_config


def create_defaults(app, sock, plugin_name, pipes, pipe_dict, default_params, load_pipe):
    check_for_saved_config(plugin_name, pipe_dict, default_params, load_pipe)
    @app.route('/')
    def home():
        return jsonify({'message': f'Welcome to the world {plugin_name}!'})
    
    @sock.route('/ws/healthcheck')
    def healthcheck_ws(ws):
        while True:
            data_str = ws.receive()
            if data_str:
                try:
                    data = json.loads(data_str)
                except json.JSONDecodeError:
                    data = {'request': data_str}
                if data.get('request') == 'system_stats':  # if they send a message requesting system stats
                    if torch.cuda.is_available():
                        device = "cuda"
                        cuda_version = torch.version.cuda
                    elif torch.backends.mps.is_available():
                        device = "mps"
                        cuda_version = "Not applicable"
                    else:
                        device = "cpu"
                        cuda_version = "Not applicable"
                    device_info = platform.uname()
                    system_stats = {
                        "cpu_percent": psutil.cpu_percent(),
                        "virtual_memory": psutil.virtual_memory(),
                        "disk_usage": psutil.disk_usage('/')
                    }
                    current_time = datetime.datetime.now().isoformat()
                    ws.send(json.dumps({
                        "device_info": device_info,
                        "system_stats": system_stats,
                        "current_time": current_time,
                        "environment_name": plugin_name,
                        "torch_device": device,
                        "cuda_version": cuda_version,
                        "mem_info": torch.cuda.mem_get_info()
                    }))
            time.sleep(1)  # sleep for a second before checking again

    @app.route('/healthcheck')
    def healthcheck():
        if torch.cuda.is_available():
            device = "cuda"
            cuda_version = torch.version.cuda
        elif torch.backends.mps.is_available():
            device = "mps"
            cuda_version = "Not applicable"
        else:
            device = "cpu"
            cuda_version = "Not applicable"
        device_info = platform.uname()
        system_stats = {
            "cpu_percent": psutil.cpu_percent(),
            "virtual_memory": psutil.virtual_memory(),
            "disk_usage": psutil.disk_usage('/')
        }
        current_time = datetime.datetime.now().isoformat()
        return jsonify({
            "device_info": device_info,
            "system_stats": system_stats,
            "current_time": current_time,
            "environment_name": plugin_name,
            "torch_device": device,
            "cuda_version": cuda_version,
            "mem_info": torch.cuda.mem_get_info()
        })
    
    @app.route("/config")
    def get_config():
        # everytime we call get config, save the config to a json file in the model directory, so we can re-init the app with the same config
        model_dir = os.getenv("HF_HOME") or "./models" 
        filename = os.path.join(model_dir, f"{plugin_name}_server_config.json")
        with open(filename, "w") as f:
            json.dump({
                "default_params": default_params,
                "pipelines": list(pipes.keys()),
                "pipeline": pipe_dict["name"],
                "loras": pipe_dict["loras"],
                "adapter_weights": pipe_dict["adapter_weights"],
            }, f)

        return jsonify({
            "default_params": default_params,
            "pipelines": list(pipes.keys()),
            "pipeline": pipe_dict["name"],
            "loras": pipe_dict["loras"],
            "adapter_weights": pipe_dict["adapter_weights"],
        })
    
    @app.route("/pipeline", methods=['PUT'])
    def update_pipeline():
        # global pipe_dict
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        pipeline = data.get("pipeline")
        if not pipeline in pipes:
            return jsonify({"message": "Pipeline not found"}), 404
        
        pipe_dict["pipeline"] = load_pipe(pipeline)
        pipe_dict["name"] = pipeline
        if data.get("refiner"):
            pipe_dict["refiner"] = load_pipe("refiner")
        else:
            pipe_dict["refiner"] = None

        # Reload any loaded_loras when we swap our pipeline
        if pipe_dict["loras"]:
            for lora in pipe_dict["loras"]:
                pipe_dict["pipeline"].load_lora_weights(lora['url'], weight_name=lora['weight_name'], adapter_name=lora['adapter_name'])
            pipe_dict["pipeline"].set_adapters([lora['adapter_name'] for lora in pipe_dict['loras']], adapter_weights=pipe_dict["adapter_weights"])
            pipe_dict["pipeline"].fuse_lora(adapter_names=[lora['adapter_name'] for lora in pipe_dict['loras']])

        return jsonify({"message": "Pipeline updated"})
    

def create_lora_helpers(app, pipes, pipe_dict, default_params, load_pipe):
    print("Creating lora helpers")
    
    @app.route("/loras", methods=['PUT'])
    def update_loras():
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        loras = data.get("loras")
        if not loras:
            pipe_dict['loras'] = []
            pipe_dict["pipeline"].unfuse_lora()
            return jsonify({"message": "Loras reset"}), 200
        pipe_dict['loras'] = loras
        # Unload all adapters before loading new ones to avoid ValueError
        pipe_dict["pipeline"] = load_pipe(pipe_dict["name"])
        for lora in loras:
            print(lora)
            pipe_dict["pipeline"].load_lora_weights(lora['url'], weight_name=lora['weight_name'], adapter_name=lora['adapter_name'])
        adapter_weights = data.get("weights")
        pipe_dict["adapter_weights"] = adapter_weights
        pipe_dict["pipeline"].set_adapters([lora['adapter_name'] for lora in loras], adapter_weights=adapter_weights)
        pipe_dict["pipeline"].fuse_lora(adapter_names=[lora['adapter_name'] for lora in loras])
        return jsonify({"message": "Loras updated"})
    



