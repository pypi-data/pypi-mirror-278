from flask import Flask, request, jsonify
from llama_index.llms.llama_cpp import LlamaCPP
from .instruct import load_model
import os
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import argparse


persist_directory = None

app = Flask(__name__)

# Check if apiconfig.txt exists in the model folder
config_file_path = os.path.join('model', 'apiconfig.txt')
if not os.path.exists(config_file_path):
    # Create apiconfig.txt with default values
    with open(config_file_path, 'w') as file:
       file.write('Host=127.0.0.1\n')
       file.write('Port=5000\n')
       file.write('CertFile=""\n')
       file.write('CertKey=""\n')

# Read host and port from apiconfig.txt
if os.path.exists(config_file_path):
    with open(config_file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            if key == 'Host':
                host = value
            elif key == 'Port':
                port = int(value)
            elif key == 'CertFile':
                cert_file = value.strip('"')
            elif key == 'CertKey':
                cert_key = value.strip('"')
else:
    print("File doesn't exist.")
    host = '127.0.0.1'
    port = 5000
    cert_file = ""
    cert_key = ""

print("Host:", host)
print("Port:", port)
print("CertFile:", cert_file)
print("CertKey:", cert_key)

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

    global persist_directory
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)
    user_input = request.json.get("input")

    if user_input.lower() == "exit":
        return jsonify({"response": "Exiting chat."})

    prompt_template = "You are a friendly assistant, who gives context aware responses on user query. Kindly analyse the provided context and give proper response\n   Context: {context}\n query:<s>[INST] {prompt} [/INST]"
    docs = db.similarity_search(user_input,k=1)
    context=docs[0].page_content
    prompt = prompt_template.format(context=context,prompt=user_input)

    response_iter = llm.stream_complete(prompt)
    response_text = ''.join(response.delta for response in response_iter)

    return jsonify({"response": response_text})

def main():
        global persist_directory
        parser = argparse.ArgumentParser()
        parser.add_argument("--agent", type=str, help="Name of the agent to query.")
        args = parser.parse_args()
        agentname=args.agent
        persist_directory = os.path.join('db', agentname)
        if cert_file is not "" and cert_key is not "":
            print(f"Inference is working on https://{host}:{port}/v1/chat/completions. You can configure custom host IP and port, and ssl certificate via the apiconfig.txt file available at {config_file_path}")
            app.run(host=host, port=port, debug=False, ssl_context=(cert_file,cert_key))
        else:
            print(f"Inference is working on http://{host}:{port}/v1/chat/completions. You can configure custom host IP and port, and ssl certificate via the apiconfig.txt file available at {config_file_path}")
            app.run(host=host, port=port, debug=False)

if __name__ == "__main__":
    main()
