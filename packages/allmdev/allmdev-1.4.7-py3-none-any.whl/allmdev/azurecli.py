from openai import AzureOpenAI
import argparse
import os
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

def infer(model, client):
    while True:
        user_input = input("\n\nUser:")
        response = client.chat.completions.create(
            model=model, # model = "deployment_name".
            messages=[
                {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
                {"role": "user", "content": user_input}
                
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

        infer(args.model, client)
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

        infer(args.model, client)
        

if __name__=='__main__':
     main()