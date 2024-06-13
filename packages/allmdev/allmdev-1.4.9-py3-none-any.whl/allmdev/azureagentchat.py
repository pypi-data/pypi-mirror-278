import os
from openai import AzureOpenAI
import argparse
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import json


model_dir = "model"

config = {
    "apikey": "",
    "version": "",
    "endpoint": "",
    "model": ""
}

file_path=os.path.join(model_dir, "azure_config.json")
if not os.path.exists(file_path):
    with open(file_path, "w") as json_file:
        json.dump(config, json_file)


def infer(model, client, agent):
    persist_directory = os.path.join('db',agent)

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create ChromaDB and store document IDs
    db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)
    prompt_template = "You are a friendly assistant, who gives context aware responses on user query. Kindly analyse the provided context and give proper response\n   Context: {context}\n query: {prompt} "
    while True:
        user_input = input("\n\nUser:")
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
            print(choice.message.content)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--key", type=str, default=None, help="your azure openai key.")
    parser.add_argument("--version", type=str, default=None, help="Your azure api version.")
    parser.add_argument("--endpoint", type=str, default=None, help="Your azure endpoint")
    parser.add_argument("--model", type=str, default='gpt-35-turbo', help="Your cloud model deployed on azure.")
    parser.add_argument("--agent", type=str, default=None, help="Name of the agent to query.")
    args = parser.parse_args()

    with open(file_path, "r") as json_file:
        config = json.load(json_file)
        key=config["apikey"]
        version=config["version"]
        endpoint=config["endpoint"]
        model=config["model"]
        # print(projectid, region, model)
    if key != "" and version != "" and endpoint != "" and model != "":
        client = AzureOpenAI(
                api_key = (key),
                api_version = version,
                azure_endpoint = (endpoint)
            )

        infer(args.model, client, args.agent)
    else:
        client = AzureOpenAI(
                api_key = (args.key),
                api_version = args.version,
                azure_endpoint = (args.endpoint)
            )
        config = {
            "apikey": args.key,
            "version": args.version,
            "endpoint": args.endpoint,
            "model": args.model
        }
        with open(file_path, "w") as json_file:
            json.dump(config, json_file)

        infer(args.model, client, args.agent)

if __name__=='__main__':
     main()
