import tempfile
import subprocess
import os
import sys

class TemporaryVenvCreator:
    def __init__(self):
        self.temp_dir = None
        self.venv_path = None

    def create_temporary_directory(self):
        self.temp_dir = tempfile.TemporaryDirectory(delete=False)
        self.venv_path = os.path.join(self.temp_dir.name, 'venv')

    def create_virtual_environment(self):
        try:
            subprocess.run(['python3', '-m', 'venv', self.venv_path], check=True)
            print(f"Virtual environment created at {self.venv_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error creating virtual environment: {e}")

    def load_virtual_environment(self):
        try:
            print(f"Virtual environment loading from {self.venv_path}")
            #current_shell = os.environ.get("SHELL") # Currently just support bash
            current_shell = "bash"
            subprocess.run([f"{current_shell}",
                            "-c",
                            f"source {self.venv_path}/bin/activate && export PS1=\"(tempyenv)$PS1\\$ \" && {current_shell}"],
                            stdin=sys.stdin,
                            stdout=sys.stdout,
                            stderr=sys.stderr)
        except subprocess.CalledProcessError as e:
            print(f"Error loading virtual environment: {e}")

def main():
    venv_creator = TemporaryVenvCreator()
    venv_creator.create_temporary_directory()
    venv_creator.create_virtual_environment()
    venv_creator.load_virtual_environment()

if __name__ == "__main__":
    main()

