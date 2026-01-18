import argparse
import os.path

from omegaconf import OmegaConf

from crypto.hybrid import Hybrid
from const import CONFIG_DIR, ROOT_DIR


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", type=str, help=""
                                                       "Changes mode of script:"
                                                       "generate - generates keys"
                                                       "encrypt - encrypts ur txt"
                                                       "decrypt - decrypts ur txt")
    parser.add_argument(
        "-e", "--env",
        type=str,
        default="dev",
        choices=["dev", "prod"],
        help="Environment config to use"
    )
    arguments = parser.parse_args()
    return arguments

def load_config(env: str):
    base_path = os.path.join(CONFIG_DIR, "base.yaml")
    env_path = os.path.join(CONFIG_DIR, f"{env}.yaml")

    base_conf = OmegaConf.load(base_path)
    env_conf = OmegaConf.load(env_path)

    return OmegaConf.merge(base_conf, env_conf)

def prepare_directories(paths: dict) -> None:
    for file_path in paths.values():
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

def main() -> None:
    args = get_args()
    config = load_config(args.env)

    settings = {}
    for name, relative_path in config.paths.items():
        settings[name] = os.path.join(ROOT_DIR, relative_path)
    prepare_directories(settings)

    hybrid = Hybrid()
    match args.mode:
        case "generate":
            hybrid.generate_keys(settings["public_key"],
                                 settings["private_key"],
                                 settings["symmetric_key"])
        case "encrypt":
            hybrid.encrypt_data(settings["plain_text"],
                                settings["private_key"],
                                settings["symmetric_key"],
                                settings["encrypted_text"])
        case "decrypt":
            hybrid.decrypt_data(settings["encrypted_text"],
                                settings["private_key"],
                                settings["symmetric_key"],
                                settings["decrypted_text"])


if __name__ == "__main__":
    main()

