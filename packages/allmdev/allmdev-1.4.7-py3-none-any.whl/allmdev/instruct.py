from llama_index.llms.llama_cpp import LlamaCPP
from huggingface_hub import hf_hub_download
import os
import shutil
from flask import Flask, request, jsonify



def load_model(model):
            model_dir = 'model'
            if not os.path.exists(model_dir):
                os.mkdir(model_dir)

            model_files = [f for f in os.listdir('model') if f.endswith('.gguf')]
            if model_files:
                        if model=='Mistral' or model=='mistral':
                            for file in model_files:
                                if 'mistral' in file.lower():
                                    # print("A mistral model already exists")
                                    # # download_again = input("Do you want to download mistral model again? (yes/y to download): ")
                                    # # if download_again.lower() in ['yes', 'y']:
                                    # #     model_id = "TheBloke/Mistral-7B-v0.1-GGUF"
                                    # #     filename = hf_hub_download(repo_id=model_id, filename="mistral-7b-v0.1.Q8_0.gguf")
                                    # #     shutil.move(filename,model_dir)
                                    # #     model_path = os.path.join(model_dir, filename)
                                    # # else:
                                    # print("Using existing mistral GGUF file")
                                    model_path = os.path.join(model_dir, model_files[0])
                                else:
                                        model_id = "TheBloke/Mistral-7B-v0.1-GGUF"
                                        filename = hf_hub_download(repo_id=model_id, filename="mistral-7b-v0.1.Q8_0.gguf")
                                        shutil.move(filename,model_dir)
                                        model_path = os.path.join(model_dir, filename)

                        elif model=='llama3' or model=='Llama3':
                            for file in model_files:
                                if 'llama3' in file.lower():
                                    # print("A mistral model already exists")
                                    # # download_again = input("Do you want to download mistral model again? (yes/y to download): ")
                                    # # if download_again.lower() in ['yes', 'y']:
                                    # #     model_id = "TheBloke/Mistral-7B-v0.1-GGUF"
                                    # #     filename = hf_hub_download(repo_id=model_id, filename="mistral-7b-v0.1.Q8_0.gguf")
                                    # #     shutil.move(filename,model_dir)
                                    # #     model_path = os.path.join(model_dir, filename)
                                    # # else:
                                    # print("Using existing mistral GGUF file")
                                    model_path = os.path.join(model_dir, model_files[0])
                                else:
                                        model_id = "crusoeai/Llama-3-8B-Instruct-262k-GGUF"
                                        filename = hf_hub_download(repo_id=model_id, filename="llama-3-8b-instruct-262k.Q8_0.gguf")
                                        shutil.move(filename,model_dir)
                                        model_path = os.path.join(model_dir, filename)  
                            

                        elif model=='Mistral_instruct' or model=='mistral_instruct':
                            for file in model_files:
                                if 'mistral-7b-instruct' in file.lower():
                                    # print("A mistral instruct model already exists")
                                    # # download_again = input("Do you want to download mistral instruct model again? (yes/y to download): ")
                                    # # if download_again.lower() in ['yes', 'y']:
                                    # #     model_id = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
                                    # #     filename = hf_hub_download(repo_id=model_id, filename="mistral-7b-instruct-v0.2.Q8_0.gguf")
                                    # #     shutil.move(filename,model_dir)
                                    # #     model_path = os.path.join(model_dir, filename)
                                    # # else:
                                    # print("Using existing mistral instruct GGUF file")
                                    model_path = os.path.join(model_dir, model_files[0])
                                else:
                                    model_id = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
                                    filename = hf_hub_download(repo_id=model_id, filename="mistral-7b-instruct-v0.2.Q8_0.gguf")
                                    shutil.move(filename,model_dir)
                                    model_path = os.path.join(model_dir, filename)

                        
                        elif model=='Llama' or model=='llama' or model=='Llama2' or model=='llama2':
                            for file in model_files:
                                if 'llama' in file.lower():
                                    # print("A llama model already exists")
                                    # # download_again = input("Do you want to download llama model again? (yes/y to download): ")
                                    # # if download_again.lower() in ['yes', 'y']:
                                    # #     model_id = "TheBloke/Llama-2-7B-GGUF"
                                    # #     filename = hf_hub_download(repo_id=model_id, filename="llama-2-7b.Q8_0.gguf")
                                    # #     shutil.move(filename,model_dir)
                                    # #     model_path = os.path.join(model_dir, filename)
                                    # # else:
                                    # print("Using existing llama GGUF file")
                                    model_path = os.path.join(model_dir, model_files[0])
                                else:
                                    model_id = "TheBloke/Llama-2-7B-GGUF"
                                    filename = hf_hub_download(repo_id=model_id, filename="llama-2-7b.Q8_0.gguf")
                                    shutil.move(filename,model_dir)
                                    model_path = os.path.join(model_dir, filename)
                                    

                        elif model=='Llama_chat' or model=='llama_chat' or model=='Llama2_chat' or model=='llama2_chat':
                            for file in model_files:
                                if 'llama-2-7b-instruct' in file.lower():
                                    # print("A llama model already exists")
                                    # # download_again = input("Do you want to download llama chat model again? (yes/y to download): ")
                                    # # if download_again.lower() in ['yes', 'y']:
                                    # #     model_id = "TheBloke/Llama-2-7B-Chat-GGUF"
                                    # #     filename = hf_hub_download(repo_id=model_id, filename="llama-2-7b-chat.Q8_0.gguf")
                                    # #     shutil.move(filename,model_dir)
                                    # #     model_path = os.path.join(model_dir, filename)
                                    # # else:
                                    # print("Using existing llama file")
                                    model_path = os.path.join(model_dir, model_files[0])

                                else:
                                    model_id = "TheBloke/Llama-2-7B-Chat-GGUF"
                                    filename = hf_hub_download(repo_id=model_id, filename="llama-2-7b-chat.Q8_0.gguf")
                                    shutil.move(filename,model_dir)
                                    model_path = os.path.join(model_dir, filename)

                        else:
                            # print("Using existing GGUF file")
                            model_path = os.path.join(model_dir, model_files[0])

            else:
                    if model=='Mistral' or model=='mistral':
                            model_id = "TheBloke/Mistral-7B-v0.1-GGUF"
                            filename = hf_hub_download(repo_id=model_id, filename="mistral-7b-v0.1.Q8_0.gguf")
                            shutil.move(filename,model_dir)
                            model_path = os.path.join(model_dir, filename)
                            

                    elif model=='Mistral_instruct' or model=='mistral_instruct':
                        model_id = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
                        filename = hf_hub_download(repo_id=model_id, filename="mistral-7b-instruct-v0.2.Q8_0.gguf")
                        shutil.move(filename,model_dir)
                        model_path = os.path.join(model_dir, filename)

                    
                    elif model=='Llama' or model=='llama' or model=='Llama2' or model=='llama2':
                        model_id = "TheBloke/Llama-2-7B-GGUF"
                        filename = hf_hub_download(repo_id=model_id, filename="llama-2-7b.Q8_0.gguf")
                        shutil.move(filename,model_dir)
                        model_path = os.path.join(model_dir, filename)

                    elif model=='Llama_chat' or model=='llama_chat' or model=='Llama2_chat' or model=='llama2_chat':
                        model_id = "TheBloke/Llama-2-7B-Chat-GGUF"
                        filename = hf_hub_download(repo_id=model_id, filename="llama-2-7b-chat.Q8_0.gguf")
                        shutil.move(filename,model_dir)
                        model_path = os.path.join(model_dir, filename)

                    else:
                        model_path = model

                    # except:
                    #     print("Kindly check input parameter to the model_load() function. The parameter should be one of the following: \"Mistral\", \"mistral\", \"Mistral_instruct\", \"mistral_instruct\", \"Llama2\", \"Llama2_chat\", or a local gguf file path on your system")

            return model_path



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



def infer(model_path, temperature=0.5, max_new_tokens=512, model_kwargs={"n_gpu_layers":0}):


        # Define a prompt template
        prompt_template = "<s>[INST] {prompt} [/INST]"
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
                
                # Exit loop if user types "exit"
                if user_input.lower() == "exit":
                    print("Exiting chat.")
                    break
                
                # Construct prompt with user input
                prompt = prompt_template.format(prompt=user_input)
                
                # Perform inference
                response_iter = llm.stream_complete(prompt)
                # print("ALLM:", end='')
                
                # Print the assistant's response
                for response in response_iter:
                    print(response.delta, end="", flush=True)

            except KeyboardInterrupt:
                print("\nExiting...")
                break

def api_serve():
        user_input = request.json.get("input")

        if user_input.lower() == "exit":
            return jsonify({"response": "Exiting chat."})

        prompt_template = "<s>[INST] {prompt} [/INST]"
        prompt = prompt_template.format(prompt=user_input)

        response_iter = llm.stream_complete(prompt)
        response_text = ''.join(response.delta for response in response_iter)

        return jsonify({"response": response_text})