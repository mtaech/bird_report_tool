from pathlib import Path


def get_env_path():
    path_dir = Path(__file__).resolve().parent
    return path_dir.joinpath(".env")
