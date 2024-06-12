from fastapi import FastAPI, WebSocket, Request, File, UploadFile, Form, Request, HTTPException, Header, Depends
from flask import request, jsonify
from pydantic import BaseModel
from llama_index.llms.llama_cpp import LlamaCPP
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import asyncio
import os
import json
from fastapi.middleware.cors import CORSMiddleware
import vertexai
from vertexai.generative_models import GenerativeModel
from openai import AzureOpenAI
from fastapi.responses import JSONResponse
from langchain.document_loaders import CSVLoader, PDFMinerLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import hashlib
import re
from datetime import datetime, timedelta
import jwt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

SECRET="!az$y#5%"

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


max_new_tokens = 512
prompt_template = "<s>[INST] {prompt} [/INST]"
config_path = "model/config.json"
vertex_config_path = "model/vertex_config.json"
azure_config_path = "model/azure_config.json"

class Message(BaseModel):
    userInput: str
    model: str
    temperature: float

class Response(BaseModel):
    response: str

class ModelConfig(BaseModel):
    temp: float
    model: str
    gpu: bool
    agent: str

def load_config():
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    else:
        return {
            "temperature": 0.5,
            "model": "",
            "model_path": "",
            "gpu": False
        }
    
def load_vertex_config():
    if os.path.exists(vertex_config_path):
        with open(vertex_config_path, "r") as f:
            return json.load(f)
    else:
        return {
            "projectId": "",
            "modelInput": "gemini-1.0-pro-002",
            "region": "",
        }
    
def load_azure_config():
    if os.path.exists(azure_config_path):
        with open(azure_config_path, "r") as f:
            return json.load(f)
    else:
        return {
            "apikey": "",
            "modelInput": "gemini-1.0-pro-002",
            "version": "",
            "endpoint": ""
        }

def save_config(config):
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)
def save_azure_config(config):
    with open(azure_config_path, "w") as f:
        json.dump(config, f, indent=4)
def save_vertex_config(config):
    with open(vertex_config_path, "w") as f:
        json.dump(config, f, indent=4)

# Database setup function
def setup_database():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        fullname TEXT NOT NULL,
        role TEXT, 
        profilepic TEXT,
        designation TEXT,
        notifications TEXT,
        JWT TEXT
    )
    ''')

    # cursor.execute('''
    # CREATE TABLE IF NOT EXISTS monitoring (
    #     logs TEXT
    # )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS organization (
        name TEXT,
        mainlogo TEXT,
        chatlogo TEXT,
        about TEXT,
        chatdisclaimer TEXT,
        emaillogo TEXT
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        feedback TEXT NOT NULL,
        datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
        chat_id TEXT NOT NULL,
        response TEXT NOT NULL
    )''')  

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sub (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customername TEXT,
        count INTEGER,
        subkey TEXT
    )''')    

    cursor.execute('SELECT COUNT(*) FROM sub')
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute('''
            INSERT INTO sub (customername, count, subkey)
            VALUES (?, ?, ?)
        ''', ("ALLM Enterprise", 2, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0b21lcm5hbWUiOiJBTExNIEVudGVycHJpc2UiLCJwbGFuIjoiMSJ9.fkXsGAwOxwnexKeB6vpbl5CatGUC8O3nNNKnwsa2y9w" ))
        conn.commit()



    name = "ALLM Enterprise"
    mainlogo = "data:image/png;base64,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"
    chatlogo = "data:image/png;base64,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"
    about = "ALLM Studio provides a specialized AI chatbot that meets all the needs of your company. Our cutting-edge technology ensures seamless integration and offers unparalleled support, making it an essential tool for enhancing your business operations. Whether it's customer service, internal communication, or data analysis, our chatbot is designed to deliver exceptional performance and reliability. Partner with us to elevate your company's efficiency and customer satisfaction."
    chatdisclaimer = "Responses can sometimes be incorrect. Please check for accuracy."

    cursor.execute('SELECT COUNT(*) FROM organization')
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute('''
            INSERT INTO organization (name, mainlogo, chatlogo, about, chatdisclaimer)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, mainlogo, chatlogo, about, chatdisclaimer))
        conn.commit()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS smtpsettings (
            senderEmail TEXT,
            receiverEmail TEXT,
            host TEXT,
            username TEXT,
            password TEXT,
            port TEXT,
            userCreation INTEGER DEFAULT 0,  -- BOOLEAN
            userDeletion INTEGER DEFAULT 0,  -- BOOLEAN
            passwordChange INTEGER DEFAULT 0,  -- BOOLEAN
            feedbackNotification INTEGER DEFAULT 0,  -- BOOLEAN
            modelChange INTEGER DEFAULT 0  -- BOOLEAN
        )
    ''')
    cursor.execute('''
        INSERT INTO smtpsettings (senderEmail, receiverEmail, host, username, password, port, userCreation, userDeletion, passwordChange, feedbackNotification, modelChange)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('sender@gmail.com', 'receiver@gmail.com', 'smtp.example.com', 'username', 'password', '587', 0, 0, 0, 0, 0))

    conn.commit()
    conn.close()


config = load_config()

def sanitize_email(email):
    # Replace invalid characters with underscores
    return re.sub(r'[^a-zA-Z0-9]', '_', email)


            

@app.websocket("/model_config")
async def websocket_model_config(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            token=data['token']
            payload = jwt.decode(token, SECRET, algorithms=["HS256"])
            mail = payload.get("email")
            print("Received model config:", data)
            is_vertex_model = "projectId" in data or "region" in data
            is_azure_model = "key" in data  or "version" in data or "endpoint" in data
            conn = sqlite3.connect('user_database.db')
            cursor = conn.cursor() 
            if is_vertex_model:
                vertex_config = {
                    "project_id" : data["projectId"],
                    "model" : data["modelInput"],
                    "region" : data["region"]
                }
                save_vertex_config(vertex_config)
                 
                cursor.execute(f'SELECT mainlogo FROM organization')
                mainlogo = cursor.fetchone()
                cursor.execute("SELECT * FROM smtpsettings")
                settings = cursor.fetchone()
                cursor.execute("SELECT emaillogo from organization")
                emaillogo = cursor.fetchone()[0]
                print(emaillogo)
                if settings[10]:
                    message = MIMEMultipart()
                    message['From'] = settings[0]
                    message['To'] = settings[0]
                    message['Subject'] = "Model configuration updated."
                    body = f'''
                        <html>
                            <head>
                                <style>
                                    body {{
                                        font-family: Arial, sans-serif;
                                        margin: 0;
                                        padding: 0;
                                        background-color: #f4f4f4;
                                    }}
                                    .container {{
                                        width: 50%;
                                        margin: 0 auto;
                                        padding: 20px;
                                        background-color: #ffffff;
                                    }}
                                    .header {{
                                        text-align: center;
                                        padding: 20px;
                                        background-color: #333333;
                                        color: #ffffff;
                                    }}
                                    .logo {{
                                        max-width: 150px;
                                        margin-bottom: 10px;
                                    }}
                                    .content {{
                                        padding: 20px;
                                        line-height: 1.6;
                                        color: #333333;
                                    }}
                                    .footer {{
                                        text-align: left;
                                        padding: 10px;
                                        background-color: #333333;
                                        color: #ffffff;
                                        font-size: 12px;
                                    }}
                                    .notice {{
                                        margin-top: 20px;
                                        font-size: 12px;
                                        color: #999999;
                                    }}
                                </style>
                            </head>
                            <body>
                                <div class="container">
                                    <div class="header">
                                        <img src={emaillogo} alt="Company Logo" class="logo">
                                    </div>
                                    <div class="content">
                                        <p>Hello Admin,</p>
                                        <p>We are writing to inform you that an admin with email : <b>{mail}</b> has been updated the model configuration, the platform is currently using Vertex Cloud Platform.</p>
                                        <p>Thank you for your attention to this matter.</p>
                                        <br>
                                        <p>Best regards,</p>
                                        <p>The ALLM Team</p>
                                    </div>
                                    <div class="footer">
                                        <p>This is an automated email. Please do not reply to this message.</p>
                                        <p class="notice">© 2024 ALLM. All rights reserved.</p>
                                        <p class="notice">ALLM, a product of <a href="https://www.allaai.com" style="color: white;">AllAdvanceAI</a>.</p>
                                    </div>
                                </div>
                            </body>
                            </html>
                        '''
                    message.attach(MIMEText(body, 'html'))
                    with smtplib.SMTP(settings[2], settings[5]) as server:
                        server.starttls()
                        server.ehlo()
                        server.login(settings[3], settings[4])
                        server.sendmail(settings[0], settings[1], message.as_string())
            if is_azure_model:
                azure_config = {
                    "apikey" : data["key"],
                    "version" : data["version"],
                    "endpoint" : data["endpoint"],
                    "modelInput" : data["modelInput"]
                }
                save_azure_config(azure_config)
                cursor.execute(f'SELECT mainlogo FROM organization')
                mainlogo = cursor.fetchone()
                cursor.execute("SELECT * FROM smtpsettings")
                settings = cursor.fetchone()
                cursor.execute("SELECT emaillogo from organization")
                emaillogo = cursor.fetchone()[0]
                if settings[10]:
                    message = MIMEMultipart()
                    message['From'] = settings[0]
                    message['To'] = settings[0]
                    message['Subject'] = "Model configuration updated."
                    body = f'''
                        <html>
                            <head>
                                <style>
                                    body {{
                                        font-family: Arial, sans-serif;
                                        margin: 0;
                                        padding: 0;
                                        background-color: #f4f4f4;
                                    }}
                                    .container {{
                                        width: 50%;
                                        margin: 0 auto;
                                        padding: 20px;
                                        background-color: #ffffff;
                                    }}
                                    .header {{
                                        text-align: center;
                                        padding: 20px;
                                        background-color: #333333;
                                        color: #ffffff;
                                    }}
                                    .logo {{
                                        max-width: 150px;
                                        margin-bottom: 10px;
                                    }}
                                    .content {{
                                        padding: 20px;
                                        line-height: 1.6;
                                        color: #333333;
                                    }}
                                    .footer {{
                                        text-align: left;
                                        padding: 10px;
                                        background-color: #333333;
                                        color: #ffffff;
                                        font-size: 12px;
                                    }}
                                    .notice {{
                                        margin-top: 20px;
                                        font-size: 12px;
                                        color: #999999;
                                    }}
                                </style>
                            </head>
                            <body>
                                <div class="container">
                                    <div class="header">
                                        <img src={emaillogo} alt="Company Logo" class="logo">
                                    </div>
                                    <div class="content">
                                        <p>Hello Admin,</p>
                                        <p>We are writing to inform you that an admin with email : <b>{mail}</b> has been updated the model configuration, the platform is currently using Azure OpenAI Cloud Platform.</p>
                                        <p>Thank you for your attention to this matter.</p>
                                        <br>
                                        <p>Best regards,</p>
                                        <p>The ALLM Team</p>
                                    </div>
                                    <div class="footer">
                                        <p>This is an automated email. Please do not reply to this message.</p>
                                        <p class="notice">© 2024 ALLM. All rights reserved.</p>
                                        <p class="notice">ALLM, a product of <a href="https://www.allaai.com" style="color: white;">AllAdvanceAI</a>.</p>
                                    </div>
                                </div>
                            </body>
                            </html>
                        '''
                    message.attach(MIMEText(body, 'html'))
                    with smtplib.SMTP(settings[2], settings[5]) as server:
                        server.starttls()
                        server.ehlo()
                        server.login(settings[3], settings[4])
                        server.sendmail(settings[0], settings[1], message.as_string())
            else:

                model_config = load_config()
                temp = model_config["temperature"]
                model = model_config["model"]
                gpu = model_config["gpu"]
                
                if model != data["model"] or temp != data["temperature"]:
                    model_config["model"] = data["model"]
                    model_config["temperature"] = data["temperature"]

                    model_directory = "model"
                    for file in os.listdir(model_directory):
                        if file.endswith('.gguf') and config["model"].lower() in file:
                            config["model_path"] = os.path.join(model_directory, file)
                            break

                    save_config(config)
                    cursor.execute(f'SELECT mainlogo FROM organization')
                    mainlogo = cursor.fetchone()
                    cursor.execute("SELECT * FROM smtpsettings")
                    settings = cursor.fetchone()
                    cursor.execute("SELECT emaillogo from organization")
                    emaillogo = cursor.fetchone()[0]
                    if settings[10]:
                        message = MIMEMultipart()
                        message['From'] = settings[0]
                        message['To'] = settings[0]
                        message['Subject'] = "Model configuration updated."
                        body = f'''
                            <html>
                                <head>
                                    <style>
                                        body {{
                                            font-family: Arial, sans-serif;
                                            margin: 0;
                                            padding: 0;
                                            background-color: #f4f4f4;
                                        }}
                                        .container {{
                                            width: 50%;
                                            margin: 0 auto;
                                            padding: 20px;
                                            background-color: #ffffff;
                                        }}
                                        .header {{
                                            text-align: center;
                                            padding: 20px;
                                            background-color: #333333;
                                            color: #ffffff;
                                        }}
                                        .logo {{
                                            max-width: 150px;
                                            margin-bottom: 10px;
                                        }}
                                        .content {{
                                            padding: 20px;
                                            line-height: 1.6;
                                            color: #333333;
                                        }}
                                        .footer {{
                                            text-align: left;
                                            padding: 10px;
                                            background-color: #333333;
                                            color: #ffffff;
                                            font-size: 12px;
                                        }}
                                        .notice {{
                                            margin-top: 20px;
                                            font-size: 12px;
                                            color: #999999;
                                        }}
                                    </style>
                                </head>
                                <body>
                                    <div class="container">
                                        <div class="header">
                                            <img src={emaillogo} alt="Company Logo" class="logo">
                                        </div>
                                        <div class="content">
                                            <p>Hello Admin,</p>
                                            <p>We are writing to inform you that an admin with email : <b>{mail}</b> has been updated the model configuration, the platform is currently using large language model present on local server.</p>
                                            <p>Thank you for your attention to this matter.</p>
                                            <br>
                                            <p>Best regards,</p>
                                            <p>The ALLM Team</p>
                                        </div>
                                        <div class="footer">
                                            <p>This is an automated email. Please do not reply to this message.</p>
                                            <p class="notice">© 2024 ALLM. All rights reserved.</p>
                                            <p class="notice">ALLM, a product of <a href="https://www.allaai.com" style="color: white;">AllAdvanceAI</a>.</p>
                                        </div>
                                    </div>
                                </body>
                                </html>
                            '''
                        message.attach(MIMEText(body, 'html'))
                        with smtplib.SMTP(settings[2], settings[5]) as server:
                            server.starttls()
                            server.ehlo()
                            server.login(settings[3], settings[4])
                            server.sendmail(settings[0], settings[1], message.as_string())

                # model_kwargs = {"n_gpu_layers": -1 if gpu else 0}
                # llm = LlamaCPP(
                #     model_path=config["model_path"],
                #     temperature=config["temperature"],
                #     max_new_tokens=max_new_tokens,
                #     context_window=3900,
                #     model_kwargs=model_kwargs,
                #     verbose=False,
                # )
            await websocket.send_json({"status": "success", "message": "Model configuration updated."})

    except Exception as e:
        print(e)
    # finally:
    #     await websocket.close()


    
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            print("ws route")
            user_input = data["userInput"]
            # print(user_input)
            if user_input == "!*33$":
                # print('Sending API status ')
                await websocket.send_json({"status": True, 'route':'Ws'})
                await websocket.close()
                break

            prompt = prompt_template.format(prompt=user_input)
            model_kwargs = {"n_gpu_layers": -1 if config["gpu"] else 0}
            llm = LlamaCPP(
                model_path=config["model_path"],
                temperature=config["temperature"],
                max_new_tokens=max_new_tokens,
                context_window=3900,
                model_kwargs=model_kwargs,
                verbose=False,
            )
            response_iter = llm.stream_complete(prompt)

            for response in response_iter:
                await websocket.send_text(response.delta)
                await asyncio.sleep(0)
                if websocket.client_state.name != 'CONNECTED':
                    break

            await websocket.close()
            

    except Exception as e:
        print(e)
        await websocket.close()
    # finally:
    #     await websocket.close()


@app.websocket("/available_agents")
async def agentinfo(websocket: WebSocket):
    await websocket.accept()
    agents = os.listdir('db')
    dict = {
        'agentinfo': agents
    }
    await websocket.send_json(dict)

@app.websocket("/agent")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        config=load_config()
        model_kwargs = {"n_gpu_layers" : -1 if config["gpu"] else 0}
        llm = LlamaCPP(
            model_path=config["model_path"],
            temperature=config["temperature"],
            max_new_tokens=max_new_tokens,
            context_window=3900,
            model_kwargs=model_kwargs,
            verbose=False,
        )
        while True:
            data = await websocket.receive_json()
            print(data)
            print("agent route")
            user_input = data["userInput"]
            
            if user_input == "!*33$":
                # print('Sending API status ')
                await websocket.send_json({"status": True, 'route':'Agent'})
                await websocket.close()
                break

            agent = data['agent']
            persist_directory = os.path.join('db', agent)
            embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)

            docs = db.similarity_search(user_input, k=3)
            context = docs[0].page_content
            prompt_template = "You are a friendly assistant, who gives context aware responses on user query. Kindly analyse the provided context and give proper response\n   Context: {context}\n query:<s>[INST] {prompt} [/INST]"
            prompt = prompt_template.format(context=context, prompt=user_input)

            # model_kwargs = {"n_gpu_layers" : -1 if config["gpu"] else 0}
            # llm = LlamaCPP(
            #     model_path=config["model_path"],
            #     temperature=config["temperature"],
            #     max_new_tokens=max_new_tokens,
            #     context_window=3900,
            #     model_kwargs=model_kwargs,
            #     verbose=False,
            # )

            response_iter = llm.stream_complete(prompt)

            for response in response_iter:
                await websocket.send_text(response.delta)
                await asyncio.sleep(0)


                save_config(config)
            await websocket.close()

        
    except Exception as e:
        print(e)
        await websocket.close()
    # finally:
    #     await websocket.close()

@app.websocket("/vertex")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        config=load_vertex_config()
        while True:
            data = await websocket.receive_json()
            print(data)
            print("vertex route")
            prompt = data["userInput"]
            
            if prompt == "!*33$":
                print('Sending API status ')
                await websocket.send_json({"status": True, 'route':'Vertex'})
                await websocket.close()
                break

            agent = data['agent']
            projectid=config["project_id"]
            region=config["region"]
            model=config["model"]
            vertexai.init(project=projectid, location=region)
            multimodal_model = GenerativeModel(model_name=model)
            if agent == "None":
                response = multimodal_model.generate_content(prompt)
                await websocket.send_text(response.text)
                await websocket.close()
            else:

                persist_directory = os.path.join('db', agent)
                embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
                db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)

                docs = db.similarity_search(prompt, k=3)
                context = docs[0].page_content
                prompt_template = "You are a friendly assistant, who gives context aware responses on user query. Kindly analyse the provided context and give proper response\n   Context: {context}\n query:<s>[INST] {prompt} [/INST]"
                prompt = prompt_template.format(context=context, prompt=prompt)
                response = multimodal_model.generate_content(prompt)
                await websocket.send_text(response.text)
                await websocket.close()
           

    except Exception as e:
        print(e)
        await websocket.close()
    # finally:
    #     await websocket.close()

@app.websocket("/azure")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        config=load_azure_config()
        while True:
            data = await websocket.receive_json()
            print(data)
            print("azure route")
            prompt = data["userInput"]
            
            if prompt == "!*33$":
                print('Sending API status ')
                await websocket.send_json({"status": True, 'route':'Azure'})
                await websocket.close()
                break

            agent = data['agent']
            key=config['apikey']
            version=config['version']
            model=config['modelInput']
            endpoint=config['endpoint']


            client = AzureOpenAI(
                api_key = (key),
                api_version = version,
                azure_endpoint = (endpoint)
            )

            if agent == "None":
                response = client.chat.completions.create(
                    model=model, # model = "deployment_name".
                    messages=[
                        {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
                        {"role": "user", "content": prompt}
                        
                    ]
                )
                for choice in response.choices:
                    await websocket.send_text(choice.message.content)
                    await websocket.close()
            else:
                persist_directory = os.path.join('db', agent)
                if os.path.exists(persist_directory):
                    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
                    db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)
                    docs = db.similarity_search(prompt, k=3)
                    context = docs[0].page_content
                    prompt_template = "You are a friendly assistant, who gives context aware responses on user query. Kindly analyse the provided context and give proper response\n   Context: {context}\n query:<s>[INST] {prompt} [/INST]"
                    prompt = prompt_template.format(context=context, prompt=prompt)
                    response = client.chat.completions.create(
                            model=model, # model = "deployment_name".
                            messages=[
                                {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
                                {"role": "user", "content": prompt}
                                
                            ]
                        )
                    for choice in response.choices:
                        await websocket.send_text(choice.message.content)
                    await websocket.close()

    except Exception as e:
        print(e)
        await websocket.close()
    # finally:
    #     await websocket.close()



# class RequestData(BaseModel):
#     agent: str
#     file: UploadFile
@app.post("/create_agent")
async def upload_file(name: str = Form(...),file: UploadFile = File(...)):
        try:
            agentname = name
            uploaded_file = file
            # Process the uploaded file
            # Example: Save the file locally
            if not os.path.exists("uploads"):
                os.mkdir("uploads")
            file_path = f"uploads/{uploaded_file.filename}"
            with open(file_path, "wb") as file_object:
                file_object.write(await uploaded_file.read())
            persist_directory = 'db'
            doc_path = os.path.normpath(file_path)
            agent_directory = os.path.join(persist_directory, agentname)
            if not os.path.exists(agent_directory):
                os.makedirs(agent_directory)

            # Load the document
            if doc_path.endswith(".csv"):
                loader = CSVLoader(doc_path)
            elif doc_path.endswith(".pdf"):
                loader = PDFMinerLoader(doc_path)
            elif doc_path.endswith(".docx"):
                loader = TextLoader(doc_path)
            else:
                raise ValueError("Unsupported file format. Supported formats are CSV, PDF, and DOCX.")

            documents = loader.load()

            # Split the document into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=500)
            texts = text_splitter.split_documents(documents)

            # Create embeddings
            embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

            # Create ChromaDB and store document IDs
            db = Chroma.from_documents(texts, embeddings, persist_directory=agent_directory)
            db.persist()

            doc_ids_path = os.path.join(agent_directory, f"{agentname}_docids.txt")

            # Store document IDs in a file
            with open(doc_ids_path, "a") as f:
                for text_id, _ in enumerate(texts):
                    document_id = f"doc_{text_id}"
                    f.write(f"{document_id}\n")
            return JSONResponse(content={"agentname": name, "message": "agent created successfully"}) 
        



        except Exception as e:
            print(e)

@app.post("/update_agent")
async def upload_file(name: str = Form(...),file: UploadFile = File(...)):
        try:
            agentname = name
            uploaded_file = file
            # Process the uploaded file
            # Example: Save the file locally
            # if not os.path.exists("uploads"):
            #     os.mkdir("uploads")
            i=len(os.listdir(f"uploads/{agentname}"))
            file_path = f"/{agentname}/{uploaded_file.filename}{i}"
            with open(file_path, "wb") as file_object:
                file_object.write(await uploaded_file.read())
            persist_directory = 'db'
            doc_path = os.path.normpath(file_path)
            agent_directory = os.path.join(persist_directory, agentname)
            if not os.path.exists(agent_directory):
                os.makedirs(agent_directory)

            for file in os.listdir(f"uploads/{agentname}"):

            # Load the document
                if file.endswith(".csv"):
                    loader = CSVLoader(file)
                elif file.endswith(".pdf"):
                    loader = PDFMinerLoader(file)
                elif file.endswith(".docx"):
                    loader = TextLoader(file)
                else:
                    raise ValueError("Unsupported file format. Supported formats are CSV, PDF, and DOCX.")

                documents = loader.load()

                # Split the document into chunks
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=500)
                texts = text_splitter.split_documents(documents)

                # Create embeddings
                embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

                # Create ChromaDB and store document IDs
                db = Chroma.from_documents(texts, embeddings, persist_directory=agent_directory)
                db.persist()

                # doc_ids_path = os.path.join(agent_directory, f"{agentname}_docids.txt")

                # Store document IDs in a file
                # with open(doc_ids_path, "a") as f:
                #     for text_id, _ in enumerate(texts):
                #         document_id = f"doc_{text_id}"
                #         f.write(f"{document_id}\n")
            return JSONResponse(content={"agentname": name, "message": "agent updated successfully"}) 
        



        except Exception as e:
            print(e)

@app.websocket("/configdata")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        print(data)
        if data == "Azure":
            azure_config=load_azure_config()
            await websocket.send_json(azure_config)
        elif data == "Vertex":
            vertex_config=load_vertex_config()
            await websocket.send_json(vertex_config)
        else:
            config=load_config()
            await websocket.send_json(config)

    except Exception as e:
        print(e)
    finally:
        await websocket.close()


@app.post("/signup")
async def signup(request: Request):
    data = await request.json()
    fullname = data.get('fullname')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    profilepic = data.get('profilepic')
    designation = data.get('designation')
    notifications = data.get('notifications')

    if not email or not password or not fullname:
        raise HTTPException(status_code=400, detail="Required fields are missing")

    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE email LIKE 'root@%'")
    root_user_count = cursor.fetchone()[0]

    if "root@" in email and password == "rootroot":
        if root_user_count > 0:
            conn.close()
            return {"message": "Root user already exists"}
        role = "admin"
        profilepic = 'data:image/jpeg;base64,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'
    else:
        role = "user"

    cursor.execute("SELECT count FROM sub")
    max_count=cursor.fetchone()
    

    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()

    # cursor.execute("SELECT name from organization")
    # orgname = cursor.fetchone()

    # cursor.execute("SELECT subkey from sub")
    # subkey = cursor.fetchone()
    # payload = jwt.decode(subkey, SECRET, algorithms=["HS256"])
    # customername = payload.get("customername")

    # print("--->",orgname, customername)


    if max_count is None: 
        max_count = 0
    if user_count is (0,):
        user_count = 0

    print("---->",max_count, user_count)

    if user_count <= max_count:
        # Check if '@' is in the email to distinguish signup from user creation
        if '@' in email:
            try:
                cursor.execute('''
                    INSERT INTO users (email, password, fullname, role, profilepic, designation, notifications)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (email, hashlib.sha256(password.encode()).hexdigest(), fullname, role, profilepic, designation, notifications))

                token = jwt.encode({'email': email}, SECRET, algorithm='HS256')

                # Store JWT token in the database
                cursor.execute('''
                    UPDATE users SET jwt = ? WHERE email = ?
                ''', (token, email))

                sanitized_table_name = sanitize_email(email)
                cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {sanitized_table_name} (
                        chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        messageheader TEXT,
                        chats TEXT                   
                    )
                ''')
                conn.commit()
                cursor.execute("SELECT * FROM smtpsettings")
                settings = cursor.fetchone()
                cursor.execute("SELECT mainlogo FROM organization LIMIT 1")
                mainlogo_data = cursor.fetchone()
                cursor.execute("SELECT emaillogo from organization")
                emaillogo = cursor.fetchone()[0]
                if settings:
                    if settings[6]:
                        message = MIMEMultipart()
                        message['From'] = settings[0]
                        message['To'] = settings[0]
                        message['Subject'] = "User added to platform"
                        body = f'''
                                <html>
                                <head>
                                    <style>
                                        body {{
                                            font-family: Arial, sans-serif;
                                            margin: 0;
                                            padding: 0;
                                            background-color: #f4f4f4;
                                        }}
                                        .container {{
                                            width: 50%;
                                            margin: 0 auto;
                                            padding: 20px;
                                            background-color: #ffffff;
                                        }}
                                        .header {{
                                            text-align: center;
                                            padding: 20px;
                                            background-color: #333333;
                                            color: #ffffff;
                                        }}
                                        .logo {{
                                            max-width: 150px;
                                            margin-bottom: 10px;
                                        }}
                                        .content {{
                                            padding: 20px;
                                            line-height: 1.6;
                                            color: #333333;
                                        }}
                                        .footer {{
                                            text-align: left;
                                            padding: 10px;
                                            background-color: #333333;
                                            color: #ffffff;
                                            font-size: 12px;
                                        }}
                                        .notice {{
                                            margin-top: 20px;
                                            font-size: 12px;
                                            color: #999999;
                                        }}
                                    </style>
                                </head>
                                <body>
                                    <div class="container">
                                        <div class="header">
                                            <img src={emaillogo} alt="Company Logo" class="logo">
                                        </div>
                                        <div class="content">
                                            <p>Hello Admin,</p>
                                            <p>We are writing to inform you that a user with name : <b>{fullname}</b> and role : <b>{role}</b> has been added to the platform.</p>
                                            <p>Thank you for your attention to this matter.</p>
                                            <br>
                                            <p>Best regards,</p>
                                            <p>The ALLM Team</p>
                                        </div>
                                        <div class="footer">
                                            <p>This is an automated email. Please do not reply to this message.</p>
                                            <p class="notice">© 2024 ALLM. All rights reserved.</p>
                                            <p class="notice">ALLM, a product of <a href="https://www.allaai.com" style="color: white;">AllAdvanceAI</a>.</p>
                                        </div>
                                    </div>
                                </body>
                                </html>
                                '''
                        message.attach(MIMEText(body, 'html'))
                        with smtplib.SMTP(settings[2], settings[5]) as server:
                            server.starttls()
                            server.ehlo()
                            server.login(settings[3], settings[4])
                            server.sendmail(settings[0], settings[1], message.as_string())
            
                    response = {'message': 'User signed up successfully!'}
                
            except sqlite3.IntegrityError:
                response = {'message': 'Username already exists!'}
            except Exception as e:
                response = {'message': 'Error occurred while signing up'}
                print(e)
            
        else:
            response = {'message': 'Email format is not correct'}
            raise HTTPException(status_code=400, detail=response)
    else:
        response = {'message': 'Maximum number of users reached, please upgrade your plan'}

    conn.close()
    return response

# Route for user login
@app.route('/login', methods=['POST'])
async def login(request: Request):
    data = await request.json()
    email = data['email']
    password = data['password']

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT id, fullname, role FROM users WHERE email = ? AND password = ?
    ''', (email, hashed_password))

    user = cursor.fetchone()

    if user:
        print(user)
        user_id = user[0]
        fullname = user[1]
        role = user[2]
        token = jwt.encode({'email': email, 'role': user[2]}, SECRET, algorithm='HS256')
        print(fullname, user_id)
        response = {'message': f"Welcome, {fullname}!","status": True, "token": token, "role": role }
    else:
        response = {'message': 'Invalid username or password.'}

    conn.close()
    return JSONResponse(content=response)

def is_user(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user_role = payload.get("role")
        if user_role and user_role.lower() == 'admin':
            return True
        else:
            return False
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/check_user")
def check_user(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    token = authorization.split(" ")[1]  # Assuming the header is "Bearer <token>"
    
    if is_user(token):
        return {"status": "true"}
    else:
        raise HTTPException(status_code=403, detail="You are not authorized to access this page")


@app.get("/fetch_profile_img")
def fetch_profile_img(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    token = authorization.split(" ")[1]  # Assuming the header is "Bearer <token>"
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    email = payload.get("email")
    role = payload.get("role")
    
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT profilepic FROM users WHERE email = ?
    ''', (email,))

    profilepicstring = cursor.fetchone()
    conn.close()

    if profilepicstring:
        # Assuming profilepicstring is a base64 encoded string stored in the database
        profilepic_base64 = profilepicstring[0]  # Assuming the profile picture is in the first column
        return {"profile_pic_base64": profilepic_base64,"role":role}
    else:
        raise HTTPException(status_code=404, detail="Profile picture not found for the user")
    
@app.post('/newchat')
async def update_chat_history(request: Request):
    data = await request.json()
    print(data)
    user_email = data['userEmail']
    message_header = data['messageheader']
    chats = data['chats']
    
    # Convert the chats array to a JSON string
    chats_json = json.dumps(chats)

    # Connect to the database
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    try:
        # Execute query to insert data into the specified user's table
        cursor.execute(f'''
            INSERT INTO {user_email} (messageheader, chats)
            VALUES (?, ?)
        ''', (message_header, chats_json))

        cursor.execute(f'''
            SELECT chat_id FROM {user_email}
            WHERE messageheader = ?
        ''', (message_header,))
        
        # Fetch the chat_id
        chat_id = cursor.fetchone()[0]

        # Commit the transaction
        conn.commit()

        # Close the database connection
        conn.close()

        return JSONResponse(content={'message': 'Chat history updated successfully.', 'chat_id': chat_id})
    except Exception as e:
        # Rollback changes if an error occurs
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=500, detail=f'Error updating chat history: {str(e)}')
    

@app.post('/fetchchat')
async def fetch_chat_history(request: Request):
    data = await request.json()
    print(data)
    user_email = data['userEmail']
    chat_id = data['chat_id']

    # Connect to the database
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    try:
        # Execute query to fetch chat history based on userEmail and chat_id
        cursor.execute(f'''
            SELECT chats FROM {user_email}
            WHERE chat_id = ?
        ''', (chat_id,))
        
        # Fetch the chat history
        chat_history = cursor.fetchone()

        if chat_history:
            # Parse the chat history from JSON
            chat_history_json = json.loads(chat_history[0])
            return JSONResponse(content={'chat': chat_history_json})
        else:
            raise HTTPException(status_code=404, detail='Chat history not found.')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f'Error fetching chat history: {str(e)}')
    finally:
        # Close the database connection
        conn.close()

@app.post('/updatechat')
async def update_chat_history(request: Request):
    data = await request.json()
    user_email = data['userEmail']
    chat_id = data['chat_id']
    updated_chats = data['chats']
    
    # Convert the updated chats array to a JSON string
    updated_chats_json = json.dumps(updated_chats)

    # Connect to the database
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    try:
        # Execute query to update the chat data for the specified chat_id
        cursor.execute(f'''
            UPDATE {user_email}
            SET chats = ?
            WHERE chat_id = ?
        ''', (updated_chats_json, chat_id))

        # Check if any rows were affected
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Chat not found.")
        
        # Commit the transaction
        conn.commit()

        return JSONResponse(content={'message': 'Chat history updated successfully.'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error updating chat history: {str(e)}')
    finally:
        # Close the database connection
        conn.close()

def get_start_of_day(date):
    return date.replace(hour=0, minute=0, second=0, microsecond=0)

def get_date_x_days_ago(days):
    return get_start_of_day(datetime.now() - timedelta(days=days))

@app.post('/fetchchatsidebar')
async def fetch_chat_sidebar(request: Request):
    data = await request.json()
    print(data)
    user_email = data.get('userEmail')

    if not user_email:
        raise HTTPException(status_code=400, detail='userEmail is required')

    email_safe = user_email.replace('.', '_').replace('@', '_')
    today_start = get_start_of_day(datetime.now())
    yesterday_start = get_date_x_days_ago(1)

    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    try:
        cursor.execute(f'''
            SELECT chat_id, messageheader, timestamp
            FROM {email_safe}
        ''')

        chats = cursor.fetchall()

        today_chats = []
        yesterday_chats = []
        previous_chats = []


        for chat in chats:
            chat_id, message_header, timestamp = chat
            chat_date = datetime.fromisoformat(timestamp)

            if chat_date >= today_start:
                today_chats.append({
                    'chat_id': chat_id,
                    'message_header': message_header,
                    'timestamp': timestamp
                })
            elif chat_date >= yesterday_start and chat_date < today_start:
                yesterday_chats.append({
                    'chat_id': chat_id,
                    'message_header': message_header,
                    'timestamp': timestamp
                })
            else:
                previous_chats.append({
                    'chat_id': chat_id,
                    'message_header': message_header,
                    'timestamp': timestamp
                })

        return JSONResponse(content={
            'today': today_chats,
            'yesterday': yesterday_chats,
            'previous': previous_chats
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error fetching chat sidebar: {str(e)}')
    finally:
        conn.close()

@app.route('/fetch_user_details', methods=['POST'])
async def fetch_user_details(request: Request):
    data = await request.json()
    email = data['email']

    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT email, fullname, role, profilepic, designation, notifications, JWT FROM users WHERE email = ?
    ''', (email,))

    user = cursor.fetchone()

    if user:
        email, fullname, role, profilepic, designation, notifications, JWT = user
        response = {
            'status': True,
            'email': email,
            'fullname': fullname,
            'role': role,
            'profilepic': profilepic,
            'designation': designation,
            'notifications': notifications,
            "JWT":JWT
        }
    else:
        response = {'status': False, 'message': 'User not found'}

    conn.close()
    return JSONResponse(content=response)


@app.get("/fetch_users")
async def fetch_non_admin_users():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT email, fullname, role, profilepic, designation, notifications 
    FROM users 
    ''')

    users = cursor.fetchall()

    user_list = [
        {
            "email": user[0],
            "fullname": user[1],
            "role": user[2],
            "profilepic": user[3],
            "designation": user[4],
            "notifications": user[5]
        }
        for user in users
    ]

    conn.close()
    return JSONResponse(content={"status": True, "users": user_list})


class UpdateUserRequest(BaseModel):
    email: str
    password: str
    fullname: str
    role: str
    profilepic: str
    designation: str
    notifications: str

@app.post('/update_user')
async def update_user(request: Request):
    data = await request.json()
    print(data)
    email = data.get('email')

    # Validate that email is provided
    if not email:
        raise HTTPException(status_code=400, detail="Email is required to update user information.")
    
    update_fields = {
        'password': data.get('password'),
        'fullname': data.get('fullname'),
        'role': data.get('role'),
        'profilepic': data.get('profilepic'),
        'designation': data.get('designation'),
        'notifications': data.get('notifications')
    }
    
    # Filter out None values from the update_fields dictionary
    update_fields = {k: v for k, v in update_fields.items() if v is not None}
    
    # Validate that at least one field to update is provided
    if not update_fields:
        raise HTTPException(status_code=400, detail="At least one field is required to update user information.")
    
    set_clause = ', '.join([f"{k} = ?" for k in update_fields.keys()])
    values = list(update_fields.values())
    values.append(email)  # Add email to the end of the values list for the WHERE clause
    
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"UPDATE users SET {set_clause} WHERE email = ?", values)
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found.")
        
        response = {'message': 'User information updated successfully.', 'status': True}
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()
    
    return JSONResponse(content=response)

@app.post("/delete_user")
async def delete_user(request: Request):
    data = await request.json()
    email = data.get('email')

    if not email:
        raise HTTPException(status_code=400, detail="Email not provided")

    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    # Check if the user exists
    cursor.execute('SELECT 1 FROM users WHERE email = ?', (email,))
    user_exists = cursor.fetchone()

    if not user_exists:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user
    cursor.execute('DELETE FROM users WHERE email = ?', (email,))
    sanitized_table_name = sanitize_email(email)
    cursor.execute(f'DROP TABLE IF EXISTS {sanitized_table_name}')
    conn.commit()
    cursor.execute(f'SELECT mainlogo FROM organization')
    mainlogo = cursor.fetchone()
    cursor.execute("SELECT * FROM smtpsettings")
    settings = cursor.fetchone()
    cursor.execute("SELECT emaillogo from organization")
    emaillogo = cursor.fetchone()[0]
    if settings[7]:
        message = MIMEMultipart()
        message['From'] = settings[0]
        message['To'] = settings[0]
        message['Subject'] = "User deleted from platform"
        body = f'''
            <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            background-color: #f4f4f4;
                        }}
                        .container {{
                            width: 50%;
                            margin: 0 auto;
                            padding: 20px;
                            background-color: #ffffff;
                        }}
                        .header {{
                            text-align: center;
                            padding: 20px;
                            background-color: #333333;
                            color: #ffffff;
                        }}
                        .logo {{
                            max-width: 150px;
                            margin-bottom: 10px;
                        }}
                        .content {{
                            padding: 20px;
                            line-height: 1.6;
                            color: #333333;
                        }}
                        .footer {{
                            text-align: left;
                            padding: 10px;
                            background-color: #333333;
                            color: #ffffff;
                            font-size: 12px;
                        }}
                        .notice {{
                            margin-top: 20px;
                            font-size: 12px;
                            color: #999999;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <img src={emaillogo} alt="Company Logo" class="logo">
                        </div>
                        <div class="content">
                            <p>Hello Admin,</p>
                            <p>We are writing to inform you that a user with email : <b>{email}</b> has been deleted from the platform.</p>
                            <p>Thank you for your attention to this matter.</p>
                            <br>
                            <p>Best regards,</p>
                            <p>The ALLM Team</p>
                        </div>
                        <div class="footer">
                            <p>This is an automated email. Please do not reply to this message.</p>
                            <p class="notice">© 2024 ALLM. All rights reserved.</p>
                            <p class="notice">ALLM, a product of <a href="https://www.allaai.com" style="color: white;">AllAdvanceAI</a>.</p>
                        </div>
                    </div>
                </body>
                </html>
            '''
        message.attach(MIMEText(body, 'html'))
        with smtplib.SMTP(settings[2], settings[5]) as server:
            server.starttls()
            server.ehlo()
            server.login(settings[3], settings[4])
            server.sendmail(settings[0], settings[1], message.as_string())
    conn.close()

    return {"message": "User deleted successfully"}


@app.post('/update_org_details')
async def add_orgData(request: Request):
    data = await request.json()
    
    # Extract values from the JSON data
    name = data.get('name')
    mainlogo = data.get('mainlogo')
    chatlogo = data.get('chatlogo')
    about = data.get('about')
    chatdisclaimer = data.get('chatdisclaimer')
    emaillogo = data.get('emaillogo')
    # # subkey = data.get('subkey')
    # subkey_bytes = subkey[0].encode('utf-8')
    # print(type(subkey[0]))
    # print(type(subkey))
    # print(subkey)
    # payload = jwt.decode(subkey_bytes, SECRET, algorithms=['HS256'])
    # print(payload)

    # Validate that all required fields are present
    # if not all([name, mainlogo, chatlogo, about, chatdisclaimer, emaillogo,subkey]):
    #     raise HTTPException(status_code=400, detail="All fields are required: name, mainlogo, chatlogo, about, chatdisclaimer, subkey")
    


    
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    
    try:
        # Check if any data exists in the organization table
        cursor.execute("SELECT COUNT(*) FROM organization")
        row_count = cursor.fetchone()[0]
        
        if row_count == 0:
            # If no data exists, insert new row
            cursor.execute("""
                INSERT INTO organization (name, mainlogo, chatlogo, about, chatdisclaimer, emaillogo)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, mainlogo, chatlogo, about, chatdisclaimer, emaillogo))
        else:
            # If data exists, update the existing row
            cursor.execute("""
                UPDATE organization
                SET name = ?, mainlogo = ?, chatlogo = ?, about = ?, chatdisclaimer = ?, emaillogo = ?
            """, (name, mainlogo, chatlogo, about, chatdisclaimer, emaillogo))

        # if subkey != '':
           
        #     customername = payload.get('customername')
        #     count = payload.get('plan')
        #     print(customername,count)
        #     cursor.execute("SELECT name from organization")
        #     orgname = cursor.fetchone()[0]
        #     print("--->",orgname, customername)

        #     if orgname != customername:
        #         return {"message": "The Subscription Key is not valid!!"}
        #     cursor.execute("SELECT COUNT(*) FROM sub")
        #     row_count_sub = cursor.fetchone()[0]
        #     if row_count_sub == 0:
        #         # If no data exists, insert new row
        #         cursor.execute("""
        #             INSERT INTO sub (customername, count, subkey)
        #             VALUES (?, ?, ?)
        #         """, (customername, count, subkey))
        #     else:
        #         # If data exists, update the existing row
        #         cursor.execute("""
        #             UPDATE sub
        #             SET customername = ?, count = ?, subkey = ?
        #         """, (customername, count, subkey))
        

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Database operation failed: " + str(e))
    finally:
        conn.close()
    
    return {"message": "Organization details updated successfully"}


@app.get("/get_org_details")
async def get_org_details():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    # try:
    cursor.execute("SELECT name, mainlogo, chatlogo, about, chatdisclaimer, emaillogo FROM organization LIMIT 1")
    result = cursor.fetchone()

    cursor.execute("SELECT subkey FROM sub")
    subkey = cursor.fetchone()

    if result:
        org_details = {
            "name": result[0],
            "mainlogo": result[1],
            "chatlogo": result[2],
            "about": result[3],
            "chatdisclaimer": result[4],
            "emaillogo": result[5],
            "subkey":subkey
        }
        return org_details
        conn.close()
    else:
        raise HTTPException(status_code=404, detail="Organization details not found")
    # except Exception as e:
        # raise HTTPException(status_code=500, detail="Database query failed: " + str(e))
    # finally:

@app.post("/update_smtpsettings")
async def update_smtpsettings(request: Request):
    data = await request.json()
    print(data)
    # Extract the data from the request
    senderEmail = data.get('senderEmail')
    receiverEmail = data.get('receiverEmail')
    host = data.get('host')
    username = data.get('username')
    password = data.get('password')
    port = data.get('port')
    
    notifications = data.get('notifications', {})
    userCreation = int(notifications.get('userCreation', False))
    userDeletion = int(notifications.get('userDeletion', False))
    passwordChange = int(notifications.get('passwordChange', False))
    feedbackNotification = int(notifications.get('feedbackNotification', False))
    modelChange = int(notifications.get('modelChange', False))

    # Connect to the database
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    try:
        # Check if there is an existing row
        cursor.execute('SELECT * FROM smtpsettings')
        existing_settings = cursor.fetchone()

        if existing_settings:
            # Update the existing row
            cursor.execute('''
                UPDATE smtpsettings
                SET senderEmail = ?,
                    receiverEmail = ?,
                    host = ?,
                    username = ?,
                    password = ?,
                    port = ?,
                    userCreation = ?,
                    userDeletion = ?,
                    passwordChange = ?,
                    feedbackNotification = ?,
                    modelChange = ?
            ''', (
                senderEmail, receiverEmail, host, username, password, port,
                userCreation, userDeletion, passwordChange, feedbackNotification, modelChange
            ))
        else:
            # Insert a new row
            cursor.execute('''
                INSERT INTO smtpsettings (
                    senderEmail, receiverEmail, host, username, password, port,
                    userCreation, userDeletion, passwordChange, feedbackNotification, modelChange
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                senderEmail, receiverEmail, host, username, password, port,
                userCreation, userDeletion, passwordChange, feedbackNotification, modelChange
            ))

        # Commit the transaction
        conn.commit()

        return JSONResponse(content={'message': 'SMTP settings updated successfully.'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error updating SMTP settings: {str(e)}')
    finally:
        # Close the database connection
        conn.close()

@app.get("/get_smtp_settings")
async def get_smtp_settings():
    # Connect to the database
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    try:
        # Fetch all settings from the table
        cursor.execute('SELECT * FROM smtpsettings')
        settings_row = cursor.fetchone()

        if settings_row:
            # Convert row data to a dictionary (assuming a single row)
            smtp_settings = {
                "senderEmail": settings_row[0],
                "receiverEmail": settings_row[1],
                "host": settings_row[2],
                "username": settings_row[3],
                "password": settings_row[4],
                "port": settings_row[5],
                "notifications": {
                    "userCreation": bool(settings_row[6]),  # Convert integer to boolean
                    "userDeletion": bool(settings_row[7]),
                    "passwordChange": bool(settings_row[8]),
                    "feedbackNotification": bool(settings_row[9]),
                    "modelChange": bool(settings_row[10]),
                }
            }
            return JSONResponse(content={"settings":smtp_settings})
        else:
            # No settings found, return an empty dictionary
            return JSONResponse(content={"message": "No SMTP settings found."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error fetching SMTP settings: {str(e)}')
    finally:
        # Close the database connection
        conn.close()

def get_chat_counts():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    try:
        labels = []
        values = [0] * 7  # Initialize values for the last 7 days
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=6)
        print(end_date,start_date)
        
        for i in range(7):
            labels.append((start_date + timedelta(days=i)).strftime('%d %b'))

        print(labels)
        # Get the list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(tables)

        for table in tables:
            table_name = table[0]
            print(table_name)
            if table_name in ['users', 'organization', 'smtpsettings', 'monitoring','sqlite_sequence', 'user_feedback','sub']:
                continue

            
            for i in range(7):
                day = start_date + timedelta(days=i)
                next_day = day + timedelta(days=1)
                cursor.execute(f"""
                    SELECT COUNT(*) FROM {table_name}
                    WHERE DATE(timestamp) >= ? AND DATE(timestamp) < ?
                """, (day, next_day))
                count = cursor.fetchone()[0]
                values[i] += count
        
        return {"labels": labels, "values": values}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

@app.get("/dashboard_data")
async def get_dashboard_data():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    try:
        # Get the total number of users
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='user'")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM user_feedback")
        total_feedbacks = cursor.fetchone()[0]

        local_model_count = 0

        for file in os.listdir('model'):
            if file.endswith('.gguf'):
                local_model_count += 1

        # Count the number of files in the 'db' and 'dist' directories
        db_files = os.listdir('db')
        dist_files = os.listdir('dist')
        chats = get_chat_counts()
        db_file_count = len(db_files)
        dist_file_count = len(dist_files)
        print(db_file_count, dist_file_count, total_users)
        print(chats)
        # Prepare the response data
        response_data = {
            "total_users": total_users,
            "agent_count": db_file_count,
            "dist_file_count": dist_file_count,
            'chats':chats,
            "total_feedbacks": total_feedbacks,
            "local_model_count": local_model_count
        }

        return response_data
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

def get_current_user_email(request: Request):
    authorization_header = request.headers.get('Authorization')
    print(authorization_header)
    if authorization_header is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    token = authorization_header.split(' ')[1]
    print(token)
    if not token:
        raise HTTPException(status_code=401, detail="Authorization header missing")


    payload = jwt.decode(token, SECRET, algorithms=['HS256'])
    print(payload)
    email = payload.get('email')
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid JWT token")
    return email

@app.post("/submit_feedback")
async def submit_feedback(request: Request, email: str = Depends(get_current_user_email)):
    feedback_data = await request.json()
    # Validate the received data
    if 'content' not in feedback_data or 'chatid' not in feedback_data:
        raise HTTPException(status_code=400, detail="Invalid request body")

    feedback = feedback_data['content']['feedback']
    chatid = feedback_data['chatid']
    response = feedback_data['content']['response']
    print(feedback, chatid)
    try:
        with sqlite3.connect('user_database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO user_feedback (email, feedback, datetime, chat_id, response)
            VALUES (?, ?, ?, ?,?)
            ''', (email, feedback, datetime.now(), chatid, response))
            conn.commit()
            cursor.execute(f'SELECT mainlogo FROM organization')
            mainlogo = cursor.fetchone()
            cursor.execute("SELECT * FROM smtpsettings")
            settings = cursor.fetchone()
            cursor.execute("SELECT emaillogo from organization")
            emaillogo = cursor.fetchone()[0]
            if settings[9]:
                message = MIMEMultipart()
                message['From'] = settings[0]
                message['To'] = settings[0]
                message['Subject'] = "New feedback recieved from a user."
                body = f'''
                    <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    margin: 0;
                                    padding: 0;
                                    background-color: #f4f4f4;
                                }}
                                .container {{
                                    width: 50%;
                                    margin: 0 auto;
                                    padding: 20px;
                                    background-color: #ffffff;
                                }}
                                .header {{
                                    text-align: center;
                                    padding: 20px;
                                    background-color: #333333;
                                    color: #ffffff;
                                }}
                                .logo {{
                                    max-width: 150px;
                                    margin-bottom: 10px;
                                }}
                                .content {{
                                    padding: 20px;
                                    line-height: 1.6;
                                    color: #333333;
                                }}
                                .footer {{
                                    text-align: left;
                                    padding: 10px;
                                    background-color: #333333;
                                    color: #ffffff;
                                    font-size: 12px;
                                }}
                                .notice {{
                                    margin-top: 20px;
                                    font-size: 12px;
                                    color: #999999;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <div class="header">
                                    <img src={emaillogo} alt="Company Logo" class="logo">
                                </div>
                                <div class="content">
                                    <p>Hello Admin,</p>
                                    <p>We are writing to inform you that a feedback : <b>{feedback}</b> has been recieved from a user with email : {email}.</p>
                                    <p>Thank you for your attention to this matter.</p>
                                    <br>
                                    <p>Best regards,</p>
                                    <p>The ALLM Team</p>
                                </div>
                                <div class="footer">
                                    <p>This is an automated email. Please do not reply to this message.</p>
                                    <p class="notice">© 2024 ALLM. All rights reserved.</p>
                                    <p class="notice">ALLM, a product of <a href="https://www.allaai.com" style="color: white;">AllAdvanceAI</a>.</p>
                                </div>
                            </div>
                        </body>
                        </html>
                    '''
                message.attach(MIMEText(body, 'html'))
                with smtplib.SMTP(settings[2], settings[5]) as server:
                    server.starttls()
                    server.ehlo()
                    server.login(settings[3], settings[4])
                    server.sendmail(settings[0], settings[1], message.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert feedback into database: {str(e)}")

    return {"message": "Feedback submitted successfully"}

@app.get("/model_info")
async def get_model_info():
    model_dir=os.listdir('model')
    model_list=[]
    for file in model_dir:
        if file.endswith('gguf'):
            if "mistral-7b-instruct" in file.lower():
                model_list.append("mistral-instruct")
            if "mistral-7b-v" in file.lower():
                model_list.append("mistral")
            if "llama2" in file.lower():
                model_list.append("llama2")
            if "llama3" in file.lower():
                model_list.append("llama3")
    model_list.append("Vertex")
    model_list.append("Azure")
    print('Models List',model_list)
    return JSONResponse({"models": model_list})

@app.get("/checkssl")
async def check_ssl():
    try:
        return JSONResponse({"ssl":False})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No SSL certiicate provided: {str(e)}")


def main():
    import uvicorn
    import warnings
    warnings.filterwarnings('ignore') 

    setup_database()
    model_dir = "model"

    config = {
        "cert_file": "",
        "cert_key": ""
    }

    #file_path=os.path.join(model_dir, "apiconfig.json")
    #if not os.path.exists(file_path):
    #    with open(file_path, "w") as json_file:
    #        json.dump(config, json_file)
    #with open(file_path, "r") as json_file:
    #       config = json.load(json_file)
    #        cert_file=config["cert_file"]
    #        cert_key=config["cert_key"]
    #if cert_file is not "" and cert_key is not "":
    #    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_certfile=cert_file, ssl_keyfile=cert_key)
    #else:
       # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()