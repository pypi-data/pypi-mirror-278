import subprocess
import os

def start_backend():
    # Path to your backend script
    backend_script = os.path.join(os.path.dirname(__file__), 'backend.py')
    # Start the backend
    subprocess.Popen(['python', backend_script])

def start_frontend():
    # Path to your frontend directory
    client_dir = os.path.join(os.path.dirname(__file__), '..', 'client')
    # Start the frontend
    subprocess.Popen(['npm', 'run', 'dev'], cwd=client_dir)

def main():
    start_backend()
    start_frontend()

if __name__ == "__main__":
    main()
