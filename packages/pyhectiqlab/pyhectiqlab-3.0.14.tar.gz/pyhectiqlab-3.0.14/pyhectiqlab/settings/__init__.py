import os
import logging
from dotenv import load_dotenv

SECRET_ENV_VARS = {
    "HECTIQLAB_API_KEY": None,
    "HECTIQLAB_CREDENTIALS": os.path.join(os.path.expanduser("~"), ".hectiq-lab/credentials.toml"),
}
PUBLIC_ENV_VARS = {
    "HECTIQLAB_API_URL": "https://api.lab.hectiq.ai",
    "HECTIQLAB_LOG_LEVEL": "warning",
    "HECTIQLAB_PROJECT": None,
    "HECTIQLAB_ALLOW_DIRTY": True,
    "HECTIQLAB_REPOS": None,
    "HECTIQLAB_MODELS_DOWNLOAD": "./",
    "HECTIQLAB_DATASETS_DOWNLOAD": "./",
    "HECTIQLAB_SHOW_PROGRESS": True,
}


def load_env():
    # Load comments from .env file
    env_path = os.path.join(os.path.dirname(__file__), ".env.public")
    if not env_path:
        assert False, f"🚫 api/app/settings: Could not find .env.public file"
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
    if key in SECRET_ENV_VARS:
        value = os.getenv(key, SECRET_ENV_VARS[key])
    elif key in PUBLIC_ENV_VARS:
        value = os.getenv(key, PUBLIC_ENV_VARS[key])
    else:
        value = os.getenv(key, default)

    if value == "True":
        return True
    elif value == "False":
        return False
    elif value == "None":
        return None
    else:
        return value
