from flask import Flask, request, jsonify
import vertexai
from vertexai.generative_models import GenerativeModel
import argparse
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import os
import json


persist_directory = None

app = Flask(__name__)

model_dir = "model"

config = {
    "project_id": "",
    "region": "",
    "model": "",
    "host": "",
    "port": "",
    "cert_file": "",
    "cert_key": ""
}

file_path=os.path.join(model_dir, "vertexapiconfig.json")
if not os.path.exists(file_path):
    with open(file_path, "w") as json_file:
        json.dump(config, json_file)



@app.route('/v1/chat/completions', methods=['POST'])
def chat():

    global persist_directory
    global multimodal_model
    global agent
    prompt_template = "You are a friendly assistant, who gives context aware responses on user query. Kindly analyse the provided context and give proper response\n   Context: {context}\n query: {prompt} "
    persist_directory = os.path.join('db',agent)

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create ChromaDB and store document IDs
    db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)

    user_input = request.json.get("input")

    if user_input.lower() == "exit":
        return jsonify({"response": "Exiting chat."})

    prompt_template = "You are a friendly assistant, who gives context aware responses on user query. Kindly analyse the provided context and give proper response\n   Context: {context}\n query:<s>[INST] {prompt} [/INST]"
    docs = db.similarity_search(user_input,k=1)
    context=docs[0].page_content
    prompt = prompt_template.format(context=context,prompt=user_input)
    response = multimodal_model.generate_content(prompt)
    return jsonify({"response": response.text})

def main():
        global persist_directory
        global multimodal_model
        global agent
        parser = argparse.ArgumentParser()
        parser.add_argument("--projectid", type=str, default=None, help="Id of your GCP project.")
        parser.add_argument("--region", type=str, default=None, help="Your cloud provider region.")
        parser.add_argument("--agent", type=str, help="Name of the agent to query.")
        parser.add_argument("--model", type=str, default="gemini-1.0-pro-002", help="Your cloud model on VertexAI.")
        args = parser.parse_args()
        agent=args.agent
        persist_directory = os.path.join('db', agent)
        with open(file_path, "r") as json_file:
            config = json.load(json_file)
            projectid=config["project_id"]
            region=config["region"]
            model=config["model"]
            host=config["host"]
            port=config["port"]
            cert_file=config["cert_file"]
            cert_key=config["cert_key"]
            # print(projectid, region, model)
        if projectid != "" and region != "" and model != "":
        # Initialize Vertex AI
            vertexai.init(project=projectid, location=region)
            # Load the model
            multimodal_model = GenerativeModel(model_name=model)
        else:
            vertexai.init(project=args.projectid, location=args.region)
            # Load the model
            multimodal_model = GenerativeModel(model_name=args.model)
            config = {
                "project_id": args.projectid,
                "region": args.region,
                "model": args.model,
                "host":"127.0.0.1",
                "port":"5000",
                "cert_file":"",
                "cert_key":""
            }
            with open(file_path, "w") as json_file:
                json.dump(config, json_file)
        
        if cert_file is not "" and cert_key is not "":
            print(f"Inference is working on https://{host}:{port}/v1/chat/completions. You can configure custom host IP and port, and ssl certificate via the vertexapiconfig.json file available at {file_path}")
            app.run(host=host, port=port, debug=False, ssl_context=(cert_file,cert_key))
        else:
            print(f"Inference is working on http://{host}:{port}/v1/chat/completions. You can configure custom host IP and port, and ssl certificate via the vertexapiconfig.json file available at {file_path}")
            app.run(host=host, port=port, debug=False)

if __name__ == "__main__":
    main()
