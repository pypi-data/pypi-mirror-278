from flask import Flask, request, jsonify
from openai import AzureOpenAI
import argparse
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import os
import json


persist_directory = None

app = Flask(__name__)

model_dir = "model"

config = {
    "apikey": "",
    "version": "",
    "endpoint": "",
    "model": "",
    "host": "",
    "port": "",
    "cert_file": "",
    "cert_key": ""
}

file_path=os.path.join(model_dir, "azureapiconfig.json")
if not os.path.exists(file_path):
    with open(file_path, "w") as json_file:
        json.dump(config, json_file)



@app.route('/v1/chat/completions', methods=['POST'])
def chat():

    global persist_directory
    global multimodal_model
    global agent
    global client
    global model
    prompt_template = "You are a friendly assistant, who gives context aware responses on user query. Kindly analyse the provided context and give proper response\n   Context: {context}\n query: {prompt} "
    persist_directory = os.path.join('db',agent)

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create ChromaDB and store document IDs
    db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)
    user_input = request.json.get("input")

    if user_input.lower() == "exit":
        return jsonify({"response": "Exiting chat."})
    
    docs = db.similarity_search(user_input,k=1)
    context=docs[0].page_content
    prompt = prompt_template.format(context=context, prompt=user_input)
    response = client.chat.completions.create(
        model=model, # model = "deployment_name".
        messages=[
            {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
            {"role": "user", "content": prompt}
            
        ]
    )
    for choice in response.choices:
        return jsonify({"response": choice.message.content})

def main():
        global persist_directory
        global multimodal_model
        global agent
        global client
        global model
        parser = argparse.ArgumentParser()
        # parser.add_argument("--model", type=str, default="Mistral", help="Name of the model or path to the model file")
        parser.add_argument("--key", type=str, default=None, help="your azure openai key.")
        parser.add_argument("--version", type=str, default=None, help="Your azure api version.")
        parser.add_argument("--endpoint", type=str, default=None, help="Your azure endpoint")
        parser.add_argument("--model", type=str, default='gpt-35-turbo', help="Your cloud model deployed on azure.")
        parser.add_argument("--agent", type=str, default=None, help="Name of the agent to query.")
        args = parser.parse_args()
        agent = args.agent
        with open(file_path, "r") as json_file:
            config = json.load(json_file)
            key=config["apikey"]
            version=config["version"]
            endpoint=config["endpoint"]
            model=config["model"]
            host=config["host"]
            port=config["port"]
            cert_file=config["cert_file"]
            cert_key=config["cert_key"]
            # print(projectid, region, model)
        if key != "" and version != "" and endpoint != "" and model != "":
            client = AzureOpenAI(
                    api_key = (key),
                    api_version = version,
                    azure_endpoint = (endpoint)
                )
            model=args.model

        else:
            client = AzureOpenAI(
                    api_key = (args.key),
                    api_version = args.version,
                    azure_endpoint = (args.endpoint)
                )
            model=args.model
            config = {
                "apikey": args.key,
                "version": args.version,
                "endpoint": args.endpoint,
                "model": args.model,
                "host":"127.0.0.1",
                "port":"5000",
                "cert_file":"",
                "cert_key":""
            }
            with open(file_path, "w") as json_file:
                json.dump(config, json_file)


        
        if cert_file is not "" and cert_key is not "":
            print(f"Inference is working on https://{host}:{port}/v1/chat/completions. You can configure custom host IP and port, and ssl certificate via the apiconfig.txt file available at {file_path}")
            app.run(host=host, port=port, debug=False, ssl_context=(cert_file,cert_key))
        else:
            print(f"Inference is working on http://{host}:{port}/v1/chat/completions. You can configure custom host IP and port, and ssl certificate via the apiconfig.txt file available at {file_path}")
            app.run(host=host, port=port, debug=False)

if __name__ == "__main__":
    main()
