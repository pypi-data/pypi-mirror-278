from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import os
import argparse
from .instruct import load_model
import argparse
from llama_index.llms.llama_cpp import LlamaCPP
from huggingface_hub import hf_hub_download
import os
import shutil



def infer(model_path, agentname, temperature=0.5, max_new_tokens=512, model_kwargs={"n_gpu_layers":0}):
        

        persist_directory = os.path.join('db',agentname)

        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        # Create ChromaDB and store document IDs
        db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)


        # Define a prompt template
        prompt_template = "You are a friendly assistant, who gives context aware responses on user query. Kindly analyse the provided context and give proper response\n   Context: {context}\n query:<s>[INST] {prompt} [/INST]"
        # print(model_path)


        # Initialize the Llama model with appropriate parameters
        llm = LlamaCPP(
            model_path=model_path,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            context_window=3900,
            model_kwargs=model_kwargs,
            verbose=False,
        )

        # Start the chat loop
        while True:
            try:
                # Prompt user for input
                user_input = input("\n\nUser: ")

                docs = db.similarity_search(user_input,k=1)
                context=docs[0].page_content

                
                # Exit loop if user types "exit"
                if user_input.lower() == "exit":
                    print("Exiting chat.")
                    break
                
                # Construct prompt with user input
                prompt = prompt_template.format(context=context, prompt=user_input)
                
                # Perform inference
                response_iter = llm.stream_complete(prompt)
                # print("ALLM:", end='')
                
                # Print the assistant's response
                for response in response_iter:
                    print(response.delta, end="", flush=True)

            except KeyboardInterrupt:
                print("\nExiting...")
                break


def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--model", type=str, default="Mistral", help="Name of the model or path to the model file")
    parser.add_argument("--agent", type=str, default=None, help="Name of the agent to query.")
    parser.add_argument("--temperature", type=float, default=0.5, help="Temperature for sampling")
    parser.add_argument("--max_new_tokens", type=int, default=512, help="Maximum number of new tokens to generate")
    parser.add_argument("--model_kwargs", type=dict, default={"n_gpu_layers":0}, help="Arguments for the model")
    args = parser.parse_args()

    model_files = [f for f in os.listdir('model') if f.endswith('.gguf')]

    model_path = load_model(model_files[0])
    if model_path is None:
         print("Model file not found. Kindly download the model or initialize it using allm-run command.")
    else:
         infer(model_path, args.agent, args.temperature, args.max_new_tokens, args.model_kwargs)

if __name__=='__main__':
     main()

