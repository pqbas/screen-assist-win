import json
import subprocess
import requests
from tqdm import tqdm
from pathlib import Path
import os


def load_config() -> dict:
    """
    Loads the config file.
    """

    with open("setup/config.json", "r") as file:
        return json.load(file)


def download_github_source(url: str, filename: str) -> None:
    """
    Downloads a file from a GitHub source.
    """

    response = requests.get(url, stream=True)
    total = int(response.headers.get("content-length", 0))

    with open(filename, "wb") as f, tqdm(
        total=total, unit="B", unit_scale=True, desc=f"Downloading {filename}...") as bar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            bar.update(len(chunk))


def generate_download_path(filename: str) -> Path:
    """
    Generates a download path for a file.
    """

    path = Path(os.getcwd()) / load_config()["downloads_folder"] / Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    return path


def pause() -> None:
    """
    Pauses the execution of the program till a key press.
    """

    os.system("pause")


def run_exe(path: Path, elevated: bool = False) -> None:
    """
    Runs an executable file.
    """

    if elevated:
        subprocess.run(["powershell", "-Command", f'Start-Process "{path}" -Verb RunAs -Wait'])
    else:
        subprocess.run([str(path)])
