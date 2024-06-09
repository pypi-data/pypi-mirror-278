from langchain.document_loaders import CSVLoader, PDFMinerLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import os
import argparse


def initialize_rag(doc_path, persist_directory, agentname):
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

def initialize_rag_from_dir(dir_path, persist_directory, agentname):
    num_files=0
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):
            num_files+=1
            initialize_rag(file_path, persist_directory, agentname)
    return num_files

def main():
    persist_directory = "db"
    if not os.path.exists(persist_directory):
        os.mkdir(persist_directory)
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", type=str, help="Path to the document to process")
    parser.add_argument("--dir", type=str, help="Path to the directory containing files to process")
    parser.add_argument("--agent", type=str, help="Name of agent to be created.")
    args = parser.parse_args()
    if args.doc:
        initialize_rag(args.doc, persist_directory, args.agent)
        print(f"Database for agent '{args.agent}' created at {os.path.join(persist_directory, args.agent)}")
    elif args.dir:
        num_files=initialize_rag_from_dir(args.dir, persist_directory, args.agent)
        print(f"Database for agent '{args.agent}' created from directory '{args.dir}'")
        print(f"{num_files} files ingested by agent '{args.agent}'")
    else:
        print("Please provide either a document using --doc argument or a directory using --dir argument, and specify agent name using --agent argument")

if __name__ == "__main__":
    main()
