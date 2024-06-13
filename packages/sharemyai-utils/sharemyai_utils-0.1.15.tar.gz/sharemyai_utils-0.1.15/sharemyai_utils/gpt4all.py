import datetime
import json
import os
from .utils import create_safe_file_name

# generator method to make websocket creation easier
# keeps us to standard format
# we check passed in params to know what pipes to look for and what data to expect
def create_gen_txt_websocket(sock, plugin_name, pipe_dict, default_params = {}, forward_pass=None):
    def generate_txt_common(ws):
        while True:
            data_str = ws.receive()
            if not data_str:
                continue
            data = json.loads(data_str)
            prompt = data.get('prompt')
            max_tokens = data.get('max_tokens') or 512
            temperature = data.get('temperature') or 0
            if not prompt:
                ws.send(json.dumps({'error': 'Prompt is required'}))
                continue
            
            model = pipe_dict["pipeline"]

            response = ""
            token_count = 0
            tokens = []
            for token in model.generate(prompt, max_tokens=max_tokens, temp=temperature, streaming=True):
                tokens.append(token)
                token_count += 1
                response += token
                ws.send(json.dumps({'text': token, "count": token_count}))

            # Save the result to a local file
            # Use the date and prompt to name the file
            date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{date_str}_{prompt.replace(' ', '_')}.txt"
            inference_directory = os.getenv("INFERENCE_DIRECTORY", "./inference")
            out_path = os.path.join(inference_directory, file_name)
            out_dir = os.path.dirname(out_path)
            
            # Make the directory if it doesn't exist
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)

            safe_file_name = create_safe_file_name(file_name)
            safe_out_path = os.path.join(inference_directory, safe_file_name)

            with open(safe_out_path, 'w') as f:
                f.write(response)
            
            # Return the file path as a response
            ws.send(json.dumps({
                "file_path": safe_out_path,
                'text': response
            }))

    @sock.route('/ws/generate/txt')
    def generate_txt(ws):
        generate_txt_common(ws)

    @sock.route('/ws/generate')
    def generate(ws):
        generate_txt_common(ws)


def create_gen_chat_websocket(sock, plugin_name, pipe_dict, default_params = {}, forward_pass=None):
    def generate_chat_common(ws):
         # we can hold the chat session for the entire websocket connection
        # they can disconnect and reconnect, send an id to re-hydrate, or its a new session
        model = pipe_dict["pipeline"]
        with model.chat_session() as chat:
            while True:
                data_str = ws.receive()
                if not data_str:
                    continue
                data = json.loads(data_str)
                prompt = data.get('prompt')
                max_tokens = data.get('max_tokens') or 512
                temperature = data.get('temperature') or 0
                if not prompt:
                    ws.send(json.dumps({'error': 'Prompt is required'}))
                    continue

                historical_messages = data.get('historicalMessages')
                if historical_messages:
                    # waiting on gpt4all to add official reload support, this will leak data (dont use for shared inference)
                    model._history = historical_messages

                response = ""
                token_count = 0
                tokens = []
                for token in model.generate(prompt, max_tokens=max_tokens, temp=temperature, streaming=True):
                    tokens.append(token)
                    token_count += 1
                    response += token
                    ws.send(json.dumps({'text': token, "count": token_count}))

                # Save the result to a local file
                # Use the date and prompt to name the file
                date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{date_str}_{prompt.replace(' ', '_')}.txt"
                inference_directory = os.getenv("INFERENCE_DIRECTORY", "./inference")
                out_path = os.path.join(inference_directory, file_name)
                out_dir = os.path.dirname(out_path)
                
                # Make the directory if it doesn't exist
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)

                # Replace special characters in the file name to avoid OSError
                safe_file_name = create_safe_file_name(file_name)
                safe_out_path = os.path.join(inference_directory, safe_file_name)

                with open(safe_out_path, 'w') as f:
                    f.write(response)
                
                # Return the file path as a response
                ws.send(json.dumps({
                    "file_path": safe_out_path,
                    'text': response,
                    "historicalMessages": model.current_chat_session
                }))


    @sock.route('/ws/generate/chat')
    def generate_chat(ws):
        generate_chat_common(ws)

    @sock.route('/ws/chat')
    def chat(ws):
        generate_chat_common(ws)
