import base64
import gc
import io
import json
import os
import sys
from PIL import Image
from .utils import save_different_params, save_image

# generator method to make websocket creation easier
# keeps us to standard format
# we check passed in params to know what pipes to look for and what data to expect
def create_gen_img_websocket(sock, plugin_name, pipe_dict, default_params = {
    "prompt": "",
    "negative_prompt": "",
    "image": "",
    "inference_steps": 40,
    "guidance_scale": 5.0,
    "strength": 1.0,
    "batch_size": 1,
    "height": 512,
    "width": 512
}, forward_pass=None):
    def generate_img_common(ws):
        while True:
            data_str = ws.receive()
            if not data_str:
                continue
            try:
                data = json.loads(data_str)
            except json.JSONDecodeError:
                data = {'prompt': data_str}
            params = {**default_params, **data}
           
            if not params.get('prompt') and not params.get('image'):
                ws.send(json.dumps({'error': 'Either prompt or image is required'}))
                continue
            
            pipe = pipe_dict.get('pipeline', None)
            refiner = pipe_dict.get('refiner', None)
          
            # Check if the image is sent as base64 or as a file object
            if params.get('image'):
                image = None
                # First, check if it looks like a file path or object
                if any(ext in params['image'] for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                    try:
                        image = Image.open(params['image'])
                    except FileNotFoundError:
                        ws.send(json.dumps({'error': 'Image file not found'}))
                    except Exception as e:
                        ws.send(json.dumps({'error': 'Error opening image file'}))
                else:
                    # If it doesn't look like a file, attempt to decode as base64
                    try:
                        image_data = base64.b64decode(params['image'].split(',')[-1])  # Handle potential data URI scheme
                        image = Image.open(io.BytesIO(image_data))
                    except Exception as e:
                        ws.send(json.dumps({'error': 'Invalid or unrecognized image data'}))
            else:
                image = None

            def callback(pipe, step_index, timestep, callback_kwargs):
                step = step_index + 1
                ws.send(json.dumps({
                    'step': step,
                    'inference_steps': params.get('inference_steps', 40),
                    'progress': f'{(step/params.get("inference_steps", 40))*100}'
                }))
                return callback_kwargs
            
            try:
                # Generate images based on the presence of an initial image or just a prompt
                generation_args = {
                    "prompt": params.get('prompt'),
                    "callback_on_step_end": callback
                }
                if 'negative_prompt' in default_params:
                    generation_args["negative_prompt"] = params.get('negative_prompt')
                if 'batch_size' in default_params:
                    generation_args["num_images_per_prompt"] = params.get('batch_size', 1)
                if 'inference_steps' in default_params:
                    generation_args["num_inference_steps"] = params.get('inference_steps', 40)
                if 'guidance_scale' in default_params:
                    generation_args["guidance_scale"] = params.get('guidance_scale', 5.0)
                if 'height' in default_params:
                    generation_args["height"] = params.get('height', 512)
                if 'width' in default_params:
                    generation_args["width"] = params.get('width', 512)
                if 'eta' in default_params:
                    generation_args["eta"] = params.get('eta', 0.3)
                if image is not None:
                    generation_args.update({"image": image, "strength": params.get('strength', 1.0)})
                result = forward_pass(pipe, **generation_args) if forward_pass else pipe(**generation_args)
            except Exception as e:
                ws.send(json.dumps({'error': str(e)}))
                continue

            # Refine generated images if required
            if refiner and params.get('use_refiner', False):
                refine_args = {
                    "prompt": params.get('prompt'),
                    "negative_prompt": params.get('negative_prompt'),
                    "image": result.images,
                    "num_inference_steps": params.get('inference_steps', 40),
                    "height": params.get('height', 512),
                    "width": params.get('width', 512),
                    "callback_on_step_end": callback
                }
                result = refiner(**refine_args)

            # if the params are different from our server config, save them to the server config
            save_different_params(plugin_name, params)
            # Save generated images to disk and collect their file paths
            file_paths = []
            for idx, image in enumerate(result.images, start=1):
                out_path = save_image(image, "png", f"{params.get('prompt')}_{idx}")
                full_path = os.path.abspath(out_path)
                file_paths.append(full_path)

            # Return the array of full file paths as a response
            ws.send(json.dumps({
                'file_paths': file_paths
            }))

            # Free GPU memory and RAM after each call
            del result, image, pipe, refiner
            if 'torch' in sys.modules:
                import torch
                torch.cuda.empty_cache()
                
            gc.collect()

    @sock.route('/ws/generate/image')
    def generate_img(ws):
        generate_img_common(ws)

    @sock.route('/ws/generate')
    def generate(ws):
        generate_img_common(ws)