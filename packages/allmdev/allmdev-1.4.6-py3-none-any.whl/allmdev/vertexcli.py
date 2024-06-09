import vertexai
from vertexai.generative_models import GenerativeModel
import argparse
import json
import os

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
def infer(multimodal_model):
    while True:
        user_input = input("\n\nUser:")
        response = multimodal_model.generate_content(user_input)
        print(response.text)
# return response.text



def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--model", type=str, default="Mistral", help="Name of the model or path to the model file")
    parser.add_argument("--projectid", type=str, default=None, help="Id of your GCP project.")
    parser.add_argument("--region", type=str, default=None, help="Your cloud provider region.")
    parser.add_argument("--model", type=str, default='gemini-1.0-pro-002', help="Your cloud model deployed on VertexAI.")
    args = parser.parse_args()

    # if os.path.exists(file_path):
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

    infer(multimodal_model)

if __name__=='__main__':
     main()