from flask import Flask, request, jsonify
from .instruct import load_model, api_serve
import os
from llama_index.llms.llama_cpp import LlamaCPP
import json

app = Flask(__name__)

model_dir = "model"

config = {
    "host": "127.0.0.1",
    "port": "5173",
    "cert_file": "",
    "cert_key": ""
}

file_path=os.path.join(model_dir, "apiconfig.json")
if not os.path.exists(file_path):
    with open(file_path, "w") as json_file:
        json.dump(config, json_file)


model_files = [f for f in os.listdir('model') if f.endswith('.gguf')]
model_path = load_model(model_files[0]) if model_files else None

llm = LlamaCPP(
    model_path=model_path,
    temperature=0.1,
    max_new_tokens=512,
    context_window=3900,
    model_kwargs={"n_gpu_layers": 0},
    verbose=False,
)

@app.route('/v1/chat/completions', methods=['POST'])
def chat():
    user_input = request.json.get("input")

    if user_input.lower() == "exit":
        return jsonify({"response": "Exiting chat."})

    prompt_template = "<s>[INST] {prompt} [/INST]"
    prompt = prompt_template.format(prompt=user_input)

    response_iter = llm.stream_complete(prompt)
    response_text = ''.join(response.delta for response in response_iter)

    return jsonify({"response": response_text})

def main():
        with open(file_path, "r") as json_file:
            config = json.load(json_file)
            host=config["host"]
            port=config["port"]
            cert_file=config["cert_file"]
            cert_key=config["cert_key"]
        if cert_file is not "" and cert_key is not "":
            print(f"Inference is working on https://{host}:{port}/v1/chat/completions. You can configure custom host IP and port, and ssl certificate via the apiconfig.txt file available at {file_path}")
            app.run(host=host, port=port, debug=False, ssl_context=(cert_file,cert_key))
        else:
            print(f"Inference is working on http://{host}:{port}/v1/chat/completions. You can configure custom host IP and port, and ssl certificate via the apiconfig.txt file available at {file_path}")
            app.run(host=host, port=port, debug=False)

if __name__ == "__main__":
    main()
