import os
import logging
from dotenv import load_dotenv


def load_env():
    # Load comments from .env file
    env_path = os.path.join(os.path.dirname(__file__), ".env.public")
    if not env_path:
        assert False, "🚫 api/app/settings: Could not find .env.public file"
    else:
        logging.info(f"✅ Loading secrets at {env_path}")
        load_dotenv(env_path)

    # Load specific environment variables from .env.{ENV} file
    ENV = os.getenv("ENV", "local")
    env_path = os.path.join(os.path.dirname(__file__), f".env.{ENV}")
    if not env_path:
        logging.info(f"🚫 api/app/settings:::.env.{ENV} file")
    else:
        logging.info(f"✅ Loading secrets at {env_path}")
        load_dotenv(env_path)


def getenv(key, default=None):
    value = os.getenv(key, default)
    if value == "True":
        return True
    elif value == "False":
        return False
    elif value == "None":
        return None
    else:
        return value
