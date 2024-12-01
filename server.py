import os
import subprocess
import sys
import time

from settings import PROJECT_PATH


def start_django_server():
    """Start the Django server using the test database."""
    project_path = os.path.expanduser(PROJECT_PATH)  # Expands '~' to the full home directory path

    server_command = [sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000']  # Use sys.executable for portability
    try:
        # Start the server process in the Renthub-Connect directory
        server_process = subprocess.Popen(
            server_command,
            cwd=project_path  # Change to the project directory
        )
        time.sleep(5)  # Wait for the server to initialize
        return server_process
    except Exception as e:
        print(f"Failed to start the server: {e}")
        return None


def stop_django_server(server_process):
    """Stop the Django development server."""
    server_process.terminate()
