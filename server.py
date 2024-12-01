import subprocess
import time


def start_django_server():
    """Start the Django server using the test database."""
    server_command = ['python3', 'manage.py', 'runserver', '127.0.0.1:8000']
    server_process = subprocess.Popen(server_command)
    time.sleep(5)
    return server_process

def stop_django_server(server_process):
    """Stop the Django development server."""
    server_process.terminate()
