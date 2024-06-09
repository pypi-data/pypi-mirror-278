import vertexai
from vertexai.generative_models import GenerativeModel
import argparse
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import os
import json


model_dir = "model"

config = {
    "project_id": "",
    "region": "",
    "model": ""
}

file_path=os.path.join(model_dir, "vertex_config.json")
if not os.path.exists(file_path):
    with open(file_path, "w") as json_file:
        json.dump(config, json_file)


# Query the model
def infer(multimodal_model, agent):
    prompt_template = "You are a friendly assistant, who gives context aware responses on user query. Kindly analyse the provided context and give proper response\n   Context: {context}\n query: {prompt} "
    persist_directory = os.path.join('db',agent)

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create ChromaDB and store document IDs
    db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)

    while True:
        user_input = input("\n\nUser:")
        docs = db.similarity_search(user_input,k=1)
        context=docs[0].page_content
        prompt = prompt_template.format(context=context, prompt=user_input)
        response = multimodal_model.generate_content(prompt)
        print(response.text)
# return response.text



def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--model", type=str, default="Mistral", help="Name of the model or path to the model file")
    parser.add_argument("--projectid", type=str, default=None, help="Id of your GCP project.")
    parser.add_argument("--region", type=str, default=0.5, help="Your cloud provider region.")
    parser.add_argument("--agent", type=str, default=None, help="Name of the agent to query.")
    args = parser.parse_args()
    with open(file_path, "r") as json_file:
        config = json.load(json_file)
        projectid=config["project_id"]
        region=config["region"]
        model=config["model"] 
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
            "model": args.model
        }
        with open(file_path, "w") as json_file:
            json.dump(config, json_file)

    infer(multimodal_model, args.agent)

if __name__=='__main__':
     main()