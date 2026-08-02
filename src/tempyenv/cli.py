import atexit
import logging
import os
import shutil
import signal
import subprocess
import sys
import tempfile

logger = logging.getLogger(__name__)


class TemporaryVenvCreator:
    BASH_COMPATIBLE_SHELLS = {"bash", "sh", "zsh", "ksh"}

    def __init__(self, python_exec=None):
        self.temp_dir = None
        self.venv_path = None
        self.python_exec = python_exec if python_exec is not None else sys.executable
        self.uv_exec = shutil.which("uv")

    def create_temporary_directory(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.venv_path = os.path.join(self.temp_dir.name, 'venv')

    def create_virtual_environment(self):
        try:
            if self.uv_exec:
                subprocess.run([self.uv_exec, 'venv', '--seed', '--python', self.python_exec, self.venv_path], check=True)
                print(f"Virtual environment created at {self.venv_path} (via uv)")
            else:
                subprocess.run([self.python_exec, '-m', 'venv', self.venv_path], check=True)
                print(f"Virtual environment created at {self.venv_path}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error creating virtual environment: {e}")

    def load_virtual_environment(self):
        try:
            print(f"Virtual environment loading from {self.venv_path}")
            user_shell_name = os.path.basename(os.environ.get("SHELL", ""))
            if user_shell_name in self.BASH_COMPATIBLE_SHELLS:
                current_shell = user_shell_name
            else:
                if shutil.which("bash") is None:
                    raise RuntimeError(
                        f"tempyenv only supports bash-compatible shells, but your shell "
                        f"({user_shell_name or 'unknown'}) isn't one and bash was not found on PATH."
                    )
                print("Warning: tempyenv only supports bash-compatible shells, will attempt to launch a new bash shell")
                current_shell = "bash"
            current_ps1 = os.environ.get("PS1", "")
            if os.environ.get("VIRTUAL_ENV_DISABLE_PROMPT"):
                # User already opted out of venv prompt decoration - honor it.
                set_ps1 = ""
            elif current_ps1.startswith("(tempyenv)"):
                # Already inside a tempyenv shell (e.g. tempyenv was run again
                # from a nested shell) - avoid stacking duplicate prefixes.
                set_ps1 = ""
            else:
                set_ps1 = "export PS1=\"(tempyenv)$PS1\\$ \" && "
            subprocess.run([f"{current_shell}",
                            "-c",
                            f"export VIRTUAL_ENV_DISABLE_PROMPT=1 && source {self.venv_path}/bin/activate && {set_ps1}{current_shell}"],
                            stdin=sys.stdin,
                            stdout=sys.stdout,
                            stderr=sys.stderr,
                            check=False)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error loading virtual environment: {e}")

    def cleanup(self):
        if self.temp_dir is not None:
            print("Cleaning up temporary virtual environment...")
            try:
                self.temp_dir.cleanup()
                print("Temporary environment removed successfully.")
            except OSError as e:
                logger.error(f"Error cleaning up temporary environment: {e}")


def main():
    import argparse
    from importlib.metadata import version
    logging.basicConfig(level=logging.ERROR, format="%(levelname)s: %(message)s")
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--python', help='Specify the Python executable', dest='python_exec', default=sys.executable)
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {version("tempyenv")}')
    args = parser.parse_args()
    python_exec = args.python_exec

    print("(tempyenv) is setting up your virtual environment...hold tight")
    venv_creator = TemporaryVenvCreator(python_exec)
    venv_creator.create_temporary_directory()
    venv_creator.create_virtual_environment()

    # Register cleanup handlers for various exit scenarios
    def signal_handler(sig, frame):
        print(f"Received signal {sig}, cleaning up...")
        venv_creator.cleanup()
        sys.exit(0)

    # Register signal handlers for common termination signals
    signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Termination request
    signal.signal(signal.SIGHUP, signal_handler)   # Terminal hang-up
    signal.signal(signal.SIGQUIT, signal_handler)  # Quit signal (Ctrl+\)

    # Register cleanup on normal program exit
    atexit.register(venv_creator.cleanup)

    venv_creator.load_virtual_environment()


if __name__ == "__main__":
    main()
