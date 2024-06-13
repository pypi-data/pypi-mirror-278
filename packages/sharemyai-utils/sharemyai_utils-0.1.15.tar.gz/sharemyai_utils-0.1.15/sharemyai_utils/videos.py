import base64
import datetime
import gc
import io
import json
import os
import sys
from PIL import Image
from .utils import save_gif

def create_gen_video_websocket(sock, pipe_dict, default_params = {}, forward_pass=None):
    def generate_video_common(ws):
        while True:
            print("Waiting for data")
            data_str = ws.receive()
            if not data_str:
                print("No data received, skipping...")
                continue
            print(f"Data received: {len(data_str)} bytes")
            try:
                data = json.loads(data_str)
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {str(e)}")
                ws.send(json.dumps({'error': 'Invalid JSON data'}))
                continue
            params = {**default_params, **data}

            if not params['prompt'] and not params['image']:
                ws.send(json.dumps({'error': 'Either prompt or image is required'}))
                continue

            pipe = pipe_dict['pipeline']
            
            # Check if the image is sent as base64 or as a file object
            if 'image' in params and params['image']:
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

            def callback(_, step_index, timestep, kwargs):
                step = step_index + 1
                ws.send(json.dumps({
                    'step': step,
                    'steps': params.get('inference_steps', params.get('num_frames')),
                    'progress': f'{(step/params.get("inference_steps", params.get("num_frames")))*100:.2f}%'
                }))
                return kwargs
            
            # Auto convert strings to numbers for all params
            for key in params:
                if isinstance(params[key], str) and params[key].isdigit():
                    params[key] = int(params[key])
                elif isinstance(params[key], str) and '.' in params[key]:
                    try:
                        params[key] = float(params[key])
                    except ValueError:
                        pass
            if forward_pass:
                result = forward_pass(pipe, params)
            else:
                if image is None:
                    result = pipe(prompt=params['prompt'], decode_chunk_size=params['decode_chunk_size']).frames[0]
                else:
                    image = image.resize((params['width'], params['height']))
                    print(f"img2img image={image}")
                    print(f"pipe_params={params}")
                    result = pipe(image=image, decode_chunk_size=params['decode_chunk_size'], callback_on_step_end=callback).frames[0]
                
            prompt_or_time = params['prompt'] if params['prompt'] else datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = save_gif(result, prompt_or_time, loop=0)

            full_path = os.path.abspath(out_path)

            ws.send(json.dumps({
                'file_path': full_path
            }))

            del result, image, pipe
            if 'torch' in sys.modules:
                import torch
                torch.cuda.empty_cache()
            gc.collect()

    @sock.route('/ws/generate/video')
    def generate_video(ws):
        generate_video_common(ws)

    @sock.route('/ws/generate')
    def generate(ws):
        generate_video_common(ws)