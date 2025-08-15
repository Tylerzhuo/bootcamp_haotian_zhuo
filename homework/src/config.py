from dotenv import load_dotenv
import os


def load_env():
    load_dotenv()


def get_key():
    return os.getenv("API_KEY")


if __name__ == "__main__":
    load_env()
    print(f"API_KEY loaded: {bool(get_key())}")