import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "BobAccess")
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # IBM Bob Enterprise API
    BOB_API_KEY: str = os.getenv("BOB_API_KEY", "")
    BOB_API_URL: str = os.getenv("BOB_API_URL", "https://bob.ibm.com")

    # IBM Watson TTS
    IBM_WATSON_TTS_APIKEY: str = os.getenv("IBM_WATSON_TTS_APIKEY", "")
    IBM_WATSON_TTS_URL: str = os.getenv("IBM_WATSON_TTS_URL", "https://api.us-south.text-to-speech.watson.cloud.ibm.com")

    # IBM Watson STT
    IBM_WATSON_STT_APIKEY: str = os.getenv("IBM_WATSON_STT_APIKEY", "")
    IBM_WATSON_STT_URL: str = os.getenv("IBM_WATSON_STT_URL", "https://api.us-south.speech-to-text.watson.cloud.ibm.com")

    # IBM watsonx.ai
    WATSONX_APIKEY: str = os.getenv("WATSONX_APIKEY", "")
    WATSONX_PROJECT_ID: str = os.getenv("WATSONX_PROJECT_ID", "")
    WATSONX_URL: str = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

    # Vector Storage
    CHROMA_PERSIST_DIRECTORY: str = os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma_db")

settings = Settings()
