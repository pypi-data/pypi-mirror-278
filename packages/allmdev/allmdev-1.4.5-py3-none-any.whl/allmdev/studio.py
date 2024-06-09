from flask import Flask, render_template, request
from flask_socketio import SocketIO
import time
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
from llama_index.llms.llama_cpp import LlamaCPP
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app)

prompt_template = "<s>[INST] {prompt} [/INST]"

executor = ThreadPoolExecutor(max_workers=1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    prompt = data['userInput']
    modelPath = data['filePath']
    filepath = os.path.normpath(modelPath)
    path=filepath.replace("\\", "\\\\")
    temperature = data['temperature']
    useGPU = data['useGPU']
    print('Received userInput:', prompt)
    print('Received filePath:', path)
    print('Received temperature:', temperature)
    print('Received useGPU:', useGPU)

    formatted_prompt = prompt_template.format(prompt=prompt)

    # Initialize LLAM object with the selected model path, temperature, and GPU settings
    llm = LlamaCPP(
        model_path=path,
        temperature=float(temperature),
        max_new_tokens=512,
        context_window=3900,
        model_kwargs={"n_gpu_layers": 1 if useGPU else 0},
        verbose=False,
    )

    # Perform inference and stream the generated tokens
    response_iter = llm.stream_complete(formatted_prompt)
    prev_token = ''
    for response in response_iter:
        token = response.delta
        # new_token = token.replace(prev_token, token)
        # if new_token:
        print(token, end='')
        socketio.emit('response', token)
        # prev_token = token
    time.sleep(0.01)


    return None

def main():
    socketio.run(app, host='localhost', port=8080)

if __name__ == '__main__':
    main()
